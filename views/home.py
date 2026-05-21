# views/home.py
import streamlit as st
import requests
import time
from datetime import datetime

# 🎨 홈 화면 전용 고도화 스킨 및 입력창 CSS
st.markdown("""
<style>
.hero-section {
    text-align: left;
    padding: 40px 0px 24px 0px;
    background-color: transparent !important;
    border-bottom: 2px solid rgba(128, 128, 128, 0.25) !important;
    margin-bottom: 40px;
}
.hero-title { 
    font-size: 2.6rem !important; 
    font-weight: 700 !important; 
    letter-spacing: -1px; 
}
.feature-card {
    background-color: var(--background-color) !important; 
    padding: 32px 24px; 
    border-radius: 16px !important;
    border: 2px solid rgba(128, 128, 128, 0.25) !important; 
    height: 100%; 
    transition: all 0.25s ease;
}
.feature-card:hover { 
    transform: translateY(-4px); 
    border-color: rgba(128, 128, 128, 0.6) !important; 
}
.feature-card h4 { 
    font-size: 1.25rem !important; 
    font-weight: 600 !important; 
    margin-top: 14px; 
    margin-bottom: 8px; 
}
.feature-card p { 
    opacity: 0.75; 
    font-size: 0.95rem !important; 
    line-height: 1.6; 
}
.beta-notice-card { 
    border: 2px solid var(--text-color) !important; 
    padding: 35px; 
    border-radius: 16px !important; 
    margin-top: 40px; 
}
.api-guide-box { 
    background-color: rgba(59, 130, 246, 0.06) !important; 
    border-left: 4px solid #3b82f6 !important; 
    padding: 20px; 
    border-radius: 8px; 
    margin-top: 20px; 
    margin-bottom: 20px; 
}
.api-link { 
    color: #3b82f6 !important; 
    text-decoration: underline !important; 
    font-weight: 700 !important; 
}
.stTextArea textarea, .stTextInput input { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}
</style>
""", unsafe_allow_html=True)

# 🗺️ 사이드바 브랜딩 및 현재 위치 표시
with st.sidebar:
    st.markdown("<h2 style='font-size:1.4rem; font-weight:700; margin-bottom:5px;'>📐 DDalGGak Math</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; opacity:0.6; margin-bottom:25px;'>Premium EdTech SaaS</p>", unsafe_allow_html=True)
    st.write("현재 위치: **🏠 Home**")

# 메인 히어로 섹션
st.markdown("""
<div class="hero-section">
    <div class="hero-title">DDalGGak Math</div>
    <p style="font-size:1.15rem; opacity:0.8; margin-top:10px;">대한민국 최초 출제위원 기조의 수학 문항 역산 설계 및 실물 시험지 변형 엔진</p>
</div>
""", unsafe_allow_html=True)

# 테크놀로지 로드맵 섹션
st.markdown("<h3 style='font-size:1.4rem; font-weight:600; margin-bottom:20px;'>📐 테크놀로지 로드맵</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div class="feature-card">
    <span style="font-size: 1.8rem;">⚙️</span>
    <h4>평가원 수학 무결성 검증</h4>
    <p>단순 텍스트 치환 방식이 아닙니다. 교육과정 성취기준을 추론하여 중간 연산 과정과 정답이 유리수 형태로 딱 떨어지도록 정교하게 역산 설계합니다.</p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="feature-card">
    <span style="font-size: 1.8rem;">📄</span>
    <h4>실물 시험지 컴파일러</h4>
    <p>수능 수학 특유의 합답형 &lt;보기&gt; 박스 레이아웃과 5지선다 오답 선지 구성 원리를 수학적으로 분석하여 인쇄용 프리뷰를 즉시 렌더링합니다.</p>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="feature-card">
    <span style="font-size: 1.8rem;">🧠</span>
    <h4>사고과정 상속 메커니즘</h4>
    <p>원본 문항의 기하학적 대칭성, 케이스 분류 등 상위 핵심 추론 논리만 추출합니다. 완전히 위장된 고품질 창조 문항을 만듭니다.</p>
</div>
""", unsafe_allow_html=True)

# 오픈 베타 안내 카드
st.markdown("""
<div class="beta-notice-card">
    <h3 style="margin-top:0; font-weight:700;">📢 프리미엄 오픈 베타 진행 중</h3>
    <p style="opacity: 0.85; line-height: 1.6; font-size: 1rem; margin-top: 12px;">
        현재 현직 교육 관계자 및 학생/학부모님들을 대상으로 무료 베타 테스트를 진행하고 있습니다.<br>
        본 플랫폼의 AI 변형 출제 엔진은 구글의 Gemini API 기반으로 구동되므로, 원활한 사용을 위해 본인의 API Key 입력이 필요합니다.
    </p>
    <div class="api-guide-box">
        💡 <b>Gemini API Key가 없으신가요?</b><br>
        <a class="api-link" href="https://aistudio.google.com/" target="_blank">Google AI Studio (여기를 딸깍 클릭)</a>에 구글 계정으로 로그인하신 후, 
        <b>[Get API key]</b> 버튼을 누르면 10초 만에 무료 키를 발급받으실 수 있습니다.
    </div>
    <p style="font-weight: 600; margin-top: 15px; font-size: 1.05rem;">
        👈 Key를 발급받으신 후, 왼쪽 메뉴에서 <b>[AI 단일 문항 변형]</b>을 누르고 사이드바 입력창에 붙여넣어 보세요!
    </p>
</div>
""", unsafe_allow_html=True)

# 📝 피드백 수집 및 구글 시트 연동 섹션
st.write("")
st.markdown("### 💬 엔진 퀄리티 향상을 위한 의견 제시")

# 💡 요구사항 반영: '직업 입력' 창으로 변경 및 예시를 딱 4개만 노출
user_info_input = st.text_input(
    "직업을 입력해주세요", 
    placeholder="ex) 교사, 강사, 학생, 학부모"
)

feedback_text = st.text_area(
    "의견이나 개선 요청사항을 자유롭게 입력해 주세요", 
    height=100, 
    placeholder="ex) 홈페이지가 가독성이 떨어져요"
)

# 3초 알림 메시지 제어용 빈 슬롯
msg_slot = st.empty()

if st.button("의견 전송하기", type="secondary"):
    if not feedback_text: 
        msg_slot.warning("내용을 입력하신 후 전송해 주세요.")
    elif not user_info_input: 
        msg_slot.warning("피드백 데이터베이스 관리를 위해 '직업'을 먼저 입력해 주세요.")
    else:
        with st.spinner('구글 데이터베이스 시트에 안전하게 실시간 기록 중...'):
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfMMoBOa7hBNNpPcsMxePiXmAGfgI8eL20NK54p9rZv4usnvw/formResponse"
            payload = {
                "entry.1056156260": feedback_text, 
                "entry.1147584167": user_info_input
            }
            try:
                response = requests.post(form_url, data=payload)
                if response.status_code == 200:
                    # 3초간 메시지 띄우기 기믹 실행
                    msg_slot.success("🎉 감사합니다! 제출해주신 피드백이 연동된 구글 시트에 실시간 반영되었습니다.")
                    time.sleep(3.0)
                    msg_slot.empty()  # 3초 후 메시지 박스 투명하게 폭파
                else: 
                    msg_slot.error("시트 전송 중 일시적인 서버 지연이 발생했습니다. 잠시 후 다시 시도해 주세요.")
            except Exception as e: 
                msg_slot.error(f"구글 시트 연동 오류 발생: {e}")
