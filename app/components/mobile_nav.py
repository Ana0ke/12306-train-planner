"""
手机端底部导航组件
提供类似App的底部Tab导航体验
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
    
    通过注入HTML/CSS实现固定的底部导航
    用户点击后跳转到对应页面
    """
    pages = get_page_config()
    
    # 构建导航链接HTML
    nav_items = ""
    for page in pages:
        nav_items += f'''
        <a href=".{page['path']}" title="{page['name']}">
            <span>{page['icon']}</span>
            {page['name']}
        </a>
        '''
    
    # 注入CSS和HTML
    st.markdown(f'''
    <style>
    /* 底部导航栏样式 */
    .mobile-nav {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: white !important;
        border-top: 1px solid #e0e0e0 !important;
        display: flex !important;
        justify-content: space-around !important;
        padding: 8px 0 !important;
        z-index: 9999 !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
    }}
    
    .mobile-nav a {{
        text-decoration: none !important;
        color: #666 !important;
        text-align: center !important;
        font-size: 11px !important;
        flex: 1 !important;
        transition: color 0.2s !important;
    }}
    
    .mobile-nav a:hover,
    .mobile-nav a:active {{
        color: #FF4B4B !important;
    }}
    
    .mobile-nav a span {{
        display: block !important;
        font-size: 22px !important;
        margin-bottom: 2px !important;
    }}
    
    /* 底部导航占位（防止内容被遮挡） */
    .nav-placeholder {{
        height: 60px !important;
        width: 100% !important;
    }}
    
    /* 深色模式适配 */
    @media (prefers-color-scheme: dark) {{
        .mobile-nav {{
            background: #1a1a1a !important;
            border-top-color: #333 !important;
        }}
        
        .mobile-nav a {{
            color: #aaa !important;
        }}
        
        .mobile-nav a:hover {{
            color: #FF6B6B !important;
        }}
    }}
    
    /* 仅在移动端显示 */
    @media (min-width: 769px) {{
        .mobile-nav {{
            display: none !important;
        }}
        
        .nav-placeholder {{
            display: none !important;
        }}
    }}
    </style>
    
    <nav class="mobile-nav">
        {nav_items}
    </nav>
    ''', unsafe_allow_html=True)


def render_nav_placeholder():
    """
    渲染底部导航占位元素
    防止页面内容被底部导航遮挡
    """
    st.markdown('''
    <div class="nav-placeholder"></div>
    <style>
    @media (max-width: 768px) {
        .nav-placeholder {
            display: block;
        }
    }
    @media (min-width: 769px) {
        .nav-placeholder {
            display: none;
        }
    }
    </style>
    ''', unsafe_allow_html=True)


def is_mobile_device() -> bool:
    """
    检测是否为移动设备
    通过Streamlit的查询参数判断
    
    Returns:
        是否为移动设备
    """
    # Streamlit Cloud 会传递相关参数
    # 简化判断：通过用户代理或其他方式
    # 实际使用时可以通过JS注入检测
    return False  # 默认返回False，由CSS媒体查询处理
