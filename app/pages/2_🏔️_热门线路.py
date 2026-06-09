"""
12306省心小助手 - 热门线路页面
"""

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="热门线路 🏔️", page_icon="🏔️", layout="wide")

# ===== 路径修复 + 注入全局样式 =====
import sys
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
from components.styles import inject_styles
inject_styles()

st.title("🏔️ 热门旅游线路")
st.caption("8条经典火车旅游线路，每条都有沿途攻略和乘车指南")

# 加载线路数据
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "routes"

# 线路渐变色配置
ROUTE_GRADIENTS = {
    "qingzang": "background: linear-gradient(135deg, #4A90D9, #FFFFFF);",
    "coastal": "background: linear-gradient(135deg, #4A90D9, #1A936F);",
    "silkroad": "background: linear-gradient(135deg, #FF6B35, #FFD700);",
    "chuanzang": "background: linear-gradient(135deg, #1A936F, #FFFFFF);",
    "food": "background: linear-gradient(135deg, #FF4B4B, #FF6B35);",
    "dongbei": "background: linear-gradient(135deg, #4A90D9, #9B59B6);",
    "guilin": "background: linear-gradient(135deg, #1A936F, #00CED1);",
    "yunnan": "background: linear-gradient(135deg, #FF69B4, #9B59B6);",
}

ROUTES_INDEX = [
    {
        "id": "qingzang",
        "name": "🏔️ 青藏线",
        "subtitle": "世界屋脊天路",
        "route": "西宁 → 格尔木 → 那曲 → 拉萨",
        "duration": "约21小时",
        "best_season": "6月-10月",
        "highlights": "可可西里、唐古拉山、纳木错、布达拉宫",
        "color": "🏔️",
    },
    {
        "id": "coastal",
        "name": "🌊 沿海线",
        "subtitle": "一路看海",
        "route": "大连 → 青岛 → 上海 → 厦门 → 深圳",
        "duration": "约18小时（分段）",
        "best_season": "4月-10月",
        "highlights": "渤海湾、黄海、东海、南海，一路看尽中国海岸线",
        "color": "🌊",
    },
    {
        "id": "silkroad",
        "name": "🏜️ 丝路线",
        "subtitle": "大漠孤烟",
        "route": "西安 → 兰州 → 敦煌 → 乌鲁木齐",
        "duration": "约24小时（分段）",
        "best_season": "5月-10月",
        "highlights": "兵马俑、莫高窟、鸣沙山、天山天池",
        "color": "🏜️",
    },
    {
        "id": "chuanzang",
        "name": "🌄 川藏线",
        "subtitle": "最美进藏路",
        "route": "成都 → 雅安 → 康定 → 拉萨",
        "duration": "约36小时（分段）",
        "best_season": "5月-10月",
        "highlights": "贡嘎雪山、然乌湖、米堆冰川、林芝桃花",
        "color": "🌄",
    },
    {
        "id": "food",
        "name": "🍜 美食线",
        "subtitle": "吃货天堂",
        "route": "成都 → 重庆 → 贵阳 → 昆明",
        "duration": "约10小时（分段）",
        "best_season": "全年",
        "highlights": "火锅、酸汤鱼、过桥米线、小面、串串",
        "color": "🍜",
    },
    {
        "id": "dongbei",
        "name": "❄️ 东北线",
        "subtitle": "冰雪奇缘",
        "route": "哈尔滨 → 长春 → 沈阳 → 大连",
        "duration": "约6小时（分段）",
        "best_season": "12月-2月（冰雪）/ 7月-8月（避暑）",
        "highlights": "冰雕、雾凇、长白山、星海广场",
        "color": "❄️",
    },
    {
        "id": "guilin",
        "name": "🌿 桂林线",
        "subtitle": "山水画卷",
        "route": "衡阳 → 桂林 → 柳州 → 南宁",
        "duration": "约6小时（分段）",
        "best_season": "4月-10月",
        "highlights": "漓江、象鼻山、龙脊梯田、德天瀑布",
        "color": "🌿",
    },
    {
        "id": "yunnan",
        "name": "🌺 云南线",
        "subtitle": "风花雪月",
        "route": "昆明 → 大理 → 丽江 → 香格里拉",
        "duration": "约8小时（分段）",
        "best_season": "3月-10月",
        "highlights": "洱海、玉龙雪山、虎跳峡、松赞林寺",
        "color": "🌺",
    },
]

# 线路卡片展示 - 带渐变条
cols = st.columns(2)
for i, route in enumerate(ROUTES_INDEX):
    with cols[i % 2]:
        gradient_style = ROUTE_GRADIENTS.get(route["id"], "background: linear-gradient(135deg, #FF6B35, #FF8C42);")
        
        with st.container():
            st.markdown(f"""
            <div style="
                background: white;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 2px 12px rgba(0,0,0,0.06);
                border: 1px solid rgba(0,0,0,0.04);
            ">
                <div style="{gradient_style}; height: 8px;"></div>
                <div style="padding: 16px;">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <div>
                            <h3 style="margin:0; color:#004E89;">{route['name']}</h3>
                            <p style="margin:4px 0 0; color:#666; font-size:0.9rem;">{route['subtitle']}</p>
                        </div>
                        <span style="
                            display:inline-block;
                            background: linear-gradient(135deg, #FF6B35, #FF8C42);
                            color: white;
                            border-radius: 12px;
                            padding: 4px 12px;
                            font-size: 0.8rem;
                        ">{route['duration']}</span>
                    </div>
                    <hr style="margin:12px 0; border:none; height:1px; background:#f0f0f0;">
                    <p style="margin:0 0 8px; color:#333; font-size:0.9rem;">
                        <strong>📍 路线：</strong>{route['route']}
                    </p>
                    <p style="margin:0 0 8px; color:#333; font-size:0.9rem;">
                        <strong>🗓️ 最佳季节：</strong>{route['best_season']}
                    </p>
                    <p style="margin:0; color:#666; font-size:0.85rem;">
                        <strong>✨ 亮点：</strong>{route['highlights']}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 查看详情按钮
            if st.button(f"📖 查看攻略 - {route['name'].split()[1]}", key=f"detail_{route['id']}", use_container_width=True):
                st.session_state["selected_route"] = route["id"]
                st.rerun()

# ===== 线路详情 =====
if "selected_route" in st.session_state:
    route_id = st.session_state["selected_route"]
    route_info = next((r for r in ROUTES_INDEX if r["id"] == route_id), None)

    if route_info:
        st.divider()
        
        # 详情页头部
        gradient_style = ROUTE_GRADIENTS.get(route_id, "background: linear-gradient(135deg, #FF6B35, #FF8C42);")
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            margin-bottom: 16px;
        ">
            <div style="{gradient_style}; height: 12px;"></div>
            <div style="padding: 24px; text-align:center;">
                <h2 style="margin:0; color:#004E89;">{route_info['name']} · {route_info['subtitle']}</h2>
                <p style="margin:8px 0 0; color:#666;">{route_info['route']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 加载详细数据
        detail_file = DATA_DIR / f"{route_id}.json"
        if detail_file.exists():
            with open(detail_file, "r", encoding="utf-8") as f:
                detail = json.load(f)

            # 沿途站点卡片
            st.markdown("### 🚉 沿途站点")
            stations_html = '<div style="display:flex; flex-wrap:wrap; gap:8px;">'
            for station in detail.get("stations", []):
                stations_html += f'''
                <div style="
                    background: white;
                    border-radius: 12px;
                    padding: 12px 16px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    border-left: 3px solid #FF6B35;
                ">
                    <strong style="color:#004E89;">{station['name']}</strong>
                    <p style="margin:4px 0 0; color:#666; font-size:0.85rem;">{station.get('desc', '')}</p>
                </div>
                '''
            stations_html += '</div>'
            st.markdown(stations_html, unsafe_allow_html=True)

            # 攻略信息
            if detail.get("guide"):
                st.markdown("### 📖 旅行攻略")
                st.markdown(f"""
                <div class="feature-card">
                {detail['guide']}
                </div>
                """, unsafe_allow_html=True)

            # 乘车建议
            if detail.get("tips"):
                st.markdown("### 💡 乘车建议")
                tips_html = '<div style="display:flex; flex-direction:column; gap:8px;">'
                for tip in detail["tips"]:
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
        else:
            st.info(f"📋 详细攻略正在编写中，敬请期待！")

        if st.button("🔙 返回线路列表", use_container_width=True):
            del st.session_state["selected_route"]
            st.rerun()
