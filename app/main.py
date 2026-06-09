"""
12306省心小助手 - Streamlit 主入口
"""

import os
import sys
from pathlib import Path

# ===== 路径修复：确保项目根目录在 sys.path 中 =====
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st

# ===== Streamlit Cloud 兼容：优先从 secrets.toml 读取配置 =====
def _load_secrets():
    """从 Streamlit secrets 加载环境变量"""
    try:
        secrets = st.secrets
        for key in ["LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL", "DEMO_MODE"]:
            if key in secrets and key not in os.environ:
                os.environ[key] = str(secrets[key])
    except Exception:
        pass

_load_secrets()

from api.llm_client import check_llm_status


st.set_page_config(
    page_title="12306省心小助手 🚂",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ===== 注入全局样式 =====
from components.styles import inject_styles
inject_styles()


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
        st.warning("⚠️ 体验模式（AI功能待配置）")
        st.caption("💡 仍可使用路线查询和热门方案体验")

    st.divider()

    st.markdown("### 🎯 适用人群")
    st.markdown("- 🏔️ 火车旅行爱好者")
    st.markdown("- 🎫 想省心的出行者")
    st.markdown("- 🤖 喜欢AI智能规划的用户")
    st.divider()

    st.caption("⚠️ 数据仅供参考，购票请以12306为准")


# ===== 主页内容 =====

# Hero区域
st.markdown("""
<div style="
    background: linear-gradient(135deg, #004E89, #1A936F);
    border-radius: 20px;
    padding: 32px 24px;
    margin: 16px 0;
    color: white;
    text-align: center;
">
    <h1 style="color:white; margin:0; font-size:1.8rem;">🚂 12306省心小助手</h1>
    <p style="color:rgba(255,255,255,0.9); margin:12px 0 0; font-size:1.1rem;">
        让每一次出行都省心 · 火车路线规划 + AI旅行攻略
    </p>
</div>
""", unsafe_allow_html=True)


# ===== 核心功能卡片 =====
st.markdown("### ✨ 核心功能")

card_cols = st.columns(4)

feature_cards = [
    ("🔍", "路线规划", "智能推荐最优方案", "#FF6B35"),
    ("🏔️", "热门线路", "8条经典火车旅游线", "#004E89"),
    ("🎫", "订票助手", "傻瓜式订票指引", "#1A936F"),
    ("🤖", "AI旅行规划", "智能生成专属方案", "#9B59B6"),
]

for i, (emoji, title, desc, color) in enumerate(feature_cards):
    with card_cols[i]:
        st.markdown(f"""
        <div class="feature-card" style="text-align:center; height:100%;">
            <div style="font-size:2.2rem; margin-bottom:8px;">{emoji}</div>
            <h3 style="margin:0; color:{color};">{title}</h3>
            <p style="color:#666; font-size:0.9rem; margin-top:8px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)


st.divider()


# ===== 功能详情展示 =====
tab1, tab2 = st.tabs(["📖 功能介绍", "🏔️ 精选线路"])

with tab1:
    col_intro1, col_intro2 = st.columns(2)
    
    with col_intro1:
        st.markdown("""
        <div class="feature-card">
        ### 🎯 我们的目标
        
        打破旅行规划的信息差！无论是规划一条完美的火车路线，
        还是想找到当地最地道的美食——告诉我你想去哪里，
        剩下的交给我来搞定。
        
        **"我去拉萨玩5天"** → 火车方案 + 每日行程 + 费用预估 + 装备清单
        </div>
        """, unsafe_allow_html=True)
    
    with col_intro2:
        st.markdown("""
        <div class="feature-card">
        ### 🤖 新增AI旅行规划
        
        - **智能生成**：基于DeepSeek大模型，结合真实火车数据
        - **对话调整**：随时修改，"第二天太满了"直接重排
        - **个性化推荐**：根据偏好定制，美食/文化/省钱各有侧重
        - **体验模式**：无需API Key，也能预览热门方案
        </div>
        """, unsafe_allow_html=True)
    
    # 三大功能模块
    st.markdown("### 📌 功能模块")
    
    func_cols = st.columns(3)
    
    func_data = [
        ("🔍 路线规划", [
            "💰 最便宜",
            "⚡ 最快速", 
            "🔄 最少换乘",
            "⚖️ 性价比最高",
            "🛋️ 最舒适",
        ], "输入出发地+目的地，智能推荐最优方案"),
        ("🏔️ 热门线路", [
            "🏔️ 青藏线 · 世界屋脊",
            "🌊 沿海线 · 一路看海",
            "🏜️ 丝路线 · 大漠孤烟",
            "🌄 川藏线 · 最美进藏",
            "🍜 美食线 · 吃货天堂",
        ], "8条经典火车旅游线路"),
        ("🎫 订票助手", [
            "票价图解一看就懂",
            "换乘步骤详细说明",
            "方案适合人群标注",
            "一键跳转12306购票",
        ], "傻瓜式订票指引"),
    ]
    
    for i, (title, items, desc) in enumerate(func_data):
        with func_cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <h4 style="color:#004E89; margin:0 0 12px;">{title}</h4>
                <p style="color:#666; font-size:0.9rem; margin-bottom:12px;">{desc}</p>
                <ul style="color:#333; font-size:0.9rem; padding-left:16px; margin:0;">
                    {''.join([f'<li style="margin:4px 0;">{item}</li>' for item in items])}
                </ul>
            </div>
            """, unsafe_allow_html=True)


with tab2:
    # 热门线路展示 - 卡片式
    st.markdown("### 🏔️ 精选线路一览")
    route_cols = st.columns(4)
    
    routes_preview = [
        ("🏔️ 青藏线", "西宁→拉萨", "天路之旅", "蓝白渐变"),
        ("🌊 沿海线", "大连→深圳", "一路看海", "蓝绿渐变"),
        ("🏜️ 丝路线", "西安→乌鲁木齐", "大漠孤烟", "橙黄渐变"),
        ("🌄 川藏线", "成都→拉萨", "最美进藏", "绿白渐变"),
        ("🍜 美食线", "成都→昆明", "吃货天堂", "红橙渐变"),
        ("❄️ 东北线", "哈尔滨→大连", "冰雪奇缘", "蓝紫渐变"),
        ("🌿 桂林线", "衡阳→南宁", "山水画卷", "绿青渐变"),
        ("🌺 云南线", "昆明→香格里拉", "风花雪月", "粉紫渐变"),
    ]
    
    for i, (name, route, desc, _) in enumerate(routes_preview):
        with route_cols[i % 4]:
            st.markdown(f"""
            <div class="feature-card" style="text-align:center; cursor:pointer;">
                <div style="font-size:1.8rem; margin-bottom:8px;">{name.split()[0]}</div>
                <h4 style="margin:0; color:#004E89;">{name.split()[1]}</h4>
                <p style="color:#666; font-size:0.85rem; margin:4px 0;">{route}</p>
                <span style="
                    display:inline-block;
                    background: linear-gradient(135deg, #FF6B35, #FF8C42);
                    color: white;
                    border-radius: 12px;
                    padding: 4px 12px;
                    font-size: 0.8rem;
                ">{desc}</span>
            </div>
            """, unsafe_allow_html=True)


st.divider()


# ===== 快速开始 =====
st.markdown("### ⚡ 快速开始")
quick_cols = st.columns(3)

quick_steps = [
    ("1️⃣", "想查路线？", "路线规划 → 输入出发地 → 目的地", "#FF6B35"),
    ("2️⃣", "想看攻略？", "热门线路 → 选择线路", "#004E89"),
    ("3️⃣", "想AI规划？", "AI旅行规划 → 输入目的地", "#1A936F"),
]

for i, (num, title, desc, color) in enumerate(quick_steps):
    with quick_cols[i]:
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border-left: 4px solid {color};
        ">
            <div style="font-size:1.8rem; margin-bottom:8px;">{num}</div>
            <h4 style="margin:0; color:{color};">{title}</h4>
            <p style="color:#666; font-size:0.9rem; margin-top:8px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)


st.divider()


# ===== 项目信息 =====
st.markdown("### 📚 项目信息")

info_cols = st.columns(3)

with info_cols[0]:
    st.markdown("""
    **📂 项目结构**
    - `app/` — Web界面
    - `core/` — 核心算法
    - `api/` — 数据接口
    - `data/` — 城市攻略
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
