"""
12306省心小助手 - AI旅行规划页面
对话式生成个性化旅行方案
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from api.llm_client import check_llm_status
from core.ai_planner import AIPlanner
from core.planner import RoutePlanner
from core.itinerary import TripPlan


st.set_page_config(page_title="AI旅行规划 🤖", page_icon="🤖", layout="wide")

# ===== 页面状态初始化 =====
if "trip_plan" not in st.session_state:
    st.session_state.trip_plan = None
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "train_route_info" not in st.session_state:
    st.session_state.train_route_info = None


def check_llm_config() -> bool:
    """检查LLM配置状态"""
    status = check_llm_status()
    return status["configured"]


# ===== 页面标题 =====
st.title("🤖 AI旅行规划")
st.caption("告诉我想去哪里、玩几天，我来帮你规划！")

# ===== LLM配置检查 =====
llm_configured = check_llm_config()

if not llm_configured:
    st.warning("⚠️ AI功能暂不可用，需要配置LLM API密钥")
    with st.expander("📝 配置指南", expanded=True):
        st.markdown("""
        ### 如何启用AI旅行规划？

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

        4. **重启应用**后即可使用AI规划功能

        ---

        💡 **不配置也能使用基础功能**：火车路线查询和热门线路功能不受影响。
        """)
    st.stop()


# ===== 输入表单 =====
st.markdown("### 🎯 告诉我你的旅行需求")

with st.form("ai_trip_form"):
    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input(
            "🏔️ 目的地",
            placeholder="如：拉萨、成都、西安...",
            help="输入你想去的目的地城市"
        )

    with col2:
        days = st.number_input(
            "📅 旅行天数",
            min_value=1,
            max_value=15,
            value=5,
            help="计划游玩的天数"
        )

    col3, col4 = st.columns(2)

    with col3:
        budget = st.number_input(
            "💰 预算（元，可选）",
            min_value=0,
            value=3000,
            step=100,
            help="总预算，留空则自动估算"
        )

    with col4:
        from_station = st.text_input(
            "🚂 出发城市（默认东安东）",
            value="东安东",
            help="从哪里出发"
        )

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
    if not destination:
        st.error("请输入目的地！")
    else:
        # 查询火车路线
        with st.spinner("🔍 查询最优火车路线..."):
            try:
                planner = RoutePlanner()
                routes = planner.search(
                    from_station=from_station,
                    to_station=destination,
                    travel_date="2024-01-01",  # 日期不影响路线
                )

                # 如果没有直达，查询换乘
                if not routes:
                    routes = planner.search_with_transfer(
                        from_station=from_station,
                        to_station=destination,
                        travel_date="2024-01-01",
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
                    st.success(f"找到最优路线：{train_info['train_no']} {train_info['depart_time']}→{train_info['arrive_time']}")

            except Exception as e:
                st.warning(f"路线查询失败，将跳过火车信息: {e}")
                train_info = None

        # 调用AI生成行程
        with st.spinner("🤖 AI正在为你规划行程，请稍候..."):
            try:
                planner = AIPlanner()
                trip_plan = planner.plan_trip(
                    destination=destination,
                    days=int(days),
                    budget=float(budget) if budget > 0 else None,
                    preferences=preferences,
                    train_info=train_info,
                )

                st.session_state.trip_plan = trip_plan
                st.session_state.conversation_history = []

            except Exception as e:
                st.error(f"AI规划失败: {e}")
                st.stop()


# ===== 显示旅行计划 =====
if st.session_state.trip_plan:
    plan: TripPlan = st.session_state.trip_plan

    st.divider()
    st.markdown(f"## 📍 {plan.title}")

    # 概览
    col_sum1, col_sum2, col_sum3 = st.columns(3)

    with col_sum1:
        st.metric("🏔️ 目的地", plan.destination)
    with col_sum2:
        st.metric("📅 旅行天数", f"{plan.days_count}天")
    with col_sum3:
        st.metric("💰 预算", f"¥{plan.budget_breakdown.total:.0f}")

    st.markdown(f"**概览：** {plan.summary}")

    # ===== 火车路线卡片 =====
    if plan.train_route:
        st.markdown("### 🚂 推荐火车路线")
        tr = plan.train_route
        with st.container():
            col_tr1, col_tr2 = st.columns([3, 1])
            with col_tr1:
                st.markdown(f"""
                **{tr.train_no}次列车** | {tr.from_station} → {tr.to_station}

                ⏰ **{tr.depart_time}** 出发 → **{tr.arrive_time}** 到达
                🕐 历时：{tr.duration} | {tr.train_type}
                {"🔄 换乘" + str(tr.transfers) + "次" if tr.transfers > 0 else "🟢 直达"}
                """)
            with col_tr2:
                st.markdown(f"""
                **票价参考**
                {tr.price_range}
                """)
            if tr.tips:
                st.info(f"💡 {tr.tips}")

    # ===== 每日行程时间轴 =====
    st.markdown("### 📅 每日行程")

    for day in plan.days:
        with st.expander(f"**Day {day.day_number}** | {day.theme}", expanded=(day.day_number <= 2)):
            # 活动时间轴
            if day.activities:
                timeline_data = []
                for act in day.activities:
                    start_time = act.time.split("-")[0] if "-" in act.time else "09:00"
                    timeline_data.append({
                        "时间": start_time,
                        "活动": act.name,
                        "详情": act.desc[:50] + "..." if len(act.desc) > 50 else act.desc,
                        "提示": act.tip,
                    })

                if timeline_data:
                    st.table(timeline_data)

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
        for tip in plan.tips:
            st.markdown(f"- {tip}")

    # ===== 对话式调整 =====
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

else:
    # 未生成计划时的提示
    st.info("👆 在上方输入目的地和天数，点击生成专属旅行方案")

    # 功能说明
    st.markdown("### 🤖 AI旅行规划能做什么？")
    feature_cols = st.columns(3)

    features = [
        ("🚂", "火车路线查询", "自动查找最优火车方案，包含票价和换乘指引"),
        ("📅", "每日行程规划", "根据天数和偏好，合理安排景点和活动"),
        ("🍜", "当地美食推荐", "结合攻略数据，推荐地道的当地美食"),
        ("💰", "预算明细", "分项估算费用，吃住行一目了然"),
        ("🎒", "装备清单", "根据目的地特点，提供必备物品清单"),
        ("💬", "对话式调整", "随时修改，让计划更贴合需求"),
    ]

    for i, (emoji, title, desc) in enumerate(features):
        with feature_cols[i % 3]:
            st.markdown(f"{emoji} **{title}**")
            st.caption(desc)
