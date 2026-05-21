# app.py
# 앱 진입점: 라우팅 설정만 담당합니다.
# CSS → styles.py / 메타 정보 → config.py

import streamlit as st

from config import APP_TITLE, APP_ICON
from styles import APP_CSS

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
)

st.markdown(APP_CSS, unsafe_allow_html=True)

pages = [
    st.Page("views/home.py",         title="Home",                           icon="🏠"),
    st.Page("views/single_math.py",  title="AI 단일 문항 변형",              icon="📐"),
    st.Page("views/full_exam.py",    title="모의고사 통째로 변형 (준비중)",  icon="⚡"),
    st.Page("views/question_box.py", title="나만의 오답 보관함 (준비중)",    icon="🗂️"),
]

pg = st.navigation(pages)
pg.run()
