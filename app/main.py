"""
12306省心小助手 - Streamlit 主入口
"""

import streamlit as st

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

    st.markdown("### 🎯 适用人群")
    st.markdown("- 🏔️ 火车旅行爱好者")
    st.markdown("- 🎫 想省心的出行者")
    st.divider()

    st.caption("⚠️ 数据仅供参考，购票请以12306为准")

# ===== 主页内容 =====
st.title("🚂 12306省心小助手")
st.subheader("让火车出行变得简单又有趣")

st.divider()

col1, col2, col3 = st.columns(3)

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

with col2:
    st.markdown("""
    ### 🏔️ 热门线路
    8条经典火车旅游线路

    - 青藏线 · 世界屋脊
    - 沿海线 · 一路看海
    - 丝路线 · 大漠孤烟
    - 川藏线 · 最美进藏
    - 更多线路持续更新...
    """)

with col3:
    st.markdown("""
    ### 🎫 订票助手
    傻瓜式订票指引

    - 票价图解一看就懂
    - 换乘步骤详细说明
    - 方案适合人群标注
    - 一键跳转12306购票
    """)

st.divider()

# 快速查询区
st.markdown("### ⚡ 快速查询")
st.info("👆 点击顶部标签页开始使用，推荐先试试「路线规划」或「热门线路」")

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
st.caption("Made with ❤️ by Ana0ke | 数据仅供参考，购票请以12306官方为准")
