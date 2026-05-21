# app.py
import streamlit as st

st.set_page_config(
    page_title="DDalGGak Math - AI 수학 문제 변형 SaaS",
    page_icon="📐",
    layout="wide"
)

# 🎨 [디자인 전면 개편] 전체 Pure 화이트 배경 + 소프트 그림자 마스터 CSS
st.markdown("""
    <style>
    /* 1. 전체 기본 배경을 완벽한 흰색으로 고정 */
    .stApp {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* 2. 사이드바도 깔끔한 화이트 + 우측 슬림 경계선 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f1f5f9 !important;
    }
    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    
    /* 3. 상단 메인 배너 슬림화 및 모던 딥블루 그라데이션 */
    .hero-section {
        text-align: center;
        padding: 45px 20px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 12px;
        margin-bottom: 35px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
    }
    .hero-title {
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem !important;
        color: #94a3b8 !important;
    }
    
    /* 4. ★요청 반영★ 화이트 배경 카드 + 부드러운 프리미엄 그림자 박스 */
    .feature-card {
        background-color: #ffffff !important;
        padding: 28px 24px;
        border-radius: 12px !important;
        border: 1px solid #f1f5f9 !important;
        text-align: center;
        /* 은은하고 넓게 퍼지는 최신 고급 그림자 효과 */
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.04), 0 1px 4px 0 rgba(0, 0, 0, 0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }
    /* 카드에 마우스 올렸을 때 살짝 떠오르는 애니메이션 효과 (SaaS 감성) */
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.08);
    }
    .feature-card h4 {
        color: #0f172a !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    .feature-card p {
        color: #475569 !important;
        font-size: 0.92rem !important;
        line-height: 1.6;
    }
    
    /* 5. 요금제 플랜 카드 그림자 및 레이아웃 다듬기 */
    .price-card {
        background-color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        padding: 32px;
        border-radius: 14px !important;
        text-align: center;
        box-shadow: 0 10px 30px -5px rgba(59, 130, 246, 0.08);
    }
    .price-card h3 { color: #0f172a !important; font-size: 1.25rem !important; font-weight: 600 !important; margin: 0; }
    .price-card h2 { color: #3b82f6 !important; font-size: 2.2rem !important; font-weight: 700 !important; margin: 12px 0; }
    .price-card p { color: #64748b !important; font-size: 0.88rem !important; }
    .price-card ul { padding-left: 15px; margin-top: 15px; }
    .price-card li { color: #334155 !important; font-size: 0.88rem !important; text-align: left; margin-bottom: 8px; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

# 메인 배너
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">수학 교재 제작의 신세계, DDalGGak Math</div>
        <div class="hero-subtitle">시험지 이미지 업로드 단 한번으로, 평가원 감성의 무결성 변형 문제를 '딸깍' 찍어내세요.</div>
    </div>
""", unsafe_allow_html=True)

# 핵심 기능 카드 배치
st.markdown("<h3 style='color:#0f172a; font-size:1.3rem; font-weight:600; margin-bottom:16px;'>✨ 핵심 기능 안내</h3>", unsafe_allow_html=True)
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
st.markdown("<h3 style='color:#0f172a; font-size:1.3rem; font-weight:600; margin-bottom:16px;'>💳 요금제 플랜</h3>", unsafe_allow_html=True)
p_col1, p_col2 = st.columns([1, 1.8])

with p_col1:
    st.markdown("""
        <div class="price-card">
            <h3>강사 프리미엄</h3>
            <h2>월 1,000원</h2>
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
    st.markdown("<h4 style='color:#0f172a; font-weight:600; margin-top:0;'>🚀 지금 바로 시작하세요</h4>", unsafe_allow_html=True)
    st.write("초기 런칭 기념으로 현재 모든 강사님들께 무료 크레딧을 제공하고 있습니다. 왼쪽 메뉴에서 변형 엔진을 선택해 보세요.")
    st.info("👈 왼쪽 사이드바 메뉴창에 생성된 **[DDalGGak Math]** 탭을 누르시면 AI 변형기 화면으로 즉시 연결됩니다.")
