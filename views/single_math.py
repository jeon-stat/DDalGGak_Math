# views/single_math.py
import streamlit as st
from PIL import Image
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

# 🎨 [디자인 고도화] 수능 시험지 템플릿 및 사이드바 컴팩트 서식
st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}
/* 📄 실제 AI 변형 문제만 들어갈 정갈한 수능 시험지 스타일 */
.ddalggak-paper-sheet { 
    background-color: #ffffff !important; 
    padding: 40px 45px; 
    border: 2px solid #000000 !important; 
    box-shadow: 0 12px 36px rgba(0,0,0,0.15); 
    font-family: 'Noto Serif KR', 'Batang', serif !important; 
    margin: 20px auto; 
    max-width: 800px; 
    border-radius: 4px; 
}
.ddalggak-paper-sheet * { color: #000000 !important; background-color: transparent !important; }
.ddalggak-paper-sheet blockquote { border: 2px solid #000000 !important; padding: 15px !important; margin: 12px 0 !important; }
.ddalggak-paper-sheet .katex, .ddalggak-paper-sheet .katex * { color: #000000 !important; }
.question-title { font-weight: bold; font-size: 1.05rem; color: #000000 !important; margin-bottom: 12px; }

/* 📐 왼쪽 사이드바 옵션 글씨 크기 축소 스킨 */
[data-testid="stSidebar"] { font-size: 0.88rem !important; }
[data-testid="stSidebar"] h2 { font-size: 1.3rem !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] .stHeader {
    font-size: 1.05rem !important; font-weight: 600 !important;
}
[data-testid="stSidebar"] label p { font-size: 0.85rem !important; }
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p { font-size: 0.85rem !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span p { font-size: 0.82rem !important; }
</style>
""", unsafe_allow_html=True)

# 🗺️ 사이드바 옵션 설정
with st.sidebar:
    st.markdown("<h2 style='font-size:1.4rem; font-weight:700; margin-bottom:5px;'>📐 DDalGGak Math</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; opacity:0.6; margin-bottom:25px;'>Premium EdTech SaaS</p>", unsafe_allow_html=True)
    st.write("현재 위치: **📐 단일 문항 변형**")
    
    st.divider() # 현재 위치 밑 분류 선
    
    st.header("⚙️ 출제 세부 옵션")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    num_variants = st.slider("생성할 변형 문항 수", min_value=1, max_value=5, value=1)
    variant_type = st.radio("변형 메커니즘 선택", options=["유형 1: 숫자 및 단순 조건 변형 (동일 구조)", "유형 2: 표현 및 형태 변형 (발문 비틀기)", "유형 3: 사고과정 공유 변형 (완전 위장 / 킬러)"])

st.title("📐 AI 단일 문항 변형 엔진")
st.markdown("수능 및 내신 기출문제를 완벽하게 분석하여 무결성 변형 문제를 생성합니다.")
st.write("")

input_method = st.radio("원본 문제 입력 방식", ["📷 이미지/PDF 업로드", "✍️ 텍스트 직접 입력"])

# 세션 상태 유지
if 'raw_result' not in st.session_state: st.session_state.raw_result = None
if 'questions' not in st.session_state: st.session_state.questions = []
if 'explanations' not in st.session_state: st.session_state.explanations = []
if 'saved_image' not in st.session_state: st.session_state.saved_image = None

source_text = ""
if input_method == "✍️ 텍스트 직접 입력":
    source_text = st.text_area("원본 문제를 입력하세요", height=150)
    st.session_state.saved_image = None
else:
    uploaded_file = st.file_uploader("문제 이미지 파일 업로드", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.session_state.saved_image = Image.open(uploaded_file)
        # 💡 원본 이미지는 왼쪽 메뉴판이나 메인 화면에 '작고 정갈하게(width=280)' 프리뷰로만 띄웁니다.
        st.image(st.session_state.saved_image, caption="🔍 업로드된 원본 기출문제", width=280)

# 변형 실행 버튼
if st.button("AI 프리미엄 문제 변형 실행 (딸깍)", type="primary"):
    if not api_key:
        st.error("🔑 사이드바에 API Key를 입력하세요!")
    else:
        with st.spinner('AI 출제위원이 고품질 문항을 설계 중입니다...'):
            try:
                engine = DDalGGakEngine(api_key=api_key)
                raw_result = engine.generate_variants(source_text, st.session_state.saved_image, variant_type, num_variants)
                questions, explanations = engine.parse_result(raw_result)
                
                st.session_state.raw_result = raw_result
                st.session_state.questions = questions
                st.session_state.explanations = explanations
                st.success("🎉 문항 출제 완료!")
            except Exception as e:
                st.error(f"❌ 에러 발생: {e}")

# 📄 결과 대시보드 렌더링
if st.session_state.raw_result:
    st.divider()
    tab1, tab2 = st.tabs(["📄 수능 시험지 실물 프리뷰", "👁️ AI Raw 데이터"])
    
    with tab1:
        # 💡 버그 해결: 하얀 종이 틀 안에는 원본 이미지 주입 코드를 완전히 제거했습니다.
        # 이 박스 내부에는 오직 AI가 완전히 새로 출제한 변형 문제만 텍스트/LaTeX로 렌더링됩니다.
        st.markdown('<div class="ddalggak-paper-sheet">', unsafe_allow_html=True)
        
        for idx, q_content in enumerate(st.session_state.questions):
            st.markdown(f'<div class="question-title">【변형 문항 {idx+1}번】</div>', unsafe_allow_html=True)
            st.markdown(q_content.strip(), unsafe_allow_html=True)
            st.write("---")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 정답 및 해설지 섹션
        st.subheader("💡 정답 및 출제위원 해설")
        for idx, e_content in enumerate(st.session_state.explanations):
            with st.expander(f"▶ 【변형 문항 {idx+1}번】 정답 및 풀이 확인"):
                st.markdown(e_content.strip())
                
    with tab2:
        st.text_area("AI 원본 텍스트", st.session_state.raw_result, height=300)
        
    # 다운로드 파일 컴파일 (인쇄용 파일 전용)
    st.divider()
    html_content = ""
    for idx, q_content in enumerate(st.session_state.questions):
        formatted_q = q_content.strip().replace(">", "<div style='border:2px solid #000; padding:18px; margin:12px 0; font-size:14px;'>").replace("\n", "<br>")
        html_content += f'<div style="margin-bottom: 40px; page-break-inside: avoid;"><b style="font-size: 18px;">{idx+1}.</b> {formatted_q}</div>'
        
    perfect_html = build_pdf_print_html(html_content)
    st.download_button(label="📥 초고화질 수능 양식 인쇄용 파일 다운로드 (딸깍)", data=perfect_html, file_name="ddalggak_math_print.html", mime="text/html")
