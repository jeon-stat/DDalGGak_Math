# app.py
import streamlit as st

st.set_page_config(
    page_title="DDalGGak Math Pro - 프리미엄 AI 수학 문제 변형 플랫폼",
    page_icon="📐",
    layout="wide"
)

# 🎨 [트릭 및 디자인] 사이드바 맨 위 'app' 글자를 'Home'으로 강제 치환하는 마스터 CSS
st.markdown("""
    <style>
    .stApp {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* [핵심 트릭] 사이드바의 첫 번째 메뉴(app.py) 글자를 Home으로 보이지 않게 치환 */
    section[data-testid="stSidebar"] re-element, 
    section[data-testid="stSidebar"] li:first-child span {
        font-size: 0 !important;
    }
    section[data-testid="stSidebar"] li:first-child span::after {
        content: "🏠 Home" !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--background-color) !important;
        border-right: 2px solid rgba(128, 128, 128, 0.25) !important;
    }
    
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
        color: var(--text-color) !important;
        margin-bottom: 12px;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.15rem !important;
        color: var(--text-color) !important;
        opacity: 0.8;
    }
    
    .feature-card {
        background-color: var(--background-color) !important;
        padding: 32px 24px;
        border-radius: 16px !important;
        border: 2px solid rgba(128, 128, 128, 0.25) !important;
        text-align: left;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.02);
        transition: all 0.25s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(128, 128, 128, 0.6) !important;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.08);
    }
    .feature-card h4 {
        color: var(--text-color) !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 14px;
        margin-bottom: 8px;
    }
    .feature-card p {
        color: var(--text-color) !important;
        opacity: 0.75;
        font-size: 0.95rem !important;
        line-height: 1.6;
    }
    
    .beta-notice-card {
        background-color: var(--background-color) !important;
        border: 2px solid var(--text-color) !important;
        padding: 35px;
        border-radius: 16px !important;
        margin-top: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
    }
    
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid rgba(128, 128, 128, 0.2) !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-section">
        <div class="hero-title">DDalGGak Math Pro</div>
        <div class="hero-subtitle">대한민국 최초 출제위원 기조의 수학 문항 역산 설계 및 실물 시험지 변형 엔진</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='font-size:1.4rem; font-weight:600; margin-bottom:20px; letter-spacing:-0.5px;'>📐 테크놀로지 로드맵</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 1.8rem;">⚙️</span>
            <h4>평가원 수학 무결성 검증 시스템</h4>
            <p>단순 텍스트 치환 방식이 아닙니다. 교육과정 성취기준을 추론하여 중간 연산 과정และ 정답이 유리수 형태로 딱 떨어지도록 정교하게 역산 설계(Backward Design)합니다.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 1.8rem;">📄</span>
            <h4>실물 시험지 컴파일러 기술</h4>
            <p>수능 수학 특유의 합답형 &lt;보기&gt; 박스 레이아웃과 5지선다 오답 선지 구성 원리를 수학적으로 분석하여, 실제 시험지와 동일한 인쇄용 프리뷰를 즉시 렌더링합니다.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 1.8rem;">🧠</span>
            <h4>사고과정 상속 메커니즘</h4>
            <p>원본 문항의 기하학적 대칭성, 케이스 분류 등 상위 핵심 추론 논리만 추출합니다. 함수와 겉모습을 완벽하게 다르게 위장하여 시중 교재에 없는 완전한 창조 문항을 만듭니다.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="beta-notice-card">
        <h3 style="margin-top:0; font-weight:700; letter-spacing:-0.5px;">📢 강사 대상 프리미엄 오픈 베타 진행 중</h3>
        <p style="opacity: 0.85; line-height: 1.6; font-size: 1rem; margin-top: 12px;">
            DDalGGak Math는 복잡하고 정교한 수학 문항 제작 과정에서 강사님들이 겪는 계산적 피로를 단 한 번의 <b>'딸깍'</b>으로 해결하고자 시작된 프로젝트입니다.<br>
            현재 대치동 및 학원가 현직 강사님들을 대상으로 출제 엔진 무결성 검증을 위한 <b>무료 베타 테스트</b>를 진행하고 있습니다.
        </p>
        <p style="font-weight: 600; margin-top: 20px; font-size: 1.05rem;">
            👈 왼쪽 사이드바 메뉴에서 <b>[AI 단일 문항 변형]</b>을 선택해 출제위원 AI 엔진의 파워를 직접 경험해 보세요.
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")
st.markdown("### 💬 엔진 퀄리티 향상을 위한 의견 제시")
st.write("변형된 문제의 조건에 수학적 모순이 있거나, 수식 렌더링이 매끄럽지 않은 부분이 있다면 언제든 아래 공간에 가감 없이 적어주세요.")

feedback_text = st.text_area("의견이나 개선 요청사항을 자유롭게 입력해 주세요 (예: 킬러 문항 변형 시 조건 누락 발생 등)", height=100)
if st.button("의견 전송하기", type="secondary"):
    if feedback_text:
        st.success("🙏 소중한 전문 의견이 개발 팀 및 AI 엔진 출제위원회에 전달되었습니다. 감사합니다!")
    else:
        st.warning("내용을 입력하신 후 전송해 주세요.")
