# views/question_box.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from components import render_sidebar

render_sidebar("🗂️ 오답 보관함")

st.title("🗂️ 클라우드 문항 및 오답 보관함")
st.markdown("""
<div style="border:2px dashed rgba(128,128,128,0.4);padding:40px;border-radius:16px;
            text-align:center;margin-top:50px;">
    <h2 style="font-size:1.6rem;font-weight:700;margin-bottom:15px;">
        🔐 회원가입 및 데이터베이스 보안 연동 예정
    </h2>
    <p style="opacity:0.8;font-size:1rem;line-height:1.6;">
        내가 생성한 프리미엄 변형 문항들을 영구적으로 저장하는
        강사 전용 클라우드 스토리지를 준비 중입니다.
    </p>
</div>
""", unsafe_allow_html=True)
