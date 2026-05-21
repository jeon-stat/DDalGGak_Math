# pages/2_Full_Exam_Split.py
import streamlit as st

st.set_page_config(page_title="모의고사 통째로 변형", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: var(--background-color) !important; color: var(--text-color) !important; }
    [data-testid="stSidebar"] { background-color: var(--background-color) !important; border-right: 2px solid rgba(128, 128, 128, 0.25) !important; }
    .teaser-box {
        border: 2px dashed rgba(128, 128, 128, 0.4);
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ 모의고사 통째로 변형 (Full-Exam Converter)")
st.markdown("시험지 PDF 한 장만 올리면 내신/수능 모의고사 30문항 전체를 원클릭 변형하는 핵심 코어 기능입니다.")

st.markdown("""
    <div class="teaser-box">
        <h2 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 15px;">🛠️ 현재 AI 엔진 심화 학습 및 파이프라인 구축 중</h2>
        <p style="opacity: 0.8; font-size: 1rem; line-height: 1.6;">
            단일 문항 인식을 넘어 문항별 좌표 자동 분할(Object Detection) 및 단원 매핑 모델을 고도화하고 있습니다.<br>
            오픈 베타 기간 동안 강사님들의 피드백을 반영하여 가장 완벽한 무결성 모의고사 제작기로 찾아뵙겠습니다.
        </p>
        <p style="font-weight: 600; color: #3b82f6; margin-top: 20px; font-size: 1.05rem;">
            🚀 Coming Soon — 첫 번째 메뉴의 [AI 단일 문항 변형] 기능을 먼저 체험해 보세요!
        </p>
    </div>
""", unsafe_allow_html=True)
