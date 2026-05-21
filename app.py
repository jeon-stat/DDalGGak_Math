# app.py
import streamlit as st
from PIL import Image
import requests
from datetime import datetime
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

st.set_page_config(
    page_title="DDalGGak Math Pro - 프리미엄 AI 수학 문제 변형 플랫폼",
    page_icon="📐",
    layout="wide"
)

# 🎨 [디자인 고도화] 라이트/다크모드 완벽 대응 및 미니멀 스킨 CSS
st.markdown("""
<style>
.stApp {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--background-color) !important;
    border-right: 2px solid rgba(128, 128, 128, 0.25) !important;
}

[data-testid="stSidebarNav"] {
    display: none !important;
}

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
</style>
""", unsafe_allow_html=True)

# 🗺️ 플랫폼 사이드바 메뉴 구성
with st.sidebar:
    st.markdown("<h2 style='font-size:1.4rem; font-weight:700; margin-bottom:5px; letter-spacing:-0.5px;'>📐 DDalGGak Math</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; opacity:0.6; margin-bottom:25px;'>Premium EdTech SaaS</p>", unsafe_allow_html=True)
    
    menu_choice = st.radio(
        "플랫폼 메뉴",
        ["🏠 Home", "📐 AI 단일 문항 변형", "⚡ 모의고사 통째로 변형 (준비중)", "🗂️ 나만의 오답 보관함 (준비중)"]
    )
    st.write("---")

# ==========================================
# [메뉴 1] 🏠 Home 화면 분기
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
        본 플랫폼의 AI 변형 출제 엔진은 구글의 Gemini API 기반으로 구동되므로, 원활한 사용을 위해 본인의 API Key 입력이 필요합니다.
    </p>
    <div class="api-guide-box">
        💡 <b>Gemini API Key가 없으신가요?</b><br>
        <a class="api-link" href="https://aistudio.google.com/" target="_blank">Google AI Studio (여기를 딸깍 클릭)</a>에 구글 계정으로 로그인하신 후, 
        <b>[Get API key]</b> 버튼을 누르면 10초 만에 무료 키를 발급받으실 수 있습니다.
    </div>
    <p style="font-weight: 600; margin-top: 15px; font-size: 1.05rem;">
        👈 Key를 발급받으신 후, 왼쪽 메뉴에서 <b>[📐 AI 단일 문항 변형]</b>을 누르고 사이드바 입력창에 붙여넣어 보세요!
    </p>
</div>
""", unsafe_allow_html=True)

    # 📝 [실시간 구글 시트 저장 핵심 파트] 
    st.write("")
    st.markdown("### 💬 엔진 퀄리티 향상을 위한 의견 제시")
    
    # 1. 홈페이지 화면 내부 사용자 정보 입력란 배치
    user_info_input = st.text_input(
        "강사 정보 입력", 
        placeholder="예시: 대치동 수학과 홍길동 팀장 / OO학원 원장"
    )
    
    feedback_text = st.text_area(
        "의견이나 개선 요청사항을 자유롭게 입력해 주세요 (예: 킬러 문항 변형 시 조건 누락 발생 등)", 
        height=100,
        placeholder="엔진 개선을 위한 소중한 한 줄 피드백을 남겨주세요."
    )
    
    if st.button("의견 전송하기", type="secondary"):
        if not feedback_text:
            st.warning("내용을 입력하신 후 전송해 주세요.")
        elif not user_info_input:
            st.warning("피드백 데이터베이스 관리를 위해 '강사 정보'를 먼저 입력해 주세요.")
        else:
            with st.spinner('구글 데이터베이스 시트에 안전하게 실시간 기록 중...'):
                
                # 지민님의 실제 구글 폼 백엔드 수집 주소 적용 완료
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfMMoBOa7hBNNpPcsMxePiXmAGfgI8eL20NK54p9rZv4usnvw/formResponse"
                
                # 추출한 entry ID 변수 매핑 완료
                payload = {
                    "entry.1056156260": feedback_text,     # 의견 내용 매핑
                    "entry.1147584167": user_info_input    # 강사 정보 매핑
                }
                
                try:
                    # 유저 화면 전환 없이 백엔드 전송 연동 실행
                    response = requests.post(form_url, data=payload)
                    if response.status_code == 200:
                        st.success(f"🎉 감사합니다, {user_info_input} 선생님! 소중한 피드백이 연동된 구글 시트에 실시간으로 즉시 기록되었습니다.")
                    else:
                        st.error("시트 전송 중 일시적인 서버 지연이 발생했습니다. 잠시 후 다시 시도해 주세요.")
                except Exception as e:
                    st.error(f"구글 시트 연동 오류 발생: {e}")

# ==========================================
# [메뉴 2] 📐 AI 단일 문항 변형 엔진 화면 분기
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
# [메뉴 3, 4] ⚡ 티저 및 대기 화면 분기
# ==========================================
elif menu_choice == "⚡ 모의고사 통째로 변형 (준비중)":
    st.title("⚡ 모의고사 통째로 변형")
    st.markdown("""
<div style="border: 2px dashed rgba(128, 128, 128, 0.4); padding: 40px; border-radius: 16px; text-align: center; margin-top: 50px;">
    <h2 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 15px;">🛠️ 현재 AI 엔진 심화 학습 및 파이프라인 구축 중</h2>
    <p style="opacity: 0.8; font-size: 1rem; line-height: 1.6;">단일 문항 인식을 넘어 문항별 좌표 자동 분할 및 단원 매핑 모델을 고도화하고 있습니다.</p>
</div>
""", unsafe_allow_html=True)

elif menu_choice == "🗂️ 나만의 오답 보관함 (준비중)":
    st.title("🗂️ 클라우드 문항 및 오답 보관함")
    st.markdown("""
<div style="border: 2px dashed rgba(128, 128, 128, 0.4); padding: 40px; border-radius: 16px; text-align: center; margin-top: 50px;">
    <h2 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 15px;">🔐 회원가입 및 데이터베이스 보안 연동 예정</h2>
    <p style="opacity: 0.8; font-size: 1rem; line-height: 1.6;">내가 생성한 프리미엄 변형 문항들을 영구적으로 저장하는 강사 전용 클라우드 스토리지를 준비 중입니다.</p>
</div>
""", unsafe_allow_html=True)
