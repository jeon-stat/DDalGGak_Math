# app.py
import streamlit as st

st.set_page_config(
    page_title="DDalGGak Math - AI 수학 문제 변형 SaaS",
    page_icon="📐",
    layout="wide"
)

# 다크모드를 완벽하게 무력화하고 강제로 고급스러운 화이트/라이트 톤을 유지하는 마스터 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 기본값을 라이트모드로 고정 */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    /* 사이드바 배경 및 텍스트 색상 고정 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    
    /* 히어로 섹션 배너 디자인 슬림화 */
    .hero-section {
        text-align: center;
        padding: 50px 20px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 8px;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 12px;
    }
    .hero-subtitle {
        font-size: 1.1rem !important;
        color: #94a3b8 !important;
    }
    
    /* 기능 카드 가독성 대폭 개선 (글씨 강제 검은색 지정) */
    .feature-card {
        background-color: #ffffff !important;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .feature-card h4 {
        color: #0f172a !important;
        font-size: 1.2rem !important;
        margin-top: 10px;
        margin-bottom: 8px;
    }
    .feature-card p {
        color: #475569 !important;
        font-size: 0.95rem !important;
        line-height: 1.5;
    }
    
    /* 요금제 카드 슬림화 */
    .price-card {
        background-color: #ffffff !important;
        border: 2px solid #3b82f6;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(59,130,246,0.1);
    }
    .price-card h3 { color: #0f172a !important; font-size: 1.3rem !important; margin: 0; }
    .price-card h2 { color: #3b82f6 !important; font-size: 2rem !important; margin: 10px 0; }
    .price-card p { color: #64748b !important; font-size: 0.9rem !important; }
    .price-card li { color: #334155 !important; font-size: 0.9rem !important; text-align: left; margin-bottom: 6px; }
    </style>
""", unsafe_allow_html=True)

# 배너 출력
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">수학 교재 제작의 신세계, DDalGGak Math</div>
        <div class="hero-subtitle">시험지 이미지 업로드 단 한번으로, 평가원 감성의 무결성 변형 문제를 '딸깍' 찍어내세요.</div>
    </div>
""", unsafe_allow_html=True)

# 메인 기능 소개 영역 (글씨 크기 및 가독성 검토 완료)
st.markdown("<h3 style='color:#0f172a; font-size:1.4rem;'>✨ 핵심 기능 안내</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 2rem;">📐</span>
            <h4>평가원급 역산 설계</h4>
            <p>중간 과정과 정답이 지저분하지 않고 소름 돋게 딱 떨어지는 정갈한 수능형 수치 설계를 제공합니다.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 2rem;">📦</span>
            <h4>실물 시험지 완벽 복제</h4>
            <p>수능 특유의 &lt;보기&gt; 조건 박스와 5지선다 배치를 완벽하게 재현하여 초고화질 인쇄를 지원합니다.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <span style="font-size: 2rem;">🔥</span>
            <h4>사고과정 공유 변형</h4>
            <p>단순 숫자 변형을 넘어, 원본의 핵심 풀이 논리만 상속받고 겉모습을 완벽히 위장한 킬러 문항을 창조합니다.</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# 요금제 영역
st.markdown("<h3 style='color:#0f172a; font-size:1.4rem;'>💳 요금제 플랜</h3>", unsafe_allow_html=True)
p_col1, p_col2 = st.columns([1, 1.8])

with p_col1:
    st.markdown("""
        <div class="price-card">
            <h3>강사 프리미엄</h3>
            <h2>월 39,000원</h2>
            <p>학원 교재 제작 및 기출 변형 무제한 생성</p>
            <hr style='border:0; border-top:1px solid #e2e8f0; margin:15px 0;'>
            <ul style='padding-left:15px;'>
                <li>Gemini 2.5 기반 고밀도 추론 변형</li>
                <li>수능형 실물 인쇄 전용 템플릿 제공</li>
                <li>매력적인 오답 선지 실수 메커니즘 설계</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with p_col2:
    st.markdown("<h4 style='color:#0f172a; margin-top:0;'>🚀 지금 바로 시작하세요</h4>", unsafe_allow_html=True)
    st.write("초기 런칭 기념으로 현재 모든 강사님들께 무료 크레딧을 제공하고 있습니다. 왼쪽 메뉴에서 변형 엔진을 선택해 보세요.")
    st.info("👈 왼쪽 사이드바 메뉴창에 생성된 **[DDalGGak Math]** 탭을 누르시면 AI 변형기 화면으로 즉시 연결됩니다.")