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
    st.caption("让每一次出行都省心")
    st.divider()

    # 检查AI功能状态
    llm_status = check_llm_status()
    if llm_status["configured"]:
        st.success("✅ AI规划已启用")
    else:
        st.warning("⚠️ 体验模式（AI功能待配置）")

    st.divider()
    st.markdown("### 📚 功能导航")
    st.markdown("使用顶部标签页切换功能")
    st.divider()
    st.caption("⚠️ 数据仅供参考，购票请以12306为准")


# ===== 主页内容 =====
# 简洁的一句话说说明
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
        火车路线规划 + AI旅行攻略，让每一次出行都省心
    </p>
</div>
""", unsafe_allow_html=True)

# 直接指向核心功能
st.markdown("""
<div style="
    background: white;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    margin: 24px 0;
">
    <h2 style="color:#333; margin:0 0 16px;">🚀 开始规划你的行程</h2>
    <p style="color:#666; margin:0 0 20px;">
        选择上方标签页：<strong>🔍路线规划</strong>、<strong>🏔️热门线路</strong>、<strong>🤖AI规划</strong>
    </p>
    <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
        <a href="1_🔍_路线规划" style="
            display:inline-block;
            background: linear-gradient(135deg, #FF6B35, #FF8C42);
            color: white;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: bold;
        ">🔍 路线规划</a>
        <a href="4_🤖_AI旅行规划" style="
            display:inline-block;
            background: linear-gradient(135deg, #9B59B6, #8E44AD);
            color: white;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: bold;
        ">🤖 AI旅行规划</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# 简洁的功能说明
st.markdown("### ✨ 核心功能")
feature_cols = st.columns(4)

feature_cards = [
    ("🔍", "路线规划", "智能推荐最优方案"),
    ("🏔️", "热门线路", "8条经典火车旅游线"),
    ("🎫", "订票助手", "傻瓜式订票指引"),
    ("🤖", "AI规划", "智能生成专属方案"),
]

for i, (emoji, title, desc) in enumerate(feature_cards):
    with feature_cols[i]:
        st.markdown(f"""
        <div class="feature-card" style="text-align:center;">
            <div style="font-size:2rem; margin-bottom:8px;">{emoji}</div>
            <h3 style="margin:0; color:#004E89;">{title}</h3>
            <p style="color:#666; font-size:0.85rem; margin-top:4px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# 热门线路预览
st.markdown("### 🏔️ 热门线路预览")

route_cols = st.columns(4)
routes_preview = [
    ("🏔️ 青藏线", "西宁→拉萨", "天路之旅"),
    ("🌊 沿海线", "大连→深圳", "一路看海"),
    ("🏜️ 丝路线", "西安→乌鲁木齐", "大漠孤烟"),
    ("🌄 川藏线", "成都→拉萨", "最美进藏"),
]

for i, (name, route, desc) in enumerate(routes_preview):
    with route_cols[i]:
        st.markdown(f"""
        <div class="feature-card" style="text-align:center;">
            <h4 style="margin:0; color:#004E89;">{name}</h4>
            <p style="color:#666; font-size:0.85rem; margin:4px 0;">{route}</p>
            <span style="
                display:inline-block;
                background: #1A936F22;
                color: #1A936F;
                border-radius: 12px;
                padding: 4px 10px;
                font-size: 0.8rem;
            ">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#666;'>前往 <strong>热门线路</strong> 标签页查看全部8条精选路线</p>", unsafe_allow_html=True)

st.divider()

# 项目信息（保持简洁）
st.caption("Made with ❤️ by Ana0ke | GitHub: Ana0ke/12306-train-planner | 数据仅供参考，购票请以12306官方为准")
