# pages/DDalGGak_Math.py
import streamlit as st
from PIL import Image
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

st.set_page_config(page_title="DDalGGak Math 출제 엔진", page_icon="📐", layout="wide")

# 🎨 [라인 강화 버전] 인풋 테두리와 실물 시험지 <보기> 박스 선 두께 대폭 업그레이드 CSS
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
    
    /* 입력 폼 박스들의 테두리선 두께를 1.5px로 늘려 가시성 확보 */
    .stTextArea textarea, .stTextInput input, .stSelectbox div {
        background-color: var(--background-color) !important;
        border: 1.5px solid rgba(128, 128, 128, 0.3) !important;
        color: var(--text-color) !important;
        border-radius: 8px !important;
    }
    
    /* 📄 실제 수능 시험지 용지 박스 테두리선 강화 (1px -> 2px) */
    .ddalggak-paper-sheet {
        background-color: #ffffff !important;
        padding: 45px 55px;
        border: 2px solid #000000 !important; /* 묵직한 수능지 외곽선 고정 */
        box-shadow: 0 20px 50px -12px rgba(0,0,0,0.15);
        font-family: 'Noto Serif KR', 'Batang', serif !important;
        margin: 30px auto;
        max-width: 860px;
        border-radius: 4px;
    }
    .ddalggak-paper-sheet * { color: #000000 !important; background-color: transparent !important; }
    
    /* ★핵심 반영★ 수능 기출 특유의 사각형 <보기> 박스 테두리를 2px 사방 실선으로 묵직하게 고정 */
    .ddalggak-paper-sheet blockquote { 
        border: 2px solid #000000 !important; 
        padding: 22px !important; 
        margin: 18px 0 !important; 
    }
    
    .ddalggak-paper-sheet .katex, .ddalggak-paper-sheet .katex * { color: #000000 !important; }
    .question-title { font-weight: bold; font-size: 1.05rem; color: #000000 !important; margin-bottom: 12px; }
    
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid rgba(128, 128, 128, 0.2) !important; }
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
        # 다운로드용 인쇄 파일 내부의 보기 박스 테두리선도 두껍게 연동 치환
        formatted_q = q_content.strip().replace(">", "<div style='border:2px solid #000; padding:18px; margin:12px 0; font-size:14px;'>").replace("\n", "<br>")
        html_content += f'<div style="margin-bottom: 40px; page-break-inside: avoid;"><b style="font-size: 18px;">{idx+1}.</b> {formatted_q}</div>'
        
    perfect_html = build_pdf_print_html(html_content)
    st.download_button(label="📥 초고화질 수능 양식 인쇄용 파일 다운로드 (딸깍)", data=perfect_html, file_name="ddalggak_math_print.html", mime="text/html")
