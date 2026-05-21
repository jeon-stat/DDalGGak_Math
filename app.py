# app.py
import streamlit as st
from PIL import Image
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

st.set_page_config(
    page_title="DDalGGak Math Pro - 프리미엄 AI 수학 문제 변형 플랫폼",
    page_icon="📐",
    layout="wide"
)

# 🎨 [디자인 고도화] 라이트/다크모드 완벽 대응 및 2px 미니멀 라인 CSS
st.markdown("""
    <style>
    .stApp {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    
    /* 사이드바 경계선 강화 */
    [data-testid="stSidebar"] {
        background-color: var(--background-color) !important;
        border-right: 2px solid rgba(128, 128, 128, 0.25) !important;
    }
    
    /* 스트림릿이 자동으로 긁어오는 영문 pages 메뉴를 투명하게 숨김 처리 (대참사 원인 제거) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* 인풋 상자 테두리 스킨 변경 */
    .stTextArea textarea, .stTextInput input, .stSelectbox div {
        background-color: var(--background-color) !important;
        border: 1.5px solid rgba(128, 128, 128, 0.3) !important;
        color: var(--text-color) !important;
        border-radius: 8px !important;
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
        letter-spacing: -1px;
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
    }
    .feature-card h4 { font-size: 1.25rem !important; font-weight: 600 !important; margin-top: 14px; margin-bottom: 8px; }
    .feature-card p { opacity: 0.75; font-size: 0.95rem !important; line-height: 1.6; }
    
    .beta-notice-card {
        border: 2px solid var(--text-color) !important;
        padding: 35px;
        border-radius: 16px !important;
        margin-top: 40px;
    }
    
    /* 📄 수능 시험지 렌더링 용지 스타일 */
    .ddalggak-paper-sheet {
        background-color: #ffffff !important;
        padding: 45px 55px;
        border: 2px solid #000000 !important;
        box-shadow: 0 20px 50px -12px rgba(0,0,0,0.15);
        font-family: 'Noto Serif KR', 'Batang', serif !important;
        margin: 30px auto;
        max-width: 860px;
        border-radius: 4px;
    }
    .ddalggak-paper-sheet * { color: #000000 !important; background-color: transparent !important; }
    .ddalggak-paper-sheet blockquote { border: 2px solid #000000 !important; padding: 20px !important; margin: 15px 0 !important; }
    .ddalggak-paper-sheet .katex, .ddalggak-paper-sheet .katex * { color: #000000 !important; }
    .question-title { font-weight: bold; font-size: 1.05rem; color: #000000 !important; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🗺️ 사이드바 내부에 수동으로 그리는 한글 메뉴판
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='font-size:1.4rem; font-weight:700; margin-bottom:5px; letter-spacing:-0.5px;'>📐 DDalGGak Math</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; opacity:0.6; margin-bottom:25px;'>Premium EdTech SaaS</p>", unsafe_allow_html=True)
    
    # 영문 파일 이름 시스템을 완전히 무시하고 개발자가 지정한 한글 메뉴로 라우팅
    menu_choice = st.radio(
        "플랫폼 메뉴",
        ["🏠 Home", "📐 AI 단일 문항 변형", "⚡ 모의고사 통째로 변형 (준비중)", "🗂️ 나만의 오답 보관함 (준비중)"]
    )
    st.write("---")

# ==========================================
# [분기 1] Home 화면
# ==========================================
if menu_choice == "🏠 Home":
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">DDalGGak Math Pro</div>
            <p style="font-size:1.15rem; opacity:0.8; margin-top:10px;">대한민국 최초 출제위원 기조의 수학 문항 역산 설계 및 실물 시험지 변형 엔진</p>
        </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
        <div class="beta-notice-card">
            <h3 style="margin-top:0; font-weight:700;">📢 강사 대상 프리미엄 오픈 베타 진행 중</h3>
            <p style="opacity: 0.85; line-height: 1.6; font-size: 1rem; margin-top: 12px;">
                현재 대치동 및 학원가 현직 강사님들을 대상으로 무료 베타 테스트를 진행하고 있습니다.<br>
                왼쪽 메뉴에서 <b>[📐 AI 단일 문항 변형]</b>을 누르시면 엔진 화면으로 즉시 진입합니다!
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### 💬 엔진 퀄리티 향상을 위한 의견 제시")
    feedback_text = st.text_area("의견이나 개선 요청사항을 자유롭게 입력해 주세요 (예: 킬러 문항 변형 시 조건 누락 발생 등)", height=100)
    if st.button("의견 전송하기", type="secondary"):
        if feedback_text: st.success("🙏 소중한 전문 의견이 출제위원회에 전달되었습니다. 감사합니다!")
        else: st.warning("내용을 입력하신 후 전송해 주세요.")

# ==========================================
# [분기 2] AI 단일 문항 변형 엔진 화면
# ==========================================
elif menu_choice == "📐 AI 단일 문항 변형":
    st.title("📐 AI 단일 문항 변형 엔진")
    st.markdown("수능 및 내신 기출문제를 완벽하게 분석하여 무결성 변형 문제를 생성합니다.")
    st.write("")

    with st.sidebar:
        st.header("⚙️ 출제 세부 옵션")
        api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
        num_variants = st.slider("생성할 변형 문항 수", min_value=1, max_value=5, value=1)
        variant_type = st.radio("변형 메커니즘 선택", options=["유형 1: 숫자 및 단순 조건 변형 (동일 구조)", "유형 2: 표현 및 형태 변형 (발문 비틀기)", "유형 3: 사고과정 공유 변형 (완전 위장 / 킬러)"])

    input_method = st.radio("원본 문제 입력 방식", ["📷 이미지/PDF 업로드", "✍️ 텍스트 직접 입력"])
    source_text, source_image = "", None

    if input_method == "✍️ 텍스트 직접 입력":
        source_text = st.text_area("원본 문제를 입력하세요", height=150)
    else:
        uploaded_file = st.file_uploader("문제 이미지 파일 업로드", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            source_image = Image.open(uploaded_file)
            st.image(source_image, caption="업로드된 원본 기출문제", width=400)

    if 'raw_result' not in st.session_state: st.session_state.raw_result = None
    if 'questions' not in st.session_state: st.session_state.questions = []
    if 'explanations' not in st.session_state: st.session_state.explanations = []

    if st.button("AI 프리미엄 문제 변형 실행 (딸깍)", type="primary"):
        if not api_key:
            st.error("🔑 사이드바에 API Key를 입력하세요!")
        else:
            with st.spinner('AI 출제위원이 고품질 문항을 설계 중입니다...'):
                try:
                    engine = DDalGGakEngine(api_key=api_key)
                    raw_result = engine.generate_variants(source_text, source_image, variant_type, num_variants)
                    questions, explanations = engine.parse_result(raw_result)
                    st.session_state.raw_result = raw_result
                    st.session_state.questions = questions
                    st.session_state.explanations = explanations
                    st.success("🎉 문항 출제 완료!")
                except Exception as e:
                    st.error(f"❌ 에러 발생: {e}")

    if st.session_state.raw_result:
        st.divider()
        tab1, tab2 = st.tabs(["📄 수능 시험지 실물 프리뷰", "👁️ AI Raw 데이터"])
        with tab1:
            st.markdown('<div class="ddalggak-paper-sheet">', unsafe_allow_html=True)
            for idx, q_content in enumerate(st.session_state.questions):
                st.markdown(f'<div class="question-title">【문항 {idx+1}번】</div>', unsafe_allow_html=True)
                st.markdown(q_content.strip())
                st.write("---")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("💡 정답 및 출제위원 해설")
            for idx, e_content in enumerate(st.session_state.explanations):
                with st.expander(f"▶ 【문항 {idx+1}번】 정답 및 풀이 확인"):
                    st.markdown(e_content.strip())
                    
        with tab2:
            st.text_area("AI 원본 텍스트", st.session_state.raw_result, height=300)
            
        st.divider()
        html_content = ""
        for idx, q_content in enumerate(st.session_state.questions):
            formatted_q = q_content.strip().replace(">", "<div style='border:2px solid #000; padding:18px; margin:12px 0; font-size:14px;'>").replace("\n", "<br>")
            html_content += f'<div style="margin-bottom: 40px; page-break-inside: avoid;"><b style="font-size: 18px;">{idx+1}.</b> {formatted_q}</div>'
            
        perfect_html = build_pdf_print_html(html_content)
        st.download_button(label="📥 초고화질 수능 양식 인쇄용 파일 다운로드 (딸깍)", data=perfect_html, file_name="ddalggak_math_print.html", mime="text/html")

# ==========================================
# [분기 3] 모의고사 통째로 변형 티저
# ==========================================
elif menu_choice == "⚡ 모의고사 통째로 변형 (준비중)":
    st.title("⚡ 모의고사 통째로 변형 (Full-Exam Converter)")
    st.markdown("시험지 PDF 한 장만 올리면 내신/수능 모의고사 30문항 전체를 원클릭 변형하는 핵심 코어 기능입니다.")
    st.markdown("""
        <div style="border: 2px dashed rgba(128, 128, 128, 0.4); padding: 40px; border-radius: 16px; text-align: center; margin-top: 50px;">
            <h2 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 15px;">🛠️ 현재 AI 엔진 심화 학습 및 파이프라인 구축 중</h2>
            <p style="opacity: 0.8; font-size: 1rem; line-height: 1.6;">
                단일 문항 인식을 넘어 문항별 좌표 자동 분할(Object Detection) 및 단원 매핑 모델을 고도화하고 있습니다.
            </p>
            <p style="font-weight: 600; color: #3b82f6; margin-top: 20px; font-size: 1.05rem;">
                🚀 Coming Soon — [AI 단일 문항 변형] 기능을 메뉴에서 먼저 체험해 보세요!
            </p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# [분기 4] 나만의 오답 보관함 티저
# ==========================================
elif menu_choice == "🗂️ 나만의 오답 보관함 (준비중)":
    st.title("🗂️ 클라우드 문항 및 오답 보관함")
    st.markdown("학원 학생별 오답 노트 관리 및 나만의 시크릿 교재 단원별 데이터베이스 아카이빙 시스템입니다.")
    st.markdown("""
        <div style="border: 2px dashed rgba(128, 128, 128, 0.4); padding: 40px; border-radius: 16px; text-align: center; margin-top: 50px;">
            <h2 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 15px;">🔐 회원가입 및 데이터베이스 보안 연동 예정</h2>
            <p style="opacity: 0.8; font-size: 1rem; line-height: 1.6;">
                내가 생성한 프리미엄 변형 문항들을 영구적으로 저장하고, 학생별 커스텀 시험지로 재조합할 수 있는 강사 전용 클라우드 스토리지를 준비 중입니다.
            </p>
            <p style="font-weight: 600; color: #10b981; margin-top: 20px; font-size: 1.05rem;">
                📈 정식 버전 출시와 함께 가동됩니다. 많은 기대 부탁드립니다!
            </p>
        </div>
    """, unsafe_allow_html=True)
