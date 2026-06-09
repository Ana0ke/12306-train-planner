"""
12306省心小助手 - Streamlit 主入口
"""

import streamlit as st
from api.llm_client import check_llm_status


st.set_page_config(
    page_title="12306省心小助手 🚂",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== 侧边栏 =====
with st.sidebar:
    st.title("🚂 12306省心小助手")
    st.caption("一站式火车出行规划 + 旅游攻略")
    st.divider()

    st.markdown("### 📋 功能导航")
    st.markdown("👉 使用顶部标签页切换功能")
    st.divider()

    # 检查AI功能状态
    llm_status = check_llm_status()
    if llm_status["configured"]:
        st.markdown("### 🤖 AI状态")
        st.success("✅ AI规划已启用")
    else:
        st.markdown("### 🤖 AI状态")
        st.warning("⚠️ AI功能待配置")

    st.divider()

    st.markdown("### 🎯 适用人群")
    st.markdown("- 🏔️ 火车旅行爱好者")
    st.markdown("- 🎫 想省心的出行者")
    st.markdown("- 🤖 喜欢AI智能规划的用户")
    st.divider()

    st.caption("⚠️ 数据仅供参考，购票请以12306为准")

# ===== 主页内容 =====
st.title("🚂 12306省心小助手")
st.subheader("让火车出行变得简单又有趣 ✨")

st.divider()

# 功能亮点展示
col_intro1, col_intro2 = st.columns(2)

with col_intro1:
    st.markdown("""
    ### 🎯 我们的目标

    打破旅行规划的信息差！无论是规划一条完美的火车路线，
    还是想找到当地最地道的美食——告诉我你想去哪里，
    剩下的交给我来搞定。

    **"我去拉萨玩5天"** → 火车方案 + 每日行程 + 费用预估 + 装备清单
    """)

with col_intro2:
    st.markdown("""
    ### ✨ 新增AI旅行规划

    🤖 **智能生成**：基于DeepSeek大模型，结合真实火车数据，
    生成专属旅行方案

    💬 **对话调整**：随时修改，"第二天太满了"直接重排

    🎯 **个性化推荐**：根据偏好定制，美食/文化/省钱各有侧重
    """)

st.divider()

# 三大功能模块
st.markdown("### 📌 核心功能")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 🔍 路线规划
    输入出发地+目的地，智能推荐最优方案

    - 💰 最便宜
    - ⚡ 最快速
    - 🔄 最少换乘
    - ⚖️ 性价比最高
    - 🛋️ 最舒适
    """)
    st.markdown("👉 入口：**路线规划**")

with col2:
    st.markdown("""
    ### 🏔️ 热门线路
    8条经典火车旅游线路

    - 🏔️ 青藏线 · 世界屋脊
    - 🌊 沿海线 · 一路看海
    - 🏜️ 丝路线 · 大漠孤烟
    - 🌄 川藏线 · 最美进藏
    - 更多线路持续更新...
    """)
    st.markdown("👉 入口：**热门线路**")

with col3:
    st.markdown("""
    ### 🎫 订票助手
    傻瓜式订票指引

    - 票价图解一看就懂
    - 换乘步骤详细说明
    - 方案适合人群标注
    - 一键跳转12306购票
    """)
    st.markdown("👉 入口：**订票助手**")

with col4:
    st.markdown("""
    ### 🤖 AI旅行规划 ✨
    智能生成专属旅行方案

    - 🚂 结合真实火车数据
    - 📅 每日行程+时间轴
    - 🍜 当地美食推荐
    - 💰 费用预估明细
    - 🎒 装备清单Tips
    """)
    # 检查AI状态
    if llm_status["configured"]:
        st.markdown("👉 入口：**AI旅行规划**")
    else:
        st.markdown("⚠️ 需要配置API密钥")

st.divider()

# 快速查询区
st.markdown("### ⚡ 快速开始")
st.info("👆 点击顶部 **>** 按钮打开页面列表，选择想要的功能")

quick_cols = st.columns(3)
with quick_cols[0]:
    st.markdown("""
    **1️⃣ 想查路线？**
    ```
    路线规划 → 输入"东安东" → "拉萨"
    ```
    """)
with quick_cols[1]:
    st.markdown("""
    **2️⃣ 想看攻略？**
    ```
    热门线路 → 选择"青藏线"
    ```
    """)
with quick_cols[2]:
    st.markdown("""
    **3️⃣ 想AI规划？**
    ```
    AI旅行规划 → 输入"拉萨5天"
    ```
    """)

st.divider()

# 热门线路展示
st.markdown("### 🏔️ 精选线路一览")
route_cols = st.columns(4)
routes_preview = [
    ("🏔️ 青藏线", "西宁→拉萨", "天路之旅"),
    ("🌊 沿海线", "大连→深圳", "一路看海"),
    ("🏜️ 丝路线", "西安→乌鲁木齐", "大漠孤烟"),
    ("🌄 川藏线", "成都→拉萨", "最美进藏"),
    ("🍜 美食线", "成都→昆明", "吃货天堂"),
    ("❄️ 东北线", "哈尔滨→大连", "冰雪奇缘"),
    ("🌿 桂林线", "衡阳→南宁", "山水画卷"),
    ("🌺 云南线", "昆明→香格里拉", "风花雪月"),
]
for i, (name, route, desc) in enumerate(routes_preview):
    with route_cols[i % 4]:
        st.markdown(f"**{name}**")
        st.caption(f"{route}")
        st.text(desc)

st.divider()

# 底部信息
st.markdown("### 📚 项目信息")

info_cols = st.columns(3)
with info_cols[0]:
    st.markdown("""
    **📂 项目结构**

    ```
    app/          Web界面
    core/         核心算法
    api/          数据接口
    data/         城市攻略
    ```
    """)
with info_cols[1]:
    st.markdown("""
    **🛠️ 技术栈**

    - Streamlit（Web框架）
    - DeepSeek/OpenAI（AI模型）
    - Plotly（可视化）
    - Loguru（日志）
    """)
with info_cols[2]:
    st.markdown("""
    **📦 快速安装**

    ```bash
    pip install -r requirements.txt
    streamlit run app/main.py
    ```
    """)

st.divider()
st.caption("Made with ❤️ by Ana0ke | GitHub: Ana0ke/12306-train-planner | 数据仅供参考，购票请以12306官方为准")
