"""
12306省心小助手 - 订票助手页面
"""

import streamlit as st

st.set_page_config(page_title="订票助手 🎫", page_icon="🎫", layout="wide")

st.title("🎫 订票助手")
st.caption("傻瓜式订票指引，让你轻松搞懂火车票")

# ===== 票种图解 =====
st.markdown("### 🎫 票种图解 — 一看就懂")

ticket_types = [
    {
        "name": "硬座",
        "emoji": "🪑",
        "price": "最便宜",
        "comfort": "⭐⭐",
        "desc": "普通座椅，可调靠背。短途(4h内)没问题，长途比较辛苦",
        "suitable": "学生党、短途出行",
        "tip": "💡 夜车超过8小时不建议选硬座，很难睡着",
    },
    {
        "name": "硬卧",
        "emoji": "🛏️",
        "price": "中等",
        "comfort": "⭐⭐⭐",
        "desc": "6人包厢(上/中/下铺)，有被褥枕头。可以躺着休息",
        "suitable": "长途夜车首选",
        "tip": "💡 下铺最方便但最抢手，上铺空间小但最安静",
    },
    {
        "name": "软卧",
        "emoji": "🛌",
        "price": "较贵",
        "comfort": "⭐⭐⭐⭐",
        "desc": "4人包厢(上下铺)，空间更大更安静，有门可关",
        "suitable": "家庭出行、商务出差",
        "tip": "💡 软卧性价比高，比飞机便宜但舒适度接近",
    },
    {
        "name": "二等座",
        "emoji": "💺",
        "price": "中等",
        "comfort": "⭐⭐⭐",
        "desc": "高铁/动车标准座位，5人一排(2+3)，可调座椅",
        "suitable": "高铁出行默认选择",
        "tip": "💡 靠窗座位A/F，靠走廊座位C/D，选座时注意",
    },
    {
        "name": "一等座",
        "emoji": "👑",
        "price": "较贵",
        "comfort": "⭐⭐⭐⭐",
        "desc": "4人一排(2+2)，座椅更宽更大，有脚踏板",
        "suitable": "3-5小时高铁舒适出行",
        "tip": "💡 一等座和二等座差价不大时很值得升",
    },
    {
        "name": "商务座",
        "emoji": "🏆",
        "price": "最贵",
        "comfort": "⭐⭐⭐⭐⭐",
        "desc": "可平躺座椅，3人一排(1+2)，有餐食和独立候车室",
        "suitable": "商务出行、特殊需求",
        "tip": "💡 有时商务座和飞机票价差不多，看情况选",
    },
]

for ticket in ticket_types:
    with st.expander(f"{ticket['emoji']} {ticket['name']} — {ticket['price']} | 舒适度 {ticket['comfort']}"):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**说明：** {ticket['desc']}")
            st.markdown(f"**适合：** {ticket['suitable']}")
        with col2:
            st.info(ticket["tip"])

st.divider()

# ===== 换乘指南 =====
st.markdown("### 🔄 换乘指南 — 不迷路")

st.markdown("""
**同站换乘（最方便）**
- 下车后看站内「便捷换乘」标识
- 不出站，走换乘通道直接到候车厅
- 一般预留 **15-20分钟** 即可

**异站换乘（需注意）**
- 需要出站再进站，预留 **40-60分钟**
- 提前查好两个站的距离和交通方式
- 大城市站间距可能很远（如广州南→广州东需30分钟地铁）
""")

col_tips1, col_tips2 = st.columns(2)
with col_tips1:
    st.markdown("#### ✅ 换乘小贴士")
    st.markdown("""
    - 买票时确认是否**同站换乘**
    - 第一程尽量选到达时间有余量的
    - 大站换乘更方便（车次多、设施全）
    - 12306购票时选「接续换乘」可自动匹配
    """)
with col_tips2:
    st.markdown("#### ❌ 常见错误")
    st.markdown("""
    - 换乘时间留太短（低于15分钟风险大）
    - 以为同站结果异站（如北京/北京西）
    - 没看清楚车次出发站
    - 忘记取纸质票（部分小站需要）
    """)

st.divider()

# ===== 购票流程 =====
st.markdown("### 📱 12306购票步骤")

steps = [
    ("1️⃣", "下载12306 App", "应用商店搜索「铁路12306」"),
    ("2️⃣", "注册/登录账号", "需要身份证实名认证"),
    ("3️⃣", "添加乘车人", "输入姓名和身份证号"),
    ("4️⃣", "查询车次", "输入出发地、目的地、日期"),
    ("5️⃣", "选择车次和座位", "根据需求和预算选择"),
    ("6️⃣", "提交订单并支付", "支持支付宝、微信、银行卡"),
    ("7️⃣", "出发前取票/刷证进站", "高铁可刷身份证，普速需取票"),
]

for i, (num, title, desc) in enumerate(steps):
    col_num, col_step = st.columns([1, 9])
    with col_num:
        st.markdown(f"## {num}")
    with col_step:
        st.markdown(f"**{title}**")
        st.caption(desc)
    if i < len(steps) - 1:
        st.markdown("↓")

st.divider()
st.info("⚠️ 购票请以12306官方App为准，本页面仅供参考指引")
