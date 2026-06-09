"""
12306省心小助手 - 订票助手页面
"""

import streamlit as st

st.set_page_config(page_title="订票助手 🎫", page_icon="🎫", layout="wide")

# ===== 路径修复 + 注入全局样式 =====
import sys
from pathlib import Path
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
from components.styles import inject_styles
inject_styles()

st.title("🎫 订票助手")
st.markdown('<p style="color:#666;">傻瓜式订票指引，让你轻松搞懂火车票</p>', unsafe_allow_html=True)

# ===== 票种图解 =====
st.markdown("### 🎫 票种图解")

ticket_types = [
    {
        "name": "硬座",
        "emoji": "🪑",
        "price": "最便宜",
        "comfort": 2,
        "desc": "普通座椅，可调靠背。短途(4h内)没问题，长途比较辛苦",
        "suitable": "学生党、短途出行",
        "tip": "💡 夜车超过8小时不建议选硬座，很难睡着",
        "color": "#888888",
    },
    {
        "name": "硬卧",
        "emoji": "🛏️",
        "price": "中等",
        "comfort": 3,
        "desc": "6人包厢(上/中/下铺)，有被褥枕头。可以躺着休息",
        "suitable": "长途夜车首选",
        "tip": "💡 下铺最方便但最抢手，上铺空间小但最安静",
        "color": "#4A90D9",
    },
    {
        "name": "软卧",
        "emoji": "🛌",
        "price": "较贵",
        "comfort": 4,
        "desc": "4人包厢(上下铺)，空间更大更安静，有门可关",
        "suitable": "家庭出行、商务出差",
        "tip": "💡 软卧性价比高，比飞机便宜但舒适度接近",
        "color": "#1A936F",
    },
    {
        "name": "二等座",
        "emoji": "💺",
        "price": "中等",
        "comfort": 3,
        "desc": "高铁/动车标准座位，5人一排(2+3)，可调座椅",
        "suitable": "高铁出行默认选择",
        "tip": "💡 靠窗座位A/F，靠走廊座位C/D，选座时注意",
        "color": "#FF6B35",
    },
    {
        "name": "一等座",
        "emoji": "👑",
        "price": "较贵",
        "comfort": 4,
        "desc": "4人一排(2+2)，座椅更宽更大，有脚踏板",
        "suitable": "3-5小时高铁舒适出行",
        "tip": "💡 一等座和二等座差价不大时很值得升",
        "color": "#9B59B6",
    },
    {
        "name": "商务座",
        "emoji": "🏆",
        "price": "最贵",
        "comfort": 5,
        "desc": "可平躺座椅，3人一排(1+2)，有餐食和独立候车室",
        "suitable": "商务出行、特殊需求",
        "tip": "💡 有时商务座和飞机票价差不多，看情况选",
        "color": "linear-gradient(135deg, #FFD700, #FFA500)",
    },
]

for ticket in ticket_types:
    with st.expander(f"{ticket['emoji']} {ticket['name']} — {ticket['price']}"):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**说明：** {ticket['desc']}")
            st.markdown(f"**适合：** {ticket['suitable']}")
            
            # 舒适度进度条
            st.markdown(f"**舒适度：**")
            comfort_html = f'''
            <div style="
                background: #E8E8E8;
                border-radius: 4px;
                height: 10px;
                overflow: hidden;
                margin-top: 4px;
            ">
                <div style="
                    {('background: ' + ticket['color'] + ';' if not ticket['color'].startswith('linear') else 'background: ' + ticket['color'] + ';')}
                    height: 100%;
                    width: {ticket['comfort'] * 20}%;
                    border-radius: 4px;
                    transition: width 0.5s ease;
                "></div>
            </div>
            <div style="display:flex; justify-content:space-between; color:#666; font-size:0.8rem; margin-top:4px;">
                <span>基础</span>
                <span>⭐{'⭐' * ticket['comfort']}</span>
                <span>豪华</span>
            </div>
            '''
            st.markdown(comfort_html, unsafe_allow_html=True)
            
        with col2:
            st.info(ticket["tip"])

st.divider()

# ===== 换乘指南 =====
st.markdown("### 🔄 换乘指南")

# 换乘步骤卡片
transfer_cols = st.columns(2)

with transfer_cols[0]:
    st.markdown("""
    <div class="feature-card" style="border-left:4px solid #1A936F;">
    <h4 style="color:#1A936F; margin:0 0 12px;">✅ 同站换乘（最方便）</h4>
    <ul style="color:#333; font-size:0.9rem; padding-left:16px; margin:0;">
        <li style="margin:8px 0;">下车后看站内「便捷换乘」标识</li>
        <li style="margin:8px 0;">不出站，走换乘通道直接到候车厅</li>
        <li style="margin:8px 0;">一般预留 <strong>15-20分钟</strong> 即可</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with transfer_cols[1]:
    st.markdown("""
    <div class="feature-card" style="border-left:4px solid #FF6B35;">
    <h4 style="color:#FF6B35; margin:0 0 12px;">⚠️ 异站换乘（需注意）</h4>
    <ul style="color:#333; font-size:0.9rem; padding-left:16px; margin:0;">
        <li style="margin:8px 0;">需要出站再进站，预留 <strong>40-60分钟</strong></li>
        <li style="margin:8px 0;">提前查好两个站的距离和交通方式</li>
        <li style="margin:8px 0;">大城市站间距可能很远</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 换乘小贴士
col_tips1, col_tips2 = st.columns(2)
with col_tips1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1A936F22, #1A936F11);
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #1A936F;
    ">
        <h4 style="color:#1A936F; margin:0 0 12px;">✅ 换乘小贴士</h4>
        <ul style="color:#333; font-size:0.9rem; padding-left:16px; margin:0;">
            <li style="margin:6px 0;">买票时确认是否<strong>同站换乘</strong></li>
            <li style="margin:6px 0;">第一程尽量选到达时间有余量的</li>
            <li style="margin:6px 0;">大站换乘更方便（车次多、设施全）</li>
            <li style="margin:6px 0;">12306购票时选「接续换乘」可自动匹配</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_tips2:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF4B4B22, #FF4B4B11);
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #FF4B4B;
    ">
        <h4 style="color:#FF4B4B; margin:0 0 12px;">❌ 常见错误</h4>
        <ul style="color:#333; font-size:0.9rem; padding-left:16px; margin:0;">
            <li style="margin:6px 0;">换乘时间留太短（低于15分钟风险大）</li>
            <li style="margin:6px 0;">以为同站结果异站（如北京/北京西）</li>
            <li style="margin:6px 0;">没看清楚车次出发站</li>
            <li style="margin:6px 0;">忘记取纸质票（部分小站需要）</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

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

# 步骤卡片展示
for i, (num, title, desc) in enumerate(steps):
    col_num, col_step = st.columns([1, 11])
    with col_num:
        st.markdown(f"""
        <div style="
            display:inline-flex;
            align-items:center;
            justify-content:center;
            width:40px;
            height:40px;
            background: linear-gradient(135deg, #FF6B35, #FF8C42);
            color: white;
            border-radius: 50%;
            font-size:1.2rem;
            font-weight:bold;
        ">{num[:1]}</div>
        """, unsafe_allow_html=True)
    with col_step:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 12px 16px;
            margin:-8px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-left: 3px solid #FF6B35;
        ">
            <strong style="color:#004E89;">{title}</strong>
            <span style="color:#666; font-size:0.9rem; margin-left:8px;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)
    
    if i < len(steps) - 1:
        st.markdown("<div style='margin-left:18px; border-left:2px dashed #ddd; height:16px;'></div>", unsafe_allow_html=True)

st.divider()
st.info("⚠️ 购票请以12306官方App为准，本页面仅供参考指引")
