# pages/3_My_Question_Box.py
import streamlit as st

st.set_page_config(page_title="나만의 오답 보관함", page_icon="🗂️", layout="wide")

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

st.title("🗂️ 클라우드 문항 및 오답 보관함")
st.markdown("학원 학생별 오답 노트 관리 및 나만의 시크릿 교재 단원별 데이터베이스 아카이빙 시스템입니다.")

st.markdown("""
    <div class="teaser-box">
        <h2 style="font-size: 1.8rem; font-weight: 700; margin-bottom: 15px;">🔐 회원가입 및 데이터베이스 보안 연동 예정</h2>
        <p style="opacity: 0.8; font-size: 1rem; line-height: 1.6;">
            내가 생성한 프리미엄 변형 문항들을 영구적으로 저장하고, 학생별 커스텀 시험지로 재조합할 수 있는<br>
            강사 전용 클라우드 스토리지 시스템을 준비 중입니다.
        </p>
        <p style="font-weight: 600; color: #10b981; margin-top: 20px; font-size: 1.05rem;">
            📈 정식 버전 출시와 함께 가동됩니다. 많은 기대 부탁드립니다!
        </p>
    </div>
""", unsafe_allow_html=True)
