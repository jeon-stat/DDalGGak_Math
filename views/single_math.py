# views/single_math.py
import streamlit as st
from PIL import Image
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

# 🎨 [디자인 대개혁] 외부 CSS 충돌을 원천 차단하는 독립형 프리미엄 수능 시험지 스킨
st.markdown("""
<style>
/* 기본 인풋 컴포넌트 스타일링 */
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}

/* 📄 [핵심 보정] 흰색 박스 버그를 전면 박멸하고 실제 수능 시험지 느낌을 구현한 프레임 */
.premium-paper-container {
    background-color: #ffffff !important;
    color: #000000 !important;
    padding: 40px 50px;
    border: 2px solid #000000 !important;
    box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    font-family: 'Noto Serif KR', 'Batang', serif !important;
    margin: 20px auto;
    max-width: 800px;
    border-radius: 2px;
    line-height: 1.7;
}

/* 시험지 내부의 모든 텍스트와 수식을 강제로 검은색 수능 시험지 서식으로 통일 */
.premium-paper-container * {
    color: #000000 !important;
    background-color: transparent !important;
}

.premium-paper-container p, .premium-paper-container div {
    color: #000000 !important;
    font-size: 1.05rem !important;
    letter-spacing: -0.5px;
}

.premium-variant-title {
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    color: #000000 !important;
    margin-bottom: 14px;
    border-bottom: 1px solid #000000;
    padding-bottom: 4px;
    display: inline-block;
}

/* 📐 왼쪽 사이드바 옵션 글씨 크기 오밀조밀하게 축소 */
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

# 🗺️ 사이드바 컨트롤러 파트
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

# 세션 무결성 로직 고정
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

# 업로드한 원본 파일 컴팩트 프리뷰 (바깥에 배치)
if st.session_state.saved_image is not None:
    st.image(st.session_state.saved_image, caption="📷 내가 업로드한 원본 기출문제", width=300)

# 변형 실행 버튼 딸깍
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

# 📄 [완벽 보정 실행] 변형 문항 노출 메커니즘
if st.session_state.raw_result:
    st.divider()
    
    st.subheader("📄 수능 시험지 실물 프리뷰")
    
    # 💡 흰색 박스를 유발하던 과거의 div 클래스명을 버리고, 강제로 완전 독립된 프리미엄 스타일로 렌더링
    for idx, q_content in enumerate(st.session_state.questions):
        st.markdown(f"""
        <div class="premium-paper-container">
            <div class="premium-variant-title">【변형 문항 {idx+1}번】</div>
            <div style="color: #000000 !important;">{q_content.strip()}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # 정답 및 출제위원 해설 영역
    st.write("")
    st.subheader("💡 정답 및 출제위원 해설")
    for idx, e_content in enumerate(st.session_state.explanations):
        with st.expander(f"▶ 【변형 문항 {idx+1}번】 정답 및 풀이 확인"):
            st.markdown(e_content.strip())
            
    # 개발 및 디버깅 검증용 보관함
    st.write("")
    with st.expander("👁️ AI Raw 데이터 확인 (개발 및 검증용)"):
        st.text_area("AI 원본 텍스트", st.session_state.raw_result, height=200)
        
    # 초고화질 다운로드 엔진 가동
    st.divider()
    html_content = ""
    for idx, q_content in enumerate(st.session_state.questions):
        formatted_q = q_content.strip().replace(">", "<div style='border:2px solid #000; padding:18px; margin:12px 0; font-size:14px;'>").replace("\n", "<br>")
        html_content += f'<div style="margin-bottom: 40px; page-break-inside: avoid;"><b style="font-size: 18px;">{idx+1}.</b> {formatted_q}</div>'
        
    perfect_html = build_pdf_print_html(html_content)
    st.download_button(label="📥 초고화질 수능 양식 인쇄용 파일 다운로드 (딸깍)", data=perfect_html, file_name="ddalggak_math_print.html", mime="text/html")
