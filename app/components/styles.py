"""
全局样式注入模块 - 所有页面共享
解决Streamlit多页面应用中CSS只注入main.py不生效于其他页面的问题
"""

import streamlit as st
from pathlib import Path


def inject_styles():
    """注入全局CSS美化 + PWA meta标签"""
    # CSS注入 — 注意路径：本文件在 app/components/，CSS在 app/static/
    css_path = Path(__file__).resolve().parent.parent / "static" / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # 手机端CSS注入
    mobile_css_path = Path(__file__).resolve().parent.parent / "static" / "mobile.css"
    if mobile_css_path.exists():
        mobile_css = mobile_css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{mobile_css}</style>", unsafe_allow_html=True)

    # PWA meta标签
    st.markdown("""
    <meta name="theme-color" content="#FF6B35">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="省心小助手">
    <link rel="manifest" href="/static/manifest.json">
    """, unsafe_allow_html=True)
