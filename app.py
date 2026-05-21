# app.py
import streamlit as st

st.set_page_config(
    page_title="DDalGGak Math - AI 수학 문제 변형 SaaS",
    page_icon="📐",
    layout="wide"
)

# 🎨 [하이브리드 테마] 라이트/다크모드에 완벽하게 동기화되는 프리미엄 CSS
st.markdown("""
    <style>
    /* 1. 시스템 테마 변수를 그대로 이어받아 배경과 글씨색 자동 동기화 */
    .stApp {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* 2. 사이드바 영역도 시스템 테마에 맞춰 투명 가독성 확보 */
    [data-testid="stSidebar"] {
        background-color: var(--background-color) !important;
        border-right: 1px solid rgba(128, 128, 128, 0.1) !important;
    }
    
    /* 3. 상단 메인 타이틀 세션 (테마 친화적 매트 라인 스타일) */
    .hero-section {
        text-align: left;
        padding: 40px 0px 24px 0px;
        background-color: transparent !important;
        border-bottom: 1px solid rgba(128, 128, 128, 0.15) !important;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        margin-bottom: 12px;
        letter-spacing: -0.8px;
    }
    .hero-subtitle {
        font-size: 1.1rem !important;
        color: var(--text-color) !important;
        opacity: 0.8;
        font-weight: 400;
    }
    
    /* 4. ★핵심★ 테마별 가변 그림자 카드로 개편 (라이트: 소프트 섀도우 / 다크: 은은한 발광 효과) */
    .feature-card {
        background-color: var(--background-color) !important;
        padding: 32px 24px;
        border-radius: 16px !important;
        border: 1px solid rgba(128, 128, 128, 0.1) !important;
        text-align: left;
        /* 다크모드에서도 텁텁하지 않도록 투명도 기반의 고급 입체 섀도우 처리 */
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.03), 
                    0 1px 2px 0 rgba(0, 0, 0, 0.02);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(128, 128, 128, 0.3) !important;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.1);
    }
    .feature-card h4 {
        color: var(--text-color) !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 14px;
        margin-bottom: 8px;
    }
    .feature-card p {
        color: var(--text-color) !important;
        opacity: 0.75;
        font-size: 0.92rem !important;
        line-height: 1.6;
    }
    
    /* 5. 요금제 카드 슬림 테마 매핑 */
    .price-card {
        background-color: var(--background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
        border-top: 4px solid var(--text-color) !important; /* 모드별 반전 포인트 선 */
        padding: 35px;
        border-radius: 16px !important;
        text-align: center;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.02);
    }
    .price-card h3 { color: var(--text-color) !important; font-size: 1.25rem !important; font-weight: 600 !important; }
    .price-card h2 { color: var(--text-color) !important; font-size: 2.4rem !important; font-weight: 700 !important; margin: 12px 0; }
    .price-card p { color: var(--text-color) !important; opacity: 0.6; }
    .price-card ul { padding-left: 15px; margin-top: 20px; }
    .price-card li { color: var(--text-color) !important; opacity: 0.85; font-size: 0.9rem !important; text-align: left; margin-bottom: 10px; }
    
    /* 탭 메뉴 텍스트 완전 동기화 */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid rgba(128, 128, 128, 0.15) !important; }
    .stTabs button { color: var(--text-color) !important; opacity: 0.6; }
    .stTabs button[aria-selected="true"] { opacity: 1 !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# 메인 배너
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">DDalGGak Math</div>
        <div class="hero-subtitle">시험지 이미지 업로드 단 한번으로, 평가원 감성의 무결성 변형 문제를 '딸깍' 찍어내세요.</div>
    </div>
""", unsafe_allow_html=True)

# 기능 카드
st.markdown("<h3 style='font-size:1.3rem; font-weight:600; margin-bottom:20px;'>✨ 핵심 기능 안내</h3>", unsafe_allow_html=True)
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
st.divider()

# 요금제
st.markdown("<h3 style='font-size:1.3rem; font-weight:600; margin-bottom:20px;'>💳 요금제 플랜</h3>", unsafe_allow_html=True)
p_col1, p_col2 = st.columns([1, 1.8])

with p_col1:
    st.markdown("""
        <div class="price-card">
            <h3>강사 프리미엄</h3>
            <h2>월 39,000원</h2>
            <p>학원 교재 제작 및 기출 변형 무제한 생성</p>
            <hr style='border:0; border-top:1px solid rgba(128,128,128,0.1); margin:15px 0;'>
            <ul>
                <li>Gemini 2.5 기반 고밀도 추론 변형</li>
                <li>수능형 실물 인쇄 전용 템플릿 제공</li>
                <li>매력적인 오답 선지 실수 메커니즘 설계</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with p_col2:
    st.markdown("<h4 style='font-weight:600; margin-top:0;'>🚀 지금 바로 시작하세요</h4>", unsafe_allow_html=True)
    st.write("초기 런칭 기념으로 현재 모든 강사님들께 무료 크레딧을 제공하고 있습니다. 왼쪽 메뉴에서 변형 엔진을 선택해 보세요.")
    st.info("👈 왼쪽 사이드바 메뉴창에 생성된 **[DDalGGak Math]** 탭을 누르시면 AI 변형기 화면으로 즉시 연결됩니다.")
