# app.py
import streamlit as st

st.set_page_config(
    page_title="DDalGGak Math Pro - 프리미엄 AI 수학 문제 변형 플랫폼",
    page_icon="📐",
    layout="wide"
)

# 🎨 라이트/다크모드 완벽 대응 및 미니멀 스킨 CSS (메뉴 숨김 버그 코드 제거 완료)
st.markdown("""
<style>
.stApp {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}
[data-testid="stSidebar"] {
    background-color: var(--background-color) !important;
    border-right: 2px solid rgba(128, 128, 128, 0.25) !important;
}
/* 대참사를 일으켰던 stSidebarNav display none 코드를 삭제했습니다 */
</style>
""", unsafe_allow_html=True)

# 🗺️ 스트림릿 최신 공식 기능을 활용해 한글 메뉴와 독립 파일들을 1:1 매핑
pages = [
    st.Page("views/home.py", title="Home", icon="🏠"),
    st.Page("views/single_math.py", title="AI 단일 문항 변형", icon="📐"),
    st.Page("views/full_exam.py", title="모의고사 통째로 변형 (준비중)", icon="⚡"),
    st.Page("views/question_box.py", title="나만의 오답 보관함 (준비중)", icon="🗂️")
]

# 🎛️ 메뉴판 가동 및 화면 연동
pg = st.navigation(pages)
pg.run()
