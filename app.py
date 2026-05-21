# app.py
import streamlit as st

st.set_page_config(
    page_title="DDalGGak Math - AI 수학 문제 변형 SaaS",
    page_icon="📐",
    layout="wide"
)

# 🎨 짙은 남색을 완전히 배제한 100% Pure 화이트 & 미니멀 라인 마스터 CSS
st.markdown("""
    <style>
    /* 1. 전체 기본 배경 및 앱 컨테이너를 완벽한 흰색으로 고정 */
    .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stHeader"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    
    /* 2. 사이드바 역시 완벽한 화이트로 통일하고 미세한 슬림 경계선만 적용 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f1f5f9 !important;
    }
    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    
    /* 3. 문제의 짙은 남색 배너 전면 제거 -> 화이트 매트 타이틀 섹션으로 개편 */
    .hero-section {
        text-align: left;
        padding: 40px 0px 20px 0px;
        background-color: #ffffff !important;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-bottom: 12px;
        letter-spacing: -0.8px;
    }
    .hero-subtitle {
        font-size: 1.1rem !important;
        color: #475569 !important;
        font-weight: 400;
    }
    
    /* 4. 빅밸류 스타일: 극도로 정교한 그림자와 선으로만 처리된 퓨어 화이트 카드 */
    .feature-card {
        background-color: #ffffff !important;
        padding: 30px 24px;
        border-radius: 12px !important;
        border: 1px solid #f1f5f9 !important;
        text-align: left;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03), 
                    0 10px 40px -10px rgba(0, 0, 0, 0.02);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        border-color: #e2e8f0 !important;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.06);
    }
    .feature-card h4 {
        color: #0f172a !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 14px;
        margin-bottom: 8px;
        letter-spacing: -0.3px;
    }
    .feature-card p {
        color: #475569 !important;
        font-size: 0.92rem !important;
        line-height: 1.6;
    }
    
    /* 5. 요금제 카드 역시 화이트 톤 기반 미니멀 라인으로 매핑 */
    .price-card {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-top: 3px solid #0f172a !important; /* 블랙 포인트 라인 */
        padding: 35px;
        border-radius: 12px !important;
        text-align: center;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.02);
    }
    .price-card h3 { color: #0f172a !important; font-size: 1.25rem !important; font-weight: 600 !important; margin: 0; }
    .price-card h2 { color: #0f172a !important; font-size: 2.4rem !important; font-weight: 700 !important; margin: 12px 0; letter-spacing: -1px; }
    .price-card p { color: #64748b !important; font-size: 0.88rem !important; }
    .price-card ul { padding-left: 15px; margin-top: 20px; }
    .price-card li { color: #334155 !important; font-size: 0.9rem !important; text-align: left; margin-bottom: 10px; line-height: 1.5; }
    
    /* 탭 메뉴 디자인 미니멀화 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 화이트 매트 타이틀 섹션
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">DDalGGak Math</div>
        <div class="hero-subtitle">시험지 이미지 업로드 단 한번으로, 평가원 감성의 무결성 변형 문제를 '딸깍' 찍어내세요.</div>
    </div>
""", unsafe_allow_html=True)

# 핵심 기능 카드 배치
st.markdown("<h3 style='color:#0f172a; font-size:1.3rem; font-weight:600; margin-bottom:20px; letter-spacing:-0.3px;'>✨ 핵심 기능 안내</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 1.8rem;">📐</span>
            <h4>평가원급 역산 설계</h4>
            <p>중간 과정과 정답이 지저분하지 않고 소름 돋게 딱 떨어지는 정갈한 수능형 수치 설계를 제공합니다.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 1.8rem;">📦</span>
            <h4>실물 시험지 완벽 복제</h4>
            <p>수능 특유의 &lt;보기&gt; 조건 박스와 5지선다 배치를 완벽하게 재현하여 초고화질 인쇄를 지원합니다.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 1.8rem;">🔥</span>
            <h4>사고과정 공유 변형</h4>
            <p>단순 숫자 변형을 넘어, 원본의 핵심 풀이 논리만 상속받고 겉모습을 완벽히 위장한 킬러 문항을 창조합니다.</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")
st.divider()

# 요금제 영역
st.markdown("<h3 style='color:#0f172a; font-size:1.3rem; font-weight:600; margin-bottom:20px; letter-spacing:-0.3px;'>💳 요금제 플랜</h3>", unsafe_allow_html=True)
p_col1, p_col2 = st.columns([1, 1.8])

with p_col1:
    st.markdown("""
        <div class="price-card">
            <h3>강사 프리미엄</h3>
            <h2>월 39,000원</h2>
            <p>학원 교재 제작 및 기출 변형 무제한 생성</p>
            <hr style='border:0; border-top:1px solid #f1f5f9; margin:15px 0;'>
            <ul>
                <li>Gemini 2.5 기반 고밀도 추론 변형</li>
                <li>수능형 실물 인쇄 전용 템플릿 제공</li>
                <li>매력적인 오답 선지 실수 메커니즘 설계</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with p_col2:
    st.markdown("<h4 style='color:#0f172a; font-weight:600; margin-top:0; letter-spacing:-0.3px;'>🚀 지금 바로 시작하세요</h4>", unsafe_allow_html=True)
    st.write("초기 런칭 기념으로 현재 모든 강사님들께 무료 크레딧을 제공하고 있습니다. 왼쪽 메뉴에서 변형 엔진을 선택해 보세요.")
    st.info("👈 왼쪽 사이드바 메뉴창에 생성된 **[DDalGGak Math]** 탭을 누르시면 AI 변형기 화면으로 즉시 연결됩니다.")
