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
            """
            <div class="dd-sidebar-brand">
                <h2>DDalGGak Math</h2>
                <p>AI math item studio</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="dd-location">현재 위치<br><b>{location}</b></div>',
            unsafe_allow_html=True,
        )
