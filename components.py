# components.py
# 여러 views에서 공통으로 사용되는 UI 컴포넌트를 이 파일에서만 관리합니다.
# 브랜딩 문구나 사이드바 레이아웃을 수정하려면 이 파일만 열면 됩니다.

import streamlit as st


def render_sidebar(location: str) -> None:
    """
    모든 페이지의 사이드바 상단에 공통 브랜딩을 표시합니다.

    Args:
        location: 현재 페이지 위치 문자열 (예: "🏠 Home")
    """
    with st.sidebar:
        st.markdown(
            "<h2 style='font-size:1.4rem; font-weight:700; margin-bottom:5px;'>"
            "📐 DDalGGak Math</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size:0.85rem; opacity:0.6; margin-bottom:25px;'>"
            "Premium EdTech SaaS</p>",
            unsafe_allow_html=True,
        )
        st.write(f"현재 위치: **{location}**")
