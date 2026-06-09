"""路径修复：确保项目根目录在 sys.path 中"""
import sys
from pathlib import Path
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

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

# ===== 注入全局样式 =====
from components.styles import inject_styles
inject_styles()

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

                # 方案对比表 - 卡片化展示
                st.markdown("### 📊 方案对比")
                
                # 顶部方案卡片
                for i, route in enumerate(sorted_routes[:3]):
                    rank_emoji = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
                    score_color = "#FFD700" if i == 0 else "#C0C0C0" if i == 1 else "#CD7F32" if i == 2 else "#666"
                    
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            background: white;
                            border-radius: 16px;
                            padding: 16px;
                            margin: 8px 0;
                            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
                            border: 1px solid rgba(0,0,0,0.04);
                        ">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="display:flex; align-items:center;">
                                    <span style="font-size:1.5rem; margin-right:12px;">{rank_emoji}</span>
                                    <div>
                                        <h4 style="margin:0; color:#004E89;">{route.train_no}</h4>
                                        <p style="margin:4px 0 0; color:#666; font-size:0.9rem;">
                                            {route.from_station} → {route.to_station}
                                        </p>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:1.2rem; font-weight:bold; color:#FF6B35;">
                                        {route.duration}
                                    </div>
                                    <div style="font-size:0.85rem; color:#666;">
                                        ¥{route.price_low}~{route.price_high}
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # 详细方案卡片
                st.markdown("### 📋 方案详情")
                for i, route in enumerate(sorted_routes[:5]):
                    score_emoji = "🟢" if route.score >= 80 else "🟡" if route.score >= 60 else "🔴"
                    rank_class = "rank-1" if i == 0 else "rank-2" if i == 1 else "rank-3" if i == 2 else ""
                    
                    with st.expander(
                        f"{score_emoji} 方案{i+1} | {route.train_no} | "
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
                            st.markdown("**💰 票价参考**")
                            # 票价用色块区分
                            price_items = []
                            if route.price_yz:
                                price_items.append(f'<span class="ticket-chip ticket-yz">硬座 ¥{route.price_yz}</span>')
                            if route.price_rw:
                                price_items.append(f'<span class="ticket-chip ticket-rw">软座 ¥{route.price_rw}</span>')
                            if route.price_yw:
                                price_items.append(f'<span class="ticket-chip ticket-yw">硬卧 ¥{route.price_yw}</span>')
                            if route.price_edz:
                                price_items.append(f'<span class="ticket-chip ticket-edz">二等 ¥{route.price_edz}</span>')
                            if route.price_ydz:
                                price_items.append(f'<span class="ticket-chip ticket-ydz">一等 ¥{route.price_ydz}</span>')
                            if route.price_swb:
                                price_items.append(f'<span class="ticket-chip ticket-swb">商务 ¥{route.price_swb}</span>')
                            
                            if price_items:
                                st.markdown(" ".join(price_items), unsafe_allow_html=True)

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
    
    # 使用提示卡片
    st.markdown("""
    <div class="feature-card">
    <h4 style="color:#004E89; margin:0 0 12px;">💡 使用提示</h4>
    <ul style="color:#333; font-size:0.9rem; padding-left:16px; margin:0;">
        <li style="margin:6px 0;">支持<strong>直达</strong>和<strong>换乘</strong>方案查询</li>
        <li style="margin:6px 0;">支持智能站名匹配：输入「长沙」会自动匹配「长沙」或「长沙南」</li>
        <li style="margin:6px 0;">5种筛选偏好可按需选择，默认推荐性价比最高的方案</li>
        <li style="margin:6px 0;">换乘方案会自动计算等待时间和换乘指引</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
