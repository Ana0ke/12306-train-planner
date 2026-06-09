"""
手机端底部导航组件

⚠️ 注意：此组件已禁用
Streamlit多页面应用不支持通过HTML链接跳转页面
侧边栏导航在移动端足够使用，底部导航会占用屏幕空间
如需页面导航，请使用 st.switch_page() 或直接使用侧边栏
"""

import streamlit as st
from pathlib import Path


def get_page_config() -> list[dict]:
    """
    获取页面配置
    返回页面列表，包含名称、图标和路径
    """
    return [
        {"name": "路线规划", "icon": "🔍", "path": "/1_🔍_路线规划"},
        {"name": "热门线路", "icon": "🏔️", "path": "/2_🏔️_热门线路"},
        {"name": "订票助手", "icon": "🎫", "path": "/3_🎫_订票助手"},
        {"name": "AI规划", "icon": "🤖", "path": "/4_🤖_AI旅行规划"},
    ]


def render_mobile_nav():
    """
    渲染手机端底部导航栏
    
    ⚠️ 已禁用：Streamlit不支持通过HTML链接跳转页面
    移动端用户请使用侧边栏导航
    """
    # 不再渲染底部导航栏
    # 侧边栏在移动端会自动适配，无需额外导航
    pass


def render_nav_placeholder():
    """
    渲染底部导航占位元素
    预留空间防止内容被遮挡（已禁用导航，占位符不再需要）
    """
    # 占位符不再需要
    pass


def is_mobile_device() -> bool:
    """
    检测是否为移动设备
    
    Returns:
        是否为移动设备
    """
    return False
