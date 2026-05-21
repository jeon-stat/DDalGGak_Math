# app.py
import streamlit as st

# 1. 페이지 글로벌 설정
st.set_page_config(
    page_title="DDalGGak Math Pro - 프리미엄 AI 수학 문제 변형 플랫폼",
    page_icon="📐",
    layout="wide"
)

# 🎨 사이드바 및 레이아웃 프리미엄 라인 CSS
st.markdown("""
    <style>
    .stApp { background-color: var(--background-color) !important; color: var(--text-color) !important; }
    [data-testid="stSidebar"] {
        background-color: var(--background-color) !important;
        border-right: 2px solid rgba(128, 128, 128, 0.25) !important;
    }
    /* 스트림릿 기본 멀티페이지 메뉴(파일명 노출되는 것)를 통째로 숨김 처리 */
    [data-testid="stSidebarNav"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 2. 공식 st.navigation 기능을 이용한 커스텀 메뉴 선언 (한글 매핑)
pg = st.navigation([
    st.Page("pages/home.py", title="Home", icon="🏠"),
    st.Page("pages/single_math.py", title="AI 단일 문항 변형", icon="📐"),
    st.Page("pages/full_exam.py", title="모의고사 통째로 변형", icon="⚡"),
    st.Page("pages/question_box.py", title="나만의 오답 보관함", icon="🗂️"),
])

# 3. 선택된 페이지 가동
pg.run()
