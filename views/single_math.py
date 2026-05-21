# views/single_math.py
import streamlit as st
from PIL import Image
import io
import base64
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

# 🎨 [디자인 고도화] 라이트/다크모드 완벽 대응 및 사이드바 글씨 축소 CSS
st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}
/* 📄 수능 시험지 실제 문항이 들어갈 깔끔한 종이 프레임 */
.ddalggak-paper-sheet { 
    background-color: #ffffff !important; 
    padding: 45px 55px; 
    border: 2px solid #000000 !important; 
    box-shadow: 0 20px 50px -12px rgba(0,0,0,0.15); 
    font-family: 'Noto Serif KR', 'Batang', serif !important; 
    margin: 25px auto; 
    max-width: 820px; 
    border-radius: 4px; 
}
.ddalggak-paper-sheet * { color: #000000 !important; background-color: transparent !important; }
.ddalggak-paper-sheet blockquote { border: 2px solid #000000 !important; padding: 20px !important; margin: 15px 0 !important; }
.ddalggak-paper-sheet .katex, .ddalggak-paper-sheet .katex * { color: #000000 !important; }
.question-title { font-weight: bold; font-size: 1.05rem; color: #000000 !important; margin-bottom: 12px; }

/* 📐 왼쪽 사이드바 옵션 글씨 크기 축소 */
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

# 🗺️ 사이드바 컨트롤러
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

# 세션 상태 무결성 보장 로직
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

# 원본 이미지가 존재할 때 화면에 과도하게 크지 않도록 300픽셀 크기로 정갈하게 인덱싱 노출
if st.session_state.saved_image is not None:
    st.image(st.session_state.saved_image, caption="📷 내가 업로드한 원본 기출문제", width=300)

# 변형 실행 트리거
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

# 📄 [구조 대개혁] 흰색 상자 대참사의 주범이었던 st.tabs를 완전히 제거하고 레이아웃 전면 수정
if st.session_state.raw_result:
    st.divider()
    
    # 1. 수능 시험지 프리뷰 렌더링 영역 (흰색 박스 버그 전면 박멸)
    st.subheader("📄 수능 시험지 실물 프리뷰")
    st.markdown('<div class="ddalggak-paper-sheet">', unsafe_allow_html=True)
    for idx, q_content in enumerate(st.session_state.questions):
        st.markdown(f'<div class="question-title">【변형 문항 {idx+1}번】</div>', unsafe_allow_html=True)
        st.markdown(q_content.strip(), unsafe_allow_html=True)
        st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. 정답 및 출제위원 해설 영역
    st.subheader("💡 정답 및 출제위원 해설")
    for idx, e_content in enumerate(st.session_state.explanations):
        with st.expander(f"▶ 【변형 문항 {idx+1}번】 정답 및 풀이 확인"):
            st.markdown(e_content.strip())
            
    # 3. 데이터 추적용 AI Raw 데이터 영역 (하단 접이식 보관함으로 격리하여 가독성 업그레이드)
    st.write("")
    with st.expander("👁️ AI Raw 데이터 확인 (개발 및 검증용)"):
        st.text_area("AI 원본 텍스트", st.session_state.raw_result, height=250)
        
    # 4. 파일 컴파일 및 인쇄 버튼 다운로더
    st.divider()
    html_content = ""
    for idx, q_content in enumerate(st.session_state.questions):
        formatted_q = q_content.strip().replace(">", "<div style='border:2px solid #000; padding:18px; margin:12px 0; font-size:14px;'>").replace("\n", "<br>")
        html_content += f'<div style="margin-bottom: 40px; page-break-inside: avoid;"><b style="font-size: 18px;">{idx+1}.</b> {formatted_q}</div>'
        
    perfect_html = build_pdf_print_html(html_content)
    st.download_button(label="📥 초고화질 수능 양식 인쇄용 파일 다운로드 (딸깍)", data=perfect_html, file_name="ddalggak_math_print.html", mime="text/html")
