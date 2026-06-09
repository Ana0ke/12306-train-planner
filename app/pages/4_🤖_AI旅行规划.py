"""路径修复：确保项目根目录在 sys.path 中"""
import sys
from pathlib import Path
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

"""
12306省心小助手 - AI旅行规划页面
对话式生成个性化旅行方案

功能：
1. Demo预览模式 - 无API Key也能体验热门目的地旅行方案
2. 多城市联程规划 - 支持"成都+九寨沟"等格式
3. 出行日期智能感知 - 自动提供季节、天气、节假日提醒
4. MCP真实数据查询 - 配置MCP_SERVER_URL后可查询真实车次
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

from api.llm_client import check_llm_status
from api.demo_plans import get_demo_plan_by_destination, POPULAR_DESTINATIONS
from api.client_12306 import Client12306
from components.styles import inject_styles

st.set_page_config(page_title="AI旅行规划 🤖", page_icon="🤖", layout="wide")
inject_styles()
from core.ai_planner import AIPlanner
from core.planner import RoutePlanner
from core.itinerary import TripPlan
from core.season_engine import get_season_info, get_holiday_alert, get_seasonal_recommendation


# ===== 页面状态初始化 =====
if "trip_plan" not in st.session_state:
    st.session_state.trip_plan = None
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "train_route_info" not in st.session_state:
    st.session_state.train_route_info = None
if "selected_demo" not in st.session_state:
    st.session_state.selected_demo = None
if "travel_date" not in st.session_state:
    st.session_state.travel_date = None
if "season_info_display" not in st.session_state:
    st.session_state.season_info_display = None
if "last_from_station" not in st.session_state:
    st.session_state.last_from_station = ""  # 记住上次输入的出发城市


def check_llm_config() -> bool:
    """检查LLM配置状态"""
    status = check_llm_status()
    return status["configured"]


# ===== 页面标题 =====
st.title("🤖 AI旅行规划")
st.markdown('<p style="color:#666;">告诉我想去哪里、玩几天，我来帮你规划！</p>', unsafe_allow_html=True)

# ===== LLM配置检查 =====
llm_configured = check_llm_config()

# 初始化12306客户端用于数据来源判断
client_12306 = Client12306()

# ===== Demo预览模式（无API Key或用户选择）=====
if not llm_configured:
    st.info("🎭 **体验模式** - 正在展示热门目的地的示例旅行方案。配置API Key后可生成个性化方案！")

# ===== 功能说明 =====
with st.expander("📖 功能说明", expanded=False):
    st.markdown("""
    ### 🤖 AI旅行规划功能

    **核心功能：**
    1. 🎭 **Demo预览** - 无需配置API Key，也能查看热门目的地的示例旅行方案
    2. 🏙️ **多城市联程** - 支持"成都+九寨沟"或"拉萨→纳木错"格式，一次规划多个城市
    3. 📅 **日期感知** - 选择出行日期后，自动提供季节、天气、穿衣建议和节假日提醒

    **使用提示：**
    - 输入目的地（如"拉萨"、"成都+九寨沟"）
    - 设置旅行天数和预算
    - 选择出行日期获取季节建议
    - 点击生成专属旅行方案
    """)

st.divider()

# ===== Demo热门方案体验 =====
st.markdown("### 🎯 热门方案体验（无需API Key）")

# 展示热门目的地卡片 - 圆形按钮样式
demo_cols = st.columns(5)
for i, dest in enumerate(POPULAR_DESTINATIONS):
    with demo_cols[i]:
        # 显示目的地卡片
        with st.container():
            st.markdown(f"""
            <div class="feature-card" style="text-align:center; padding:16px;">
                <div style="font-size:2rem; margin-bottom:4px;">{dest['emoji']}</div>
                <h4 style="margin:0; color:#004E89;">{dest['name']}</h4>
                <p style="color:#666; font-size:0.8rem; margin:4px 0;">{dest['days']}日游</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"查看方案", key=f"demo_{dest['key']}", use_container_width=True):
                # 获取demo方案
                demo_plan = get_demo_plan_by_destination(dest['key'])
                if demo_plan:
                    st.session_state.trip_plan = demo_plan
                    st.session_state.selected_demo = dest['key']
                    st.rerun()
                else:
                    st.error(f"未找到{dest['name']}的方案")

# 显示选中的Demo方案
if st.session_state.trip_plan and st.session_state.selected_demo:
    st.divider()
    _display_trip_plan(st.session_state.trip_plan, is_demo=True)
    st.info("👆 以上为示例方案。配置API Key后可生成专属方案！")

    if st.button("🔄 清除方案", use_container_width=True):
        st.session_state.trip_plan = None
        st.session_state.selected_demo = None
        st.rerun()

    st.stop()  # Demo模式下不显示后续表单

# ===== AI规划表单 =====
st.divider()
st.markdown("### ✨ AI生成专属方案")

# 如果有LLM，显示完整表单
with st.form("ai_trip_form"):
    st.markdown("#### 🎯 告诉我你的旅行需求")

    # 第一行：目的地和天数
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        destination = st.text_input(
            "🏔️ 目的地",
            placeholder="如：拉萨、成都+九寨沟、西安→华山",
            help="支持多城市，用 + 或 → 连接，如成都+九寨沟"
        )
        # 多城市提示
        if destination:
            from core.ai_planner import AIPlanner
            planner = AIPlanner()
            cities = planner._parse_multi_destination(destination)
            if len(cities) > 1:
                st.success(f"🏙️ 检测到{len(cities)}个城市：{' → '.join(cities)}")

    with col2:
        days = st.number_input(
            "📅 旅行天数",
            min_value=1,
            max_value=15,
            value=5,
            help="计划游玩的天数"
        )

    with col3:
        # 使用上次输入的值作为默认值，如果为空则显示空字符串
        default_from = st.session_state.last_from_station if st.session_state.last_from_station else ""
        from_station = st.text_input(
            "🚂 出发城市",
            value=default_from,
            placeholder="如：北京、上海",
            help="从哪里出发（为空则跳过火车查询）"
        )

    # 第二行：出行日期和预算
    col4, col5 = st.columns(2)

    with col4:
        travel_date_input = st.date_input(
            "📆 出行日期（可选）",
            value=None,
            min_value=date.today(),
            max_value=date.today().replace(year=date.today().year + 1),
            help="选择日期获取季节建议和节假日提醒"
        )
        # 将date转为字符串
        travel_date_str = travel_date_input.strftime("%Y-%m-%d") if travel_date_input else None

    with col5:
        budget = st.number_input(
            "💰 预算（元）",
            min_value=0,
            value=3000,
            step=100,
            help="总预算，留空则自动估算"
        )

    # 季节信息展示
    if travel_date_str and destination:
        try:
            # 解析目的地（取第一个城市）
            planner = AIPlanner()
            cities = planner._parse_multi_destination(destination)
            main_city = cities[0]

            month = travel_date_input.month
            season_info = get_season_info(main_city, month)
            holiday_info = get_holiday_alert(travel_date_input)
            seasonal_rec = get_seasonal_recommendation(main_city, month)

            st.markdown("---")
            st.markdown(f"#### 📅 {travel_date_str} 季节信息")

            # 节假日提醒
            if holiday_info.get("alert"):
                if holiday_info.get("is_holiday"):
                    st.warning(f"{holiday_info['alert']}")
                else:
                    st.info(f"{holiday_info['alert']}")

            # 季节卡片
            season_col1, season_col2, season_col3, season_col4 = st.columns(4)

            with season_col1:
                st.metric("🌡️ 季节", season_info['season'])
            with season_col2:
                st.metric("🌤️ 天气", season_info['weather'])
            with season_col3:
                st.metric("💨 气温", season_info['temp'])
            with season_col4:
                st.metric("👔 穿衣", season_info.get('clothes', '未知')[:8])

            st.markdown(f"**👔 穿衣建议：** {season_info['clothes']}")
            st.markdown(f"**💡 注意事项：** {season_info['tips']}")
            st.markdown(f"**🌸 季节推荐：** {seasonal_rec}")

            if holiday_info.get("tips"):
                st.markdown(f"**📌 出行建议：**")
                for tip in holiday_info["tips"]:
                    st.markdown(f"- {tip}")

            # 保存季节信息用于后续
            st.session_state.season_info_display = season_info

        except Exception as e:
            st.warning(f"无法获取季节信息：{e}")

    # 偏好标签
    st.markdown("**🎯 旅行偏好**（可多选）")
    pref_cols = st.columns(6)
    preferences = []

    prefs = [
        ("🍜", "美食优先"),
        ("🏛️", "文化历史"),
        ("🏔️", "自然风光"),
        ("📸", "拍照打卡"),
        ("💰", "省钱为主"),
        ("🛋️", "舒适为主"),
    ]

    pref_state = [False] * len(prefs)
    for i, (emoji, label) in enumerate(prefs):
        with pref_cols[i]:
            if st.checkbox(f"{emoji}", value=pref_state[i], key=f"pref_{i}"):
                preferences.append(label)

    submitted = st.form_submit_button("✨ 生成旅行方案", use_container_width=True)


# ===== 处理查询 =====
if submitted:
    # 保存出发城市到session_state
    if from_station:
        st.session_state.last_from_station = from_station
    
    if not destination:
        st.error("请输入目的地！")
    else:
        # 如果出发城市为空，直接跳过火车查询
        if not from_station:
            train_info = None
        else:
            # 查询火车路线
            with st.spinner("🔍 查询最优火车路线..."):
                try:
                    planner = RoutePlanner()
                    # 直接用search_with_transfer，它内部会先查直达再查换乘
                    routes = planner.search_with_transfer(
                        from_station=from_station,
                        to_station=destination,
                        travel_date="2024-01-01",  # 日期不影响路线
                    )

                    # 选择最优方案
                    train_info = None
                    if routes:
                        best_route = routes[0]
                        train_info = {
                            "train_no": best_route.train_no,
                            "from_station": best_route.from_station,
                            "to_station": best_route.to_station,
                            "depart_time": best_route.depart_time,
                            "arrive_time": best_route.arrive_time,
                            "duration": best_route.duration,
                            "train_type": best_route.train_type,
                            "transfers": best_route.transfers,
                            "price_range": f"¥{best_route.price_low}~¥{best_route.price_high}",
                            "price_low": best_route.price_low,
                            "tips": f"{best_route.train_type}，{'直达' if best_route.transfers == 0 else f'换乘{best_route.transfers}次'}" + \
                                    f"，建议提前购票",
                        }
                        st.session_state.train_route_info = train_info

                    # 显示路线方案
                    if train_info:
                        data_source = "🟢 实时数据" if client_12306.using_mcp else "📊 演示数据"
                        st.success(f"找到最优路线：{train_info['train_no']} {train_info['depart_time']}→{train_info['arrive_time']} [{data_source}]")

                except Exception as e:
                    st.warning(f"路线查询失败，将跳过火车信息: {e}")
                    train_info = None

        # 调用AI生成行程
        with st.spinner("🤖 AI正在为你规划行程，请稍候..."):
            try:
                ai_planner = AIPlanner()
                trip_plan = ai_planner.plan_trip(
                    destination=destination,
                    days=int(days),
                    budget=float(budget) if budget > 0 else None,
                    preferences=preferences,
                    train_info=train_info,
                    travel_date=travel_date_str,
                )

                st.session_state.trip_plan = trip_plan
                st.session_state.conversation_history = []

            except Exception as e:
                st.error(f"AI规划失败: {e}")
                st.stop()


# ===== 显示旅行计划 =====
if st.session_state.trip_plan:
    _display_trip_plan(st.session_state.trip_plan, is_demo=False)


def _display_trip_plan(plan: TripPlan, is_demo: bool = False):
    """显示旅行计划（抽取为独立函数复用）"""

    st.divider()
    st.markdown(f"## 📍 {plan.title}")

    # Demo模式标记
    if is_demo:
        st.info("🎭 这是示例方案，可供参考。配置API Key生成专属方案！")

    # 概览卡片
    col_sum1, col_sum2, col_sum3 = st.columns(3)

    with col_sum1:
        st.metric("🏔️ 目的地", plan.destination)
    with col_sum2:
        st.metric("📅 旅行天数", f"{plan.days_count}天")
    with col_sum3:
        st.metric("💰 预算", f"¥{plan.budget_breakdown.total:.0f}")

    # 复制行程按钮
    from core.exporter import format_itinerary_for_clipboard
    clipboard_text = format_itinerary_for_clipboard(plan)
    
    # 使用HTML+JS实现复制到剪贴板
    st.markdown(f"""
    <button onclick="navigator.clipboard.writeText(`{clipboard_text.replace('`', '\\`').replace('\n', '\\n')}`).then(() => alert('行程已复制到剪贴板！'));"
        style="
            background: linear-gradient(135deg, #FF6B35, #FF8C42);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
            cursor: pointer;
            margin-top: 8px;
        ">
        📋 复制行程到剪贴板
    </button>
    """, unsafe_allow_html=True)

    # 出行日期和季节信息
    if plan.travel_date:
        col_date, col_season = st.columns(2)
        with col_date:
            st.markdown(f"**📆 出行日期：** {plan.travel_date}")
        if plan.season_info:
            with col_season:
                st.markdown(f"**🌡️ 季节：** {plan.season_info.get('season', '未知')} | {plan.season_info.get('weather', '')}")

    st.markdown(f"**概览：** {plan.summary}")

    # ===== 火车路线卡片 =====
    if plan.train_route:
        st.markdown("### 🚂 推荐火车路线")
        tr = plan.train_route
        with st.container():
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #004E89, #1A936F);
                border-radius: 16px;
                padding: 20px;
                color: white;
                margin: 8px 0;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <h4 style="margin:0; color:white;">🚂 {tr.train_no}次列车</h4>
                        <p style="margin:8px 0 0; opacity:0.9;">{tr.from_station} → {tr.to_station}</p>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:1.5rem; font-weight:bold;">{tr.depart_time} → {tr.arrive_time}</div>
                        <p style="margin:4px 0 0; opacity:0.9;">{tr.duration} | {tr.train_type}</p>
                    </div>
                </div>
                <div style="margin-top:12px; display:flex; gap:16px;">
                    <span style="
                        background: {'rgba(255,255,255,0.2)' if tr.transfers > 0 else 'rgba(26,147,111,0.8)'};
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-size: 0.9rem;
                    ">
                        {'🔄 换乘' + str(tr.transfers) + '次' if tr.transfers > 0 else '🟢 直达'}
                    </span>
                    <span style="background:rgba(255,107,53,0.8); padding:4px 12px; border-radius:12px;">
                        💰 {tr.price_range}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if tr.tips:
                st.info(f"💡 {tr.tips}")

    # ===== 每日行程时间轴 =====
    st.markdown("### 📅 每日行程")

    for day in plan.days:
        with st.expander(f"**Day {day.day_number}** | {day.theme}", expanded=(day.day_number <= 2)):
            # 活动时间轴 - CSS样式
            if day.activities:
                timeline_html = '<div class="timeline" style="padding-left:8px;">'
                for act in day.activities:
                    start_time = act.time.split("-")[0] if "-" in act.time else "09:00"
                    timeline_html += f'''
                    <div class="timeline-item">
                        <div style="
                            background: white;
                            border-radius: 12px;
                            padding: 12px 16px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                            border-left: 3px solid #FF6B35;
                        ">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="
                                    background: linear-gradient(135deg, #FF6B35, #FF8C42);
                                    color: white;
                                    padding: 2px 10px;
                                    border-radius: 10px;
                                    font-size: 0.85rem;
                                ">{act.time}</span>
                                <strong style="color:#004E89;">{act.name}</strong>
                            </div>
                            <p style="margin:8px 0 0; color:#666; font-size:0.9rem;">{act.desc}</p>
                            {f'<p style="margin:4px 0 0; color:#1A936F; font-size:0.85rem;">💡 {act.tip}</p>' if act.tip else ''}
                        </div>
                    </div>
                    '''
                timeline_html += '</div>'
                st.markdown(timeline_html, unsafe_allow_html=True)

            # 展开显示详情
            col_day1, col_day2 = st.columns(2)

            with col_day1:
                if day.food:
                    st.markdown("**🍜 今日美食**")
                    for food in day.food:
                        st.markdown(f"- {food}")

            with col_day2:
                if day.accommodation:
                    st.markdown("**🏨 住宿建议**")
                    st.markdown(day.accommodation)

    # ===== 费用分析 =====
    st.markdown("### 💰 费用预算")

    budget_data = {
        "类别": ["交通", "住宿", "餐饮", "门票"],
        "费用": [
            plan.budget_breakdown.transport,
            plan.budget_breakdown.accommodation,
            plan.budget_breakdown.food,
            plan.budget_breakdown.tickets,
        ],
    }

    # 饼图
    if sum(budget_data["费用"]) > 0:
        fig_pie = px.pie(
            budget_data,
            values="费用",
            names="类别",
            title="费用占比",
            hole=0.4,
            color_discrete_sequence=["#FF6B35", "#004E89", "#1A936F", "#9B59B6"]
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    # 费用明细
    st.markdown("**费用明细**")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.metric("🚂 交通费", f"¥{plan.budget_breakdown.transport:.0f}")
        st.metric("🏨 住宿费", f"¥{plan.budget_breakdown.accommodation:.0f}")
    with col_b2:
        st.metric("🍜 餐饮费", f"¥{plan.budget_breakdown.food:.0f}")
        st.metric("🎫 门票费", f"¥{plan.budget_breakdown.tickets:.0f}")

    st.markdown(f"**💵 总计：¥{plan.budget_breakdown.total:.0f}**")

    # ===== 装备清单 =====
    if plan.packing_list:
        st.markdown("### 🎒 装备清单")
        pack_cols = st.columns(3)
        for i, item in enumerate(plan.packing_list):
            with pack_cols[i % 3]:
                st.checkbox(item, value=True, disabled=True, key=f"pack_{i}")

    # ===== 实用Tips =====
    if plan.tips:
        st.markdown("### 💡 实用Tips")
        tips_html = '<div style="display:flex; flex-direction:column; gap:8px;">'
        for tip in plan.tips:
            tips_html += f'''
            <div style="
                background: linear-gradient(135deg, #1A936F22, #1A936F11);
                border-left: 4px solid #1A936F;
                border-radius: 8px;
                padding: 12px 16px;
            ">{tip}</div>
            '''
        tips_html += '</div>'
        st.markdown(tips_html, unsafe_allow_html=True)

    # ===== 对话式调整（仅在非Demo模式下）=====
    if not is_demo and llm_configured:
        st.divider()
        st.markdown("### 💬 需要调整行程？")

        refine_col1, refine_col2 = st.columns([4, 1])

        with refine_col1:
            user_feedback = st.text_input(
                "说说你的想法",
                placeholder="如：第二天太满了、想加个美食推荐、预算超了怎么办...",
                key="refine_input",
            )

        with refine_col2:
            if st.button("✨ 调整", use_container_width=True):
                if user_feedback and st.session_state.trip_plan:
                    with st.spinner("🤖 正在调整行程..."):
                        try:
                            planner = AIPlanner()
                            refined_plan = planner.refine_plan(
                                current_plan=st.session_state.trip_plan,
                                user_feedback=user_feedback,
                            )
                            st.session_state.trip_plan = refined_plan
                            st.session_state.conversation_history.append({
                                "user": user_feedback,
                                "plan": refined_plan,
                            })
                            st.rerun()
                        except Exception as e:
                            st.error(f"调整失败: {e}")

        # 调整历史
        if st.session_state.conversation_history:
            with st.expander("📜 调整历史"):
                for conv in st.session_state.conversation_history:
                    st.markdown(f"**你：** {conv['user']}")
                    st.markdown(f"**已调整** ✓")


# ===== 未生成计划时的提示 =====
if not st.session_state.trip_plan:
    st.info("👆 在上方输入目的地和天数，点击生成专属旅行方案")

    # 功能说明
    st.markdown("### 🤖 AI旅行规划能做什么？")
    feature_cols = st.columns(3)

    features = [
        ("🚂", "火车路线查询", "自动查找最优火车方案，包含票价和换乘指引"),
        ("📅", "每日行程规划", "根据天数和偏好，合理安排景点和活动"),
        ("🏙️", "多城市联程", "支持成都+九寨沟等格式，一次规划多个城市"),
        ("📆", "日期智能感知", "选择日期后自动提供季节天气和节假日提醒"),
        ("🍜", "当地美食推荐", "结合攻略数据，推荐地道的当地美食"),
        ("💰", "预算明细", "分项估算费用，吃住行一目了然"),
        ("🎒", "装备清单", "根据目的地特点，提供必备物品清单"),
        ("💬", "对话式调整", "随时修改，让计划更贴合需求"),
    ]

    for i, (emoji, title, desc) in enumerate(features):
        with feature_cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card" style="padding:12px;">
                <div style="font-size:1.5rem; margin-bottom:4px;">{emoji}</div>
                <h4 style="margin:0; color:#004E89; font-size:0.95rem;">{title}</h4>
                <p style="color:#666; font-size:0.8rem; margin:4px 0 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ===== LLM配置提示（无API Key时）=====
    if not llm_configured:
        st.divider()
        st.markdown("### 🔑 如何启用AI生成功能？")

        with st.expander("📝 配置指南", expanded=False):
            st.markdown("""
            1. **创建 `.env` 文件**（在项目根目录）
            2. **添加以下配置**：

            ```bash
            # LLM API配置
            LLM_API_KEY=你的API密钥
            LLM_BASE_URL=https://api.deepseek.com
            LLM_MODEL=deepseek-chat
            ```

            3. **支持的LLM服务**：
            - 🌊 **DeepSeek**（推荐）：https://platform.deepseek.com
            - 🤖 **OpenAI**：https://api.openai.com
            - 📊 **智谱AI**：https://open.bigmodel.cn

            4. **重启应用**后即可使用AI生成功能

            ---

            💡 **无需配置也能使用**：Demo预览功能可以查看热门目的地的示例方案！
            """)
