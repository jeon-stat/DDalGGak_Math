# pages/DDalGGak_Math.py
import streamlit as st
from PIL import Image
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

st.set_page_config(page_title="DDalGGak Math 출제 엔진", page_icon="📐", layout="wide")

# 🎨 내부 도구창도 다크/라이트에 따라 가변 텍스트 필드를 적용하되, '시험지 프리뷰'만큼은 무조건 백색 용지로 고정
st.markdown("""
    <style>
    /* 전체 기본 시스템 자동 연동 */
    .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stHeader"] {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }
    [data-testid="stSidebar"] {
        background-color: var(--background-color) !important;
        border-right: 1px solid rgba(128, 128, 128, 0.1) !important;
    }
    
    /* 인풋 박스 배경 및 테두리 유연화 (다크모드 시 어두운 계열 인풋으로 자동 호환) */
    .stTextArea textarea, .stTextInput input, .stSelectbox div {
        background-color: var(--background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        color: var(--text-color) !important;
        border-radius: 8px !important;
    }
    
    /* 📄 [절대 규칙] 실물 시험지 렌더링 박스는 다크모드여도 '무조건 새하얀 종이' 형태 고정 */
    .ddalggak-paper-sheet {
        background-color: #ffffff !important;
        padding: 45px 55px;
        border: 1px solid #0f172a !important;
        box-shadow: 0 20px 50px -12px rgba(0,0,0,0.15);
        font-family: 'Noto Serif KR', 'Batang', serif !important;
        margin: 30px auto;
        max-width: 860px;
        border-radius: 4px;
    }
    /* 시험지 내부 텍스트 및 기호는 강제로 올 블랙 처리 */
    .ddalggak-paper-sheet * { color: #000000 !important; background-color: transparent !important; }
    .ddalggak-paper-sheet blockquote { border: 1px solid #000000 !important; padding: 20px !important; margin: 15px 0 !important; }
    .ddalggak-paper-sheet .katex, .ddalggak-paper-sheet .katex * { color: #000000 !important; }
    .question-title { font-weight: bold; font-size: 1.05rem; color: #000000 !important; margin-bottom: 12px; }
    
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid rgba(128, 128, 128, 0.15) !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📐 DDalGGak Math 출제 엔진")
st.markdown("수능 및 내신 기출문제를 완벽하게 분석하여 무결성 변형 문제를 생성합니다.")

# 사이드바 제어 패널
with st.sidebar:
    st.header("⚙️ 딸깍 출제 옵션")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    num_variants = st.slider("생성할 변형 문항 수", min_value=1, max_value=5, value=1)
    variant_type = st.radio("변형 메커니즘 선택", options=["유형 1: 숫자 및 단순 조건 변형 (동일 구조)", "유형 2: 표현 및 형태 변형 (발문 비틀기)", "유형 3: 사고과정 공유 변형 (완전 위장 / 킬러)"])

# 입력 UI
input_method = st.radio("원본 문제 입력 방식", ["📷 이미지/PDF 업로드", "✍️ 텍스트 직접 입력"])
source_text, source_image = "", None

if input_method == "✍️ 텍스트 직접 입력":
    source_text = st.text_area("원본 문제를 입력하세요", height=150)
else:
    uploaded_file = st.file_uploader("문제 이미지 파일 업로드", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        source_image = Image.open(uploaded_file)
        st.image(source_image, caption="업로드된 원본 기출문제", width=400)

# 세션 상태 세팅
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

# 결과 출력 뷰어
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
        formatted_q = q_content.strip().replace(">", "<div style='border:1px solid #000; padding:15px; margin:10px 0; font-size:14px;'>").replace("\n", "<br>")
        html_content += f'<div style="margin-bottom: 40px; page-break-inside: avoid;"><b style="font-size: 18px;">{idx+1}.</b> {formatted_q}</div>'
        
    perfect_html = build_pdf_print_html(html_content)
    st.download_button(label="📥 초고화질 수능 양식 인쇄용 파일 다운로드 (딸깍)", data=perfect_html, file_name="ddalggak_math_print.html", mime="text/html")
