"""
12306省心小助手 - 路线规划页面
支持智能站点名匹配
"""

import streamlit as st
from core.planner import RoutePlanner
from core.filter import RouteFilter
from core.scorer import RouteScorer
from api.client_12306 import Client12306

st.set_page_config(page_title="路线规划 🔍", page_icon="🔍", layout="wide")

st.title("🔍 路线规划")
st.caption("输入出发地和目的地，智能推荐最优出行方案")

# 初始化客户端获取站点列表（用于模糊匹配）
@st.cache_data
def get_all_stations():
    """获取所有站点名称列表"""
    client = Client12306()
    # 触发站点数据加载
    client._load_station_data()
    return client._station_names if client._station_names else []


@st.cache_data
def get_station_suggestions(keyword: str) -> list[str]:
    """
    获取站点建议列表
    
    Args:
        keyword: 用户输入的关键词
        
    Returns:
        匹配的站点名称列表
    """
    if not keyword or len(keyword) < 1:
        return []
    
    client = Client12306()
    return client.fuzzy_search_stations(keyword)


# ===== 查询表单 =====
with st.form("route_query"):
    col1, col2, col3 = st.columns(3)
    
    # 获取站点列表
    all_stations = get_all_stations()

    with col1:
        from_station_input = st.text_input("🚉 出发地", placeholder="如：东安东、长沙、北京")
        # 如果有模糊匹配，显示提示
        if from_station_input:
            suggestions = get_station_suggestions(from_station_input)
            if suggestions and from_station_input not in suggestions:
                st.caption(f"💡 匹配到: {', '.join(suggestions[:5])}")

    with col2:
        to_station_input = st.text_input("🏁 目的地", placeholder="如：深圳、拉萨、广州")
        # 如果有模糊匹配，显示提示
        if to_station_input:
            suggestions = get_station_suggestions(to_station_input)
            if suggestions and to_station_input not in suggestions:
                st.caption(f"💡 匹配到: {', '.join(suggestions[:5])}")

    with col3:
        travel_date = st.date_input("📅 出发日期")

    st.divider()

    col_pref1, col_pref2, col_pref3, col_pref4, col_pref5 = st.columns(5)
    with col_pref1:
        pref_cheap = st.checkbox("💰 最便宜", value=False)
    with col_pref2:
        pref_fast = st.checkbox("⚡ 最快速", value=False)
    with col_pref3:
        pref_direct = st.checkbox("🔄 最少换乘", value=False)
    with col_pref4:
        pref_balance = st.checkbox("⚖️ 性价比", value=True)
    with col_pref5:
        pref_comfort = st.checkbox("🛋️ 最舒适", value=False)

    submitted = st.form_submit_button("🚂 查询路线", use_container_width=True)

# ===== 查询结果 =====
if submitted:
    # 获取用户输入的站名（使用原始输入，让后端自动解析）
    from_station = from_station_input.strip()
    to_station = to_station_input.strip()
    
    if not from_station or not to_station:
        st.error("请输入出发地和目的地！")
    elif from_station == to_station:
        st.error("出发地和目的地不能相同！")
    else:
        # 确定偏好
        if pref_cheap:
            preference = "cheapest"
        elif pref_fast:
            preference = "fastest"
        elif pref_direct:
            preference = "fewest_transfer"
        elif pref_comfort:
            preference = "comfortable"
        else:
            preference = "balanced"

        with st.spinner(f"正在查询 {from_station} → {to_station} 的路线..."):
            planner = RoutePlanner()
            routes = planner.search(
                from_station=from_station,
                to_station=to_station,
                travel_date=str(travel_date),
            )

            if not routes:
                st.warning(f"未找到 {from_station} → {to_station} 的直达路线，正在查找换乘方案...")
                routes = planner.search_with_transfer(
                    from_station=from_station,
                    to_station=to_station,
                    travel_date=str(travel_date),
                )

            if routes:
                # 筛选和评分
                route_filter = RouteFilter(preference=preference)
                scored_routes = RouteScorer.score_all(routes, preference=preference)
                sorted_routes = route_filter.sort(scored_routes)

                st.success(f"找到 {len(sorted_routes)} 个方案！")

                # 方案对比表
                st.markdown("### 📊 方案对比")
                display_routes = []
                for i, route in enumerate(sorted_routes[:10]):
                    display_routes.append({
                        "排名": i + 1,
                        "车次": route.train_no,
                        "出发→到达": f"{route.from_station}→{route.to_station}",
                        "出发时间": route.depart_time,
                        "到达时间": route.arrive_time,
                        "历时": route.duration,
                        "换乘": f"{route.transfers}次" if route.transfers > 0 else "直达",
                        "参考票价": f"¥{route.price_low}~{route.price_high}",
                        "综合评分": f"⭐ {route.score:.0f}/100",
                    })
                st.dataframe(display_routes, use_container_width=True, hide_index=True)

                # 详细方案卡片
                st.markdown("### 📋 方案详情")
                for i, route in enumerate(sorted_routes[:5]):
                    score_emoji = "🟢" if route.score >= 80 else "🟡" if route.score >= 60 else "🔴"
                    with st.expander(
                        f"{score_emoji} 方案{i+1}：{route.train_no} | "
                        f"{route.duration} | ¥{route.price_low}~{route.price_high} | "
                        f"评分 {route.score:.0f}",
                        expanded=(i == 0),
                    ):
                        col_a, col_b = st.columns([2, 1])
                        with col_a:
                            st.markdown(f"**🚉 {route.from_station}** → **{route.to_station}**")
                            st.markdown(f"⏰ {route.depart_time} → {route.arrive_time}")
                            st.markdown(f"🕐 历时：{route.duration}")
                            if route.transfers > 0:
                                st.markdown(f"🔄 换乘：{route.transfers}次")
                                for t in route.transfer_details:
                                    st.markdown(f"  - {t}")
                        with col_b:
                            st.markdown(f"💰 参考票价：")
                            if route.price_yz:
                                st.markdown(f"  硬座：¥{route.price_yz}")
                            if route.price_rw:
                                st.markdown(f"  硬卧：¥{route.price_rw}")
                            if route.price_yw:
                                st.markdown(f"  软卧：¥{route.price_yw}")
                            if route.price_edz:
                                st.markdown(f"  二等座：¥{route.price_edz}")
                            if route.price_ydz:
                                st.markdown(f"  一等座：¥{route.price_ydz}")
                            if route.price_swb:
                                st.markdown(f"  商务座：¥{route.price_swb}")

                        st.info("⚠️ 以上信息仅供参考，实际票价和时刻请以12306为准")
            else:
                st.error(f"抱歉，未找到 {from_station} → {to_station} 的可用路线 😢")
                st.markdown("**建议：**")
                st.markdown("- 检查站名是否正确")
                st.markdown("- 尝试输入更完整的站名（如「长沙南」而非「长沙」）")
                st.markdown("- 尝试附近的大站作为出发/到达站")
                st.markdown("- 直接到 [12306](https://www.12306.cn) 查询")
else:
    # 未查询时显示提示
    st.info("👆 输入出发地和目的地，选择偏好后点击查询")
    st.markdown("### 💡 使用提示")
    st.markdown("- 支持**直达**和**换乘**方案查询")
    st.markdown("- 支持智能站名匹配：输入「长沙」会自动匹配「长沙」或「长沙南」")
    st.markdown("- 5种筛选偏好可按需选择，默认推荐性价比最高的方案")
    st.markdown("- 换乘方案会自动计算等待时间和换乘指引")
