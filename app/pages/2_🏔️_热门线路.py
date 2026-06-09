"""
12306省心小助手 - 热门线路页面
"""

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="热门线路 🏔️", page_icon="🏔️", layout="wide")

st.title("🏔️ 热门旅游线路")
st.caption("8条经典火车旅游线路，每条都有沿途攻略和乘车指南")

# 加载线路数据
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "routes"

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

# 线路卡片展示
cols = st.columns(2)
for i, route in enumerate(ROUTES_INDEX):
    with cols[i % 2]:
        with st.container(border=True):
            col_title, col_info = st.columns([3, 2])
            with col_title:
                st.markdown(f"### {route['name']}")
                st.caption(route["subtitle"])
                st.markdown(f"📍 **路线：** {route['route']}")
            with col_info:
                st.markdown(f"🕐 **耗时：** {route['duration']}")
                st.markdown(f"🗓️ **最佳季节：** {route['best_season']}")
                st.markdown(f"✨ **亮点：** {route['highlights']}")

            # 查看详情按钮
            if st.button("📖 查看攻略", key=f"detail_{route['id']}"):
                st.session_state["selected_route"] = route["id"]
                st.rerun()

# ===== 线路详情 =====
if "selected_route" in st.session_state:
    route_id = st.session_state["selected_route"]
    route_info = next((r for r in ROUTES_INDEX if r["id"] == route_id), None)

    if route_info:
        st.divider()
        st.markdown(f"## {route_info['name']} · {route_info['subtitle']}")

        # 加载详细数据
        detail_file = DATA_DIR / f"{route_id}.json"
        if detail_file.exists():
            with open(detail_file, "r", encoding="utf-8") as f:
                detail = json.load(f)

            # 沿途站点
            st.markdown("### 🚉 沿途站点")
            for station in detail.get("stations", []):
                st.markdown(f"- **{station['name']}** — {station.get('desc', '')}")

            # 攻略信息
            if detail.get("guide"):
                st.markdown("### 📖 旅行攻略")
                st.markdown(detail["guide"])

            # 乘车建议
            if detail.get("tips"):
                st.markdown("### 💡 乘车建议")
                for tip in detail["tips"]:
                    st.markdown(f"- {tip}")
        else:
            st.info(f"📋 详细攻略正在编写中，敬请期待！")

        if st.button("🔙 返回线路列表"):
            del st.session_state["selected_route"]
            st.rerun()
