import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# views/full_exam.py
import streamlit as st

from components import render_sidebar

render_sidebar("⚡ 모의고사 변형")

st.title("⚡ 모의고사 통째로 변형")
st.markdown("""
<div style="border:2px dashed rgba(128,128,128,0.4);padding:40px;border-radius:16px;
            text-align:center;margin-top:50px;">
    <h2 style="font-size:1.6rem;font-weight:700;margin-bottom:15px;">
        🛠️ 현재 AI 엔진 심화 학습 및 파이프라인 구축 중
    </h2>
    <p style="opacity:0.8;font-size:1rem;line-height:1.6;">
        단일 문항 인식을 넘어 문항별 좌표 자동 분할 및 단원 매핑 모델을 고도화하고 있습니다.
    </p>
</div>
""", unsafe_allow_html=True)
