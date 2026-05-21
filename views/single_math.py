# views/single_math.py
import streamlit as st
from PIL import Image
import io
import base64
from ai_engine import DDalGGakEngine
from templates import build_pdf_print_html

# 🎨 [디자인 고도화] 라이트/다크모드 완벽 대응 및 사이드바 글씨 축소 커스텀 CSS
st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}
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

/* 📷 시험지 내부 원본 이미지 컨테이너 정밀 서식 */
.embedded-source-img {
    display: block;
    margin: 10px auto 25px auto;
    max-width: 100%;
    height: auto;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* 📐 [요구사항 반영] 왼쪽 사이드바 옵션 글씨 크기 정밀 축소 스킨 */
[data-testid="stSidebar"] {
    font-size: 0.88rem !important;      /* 기본 폰트 크기 축소 */
}
[data-testid="stSidebar"] h2 {
    font-size: 1.3rem !important;       /* DDalGGak Math 타이틀 크기 */
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] .stHeader {
    font-size: 1.05rem !important;      /* '출제 세부 옵션' 타이틀 크기 축소 */
    font-weight: 600 !important;
}
[data-testid="stSidebar"] label p {
    font-size: 0.85rem !important;      /* 슬라이더, 입력창 위 항목 이름 크기 축소 */
}
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
    font-size: 0.85rem !important;      /* '현재 위치' 및 기타 안내문 텍스트 크기 축소 */
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span p {
    font-size: 0.82rem !important;      /* 변형 메커니즘 라디오 버튼 보기 글씨 크기 축소 */
}
</style>
""", unsafe_allow_html=True)

# 🗺️ 사이드바 출제 세부 옵션 제어
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

# 세션 상태 초기화
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
        opened_image = Image.open(uploaded_file)
        st.session_state.saved_image = opened_image
        st.image(st.session_state.saved_image, caption="업로드된 원본 기출문제 (작업 대기 중)", width=400)

# 변형 실행 버튼 프로세스
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

# 📄 출력결과 렌더링 메커니즘
if st.session_state.raw_result:
    st.divider()
    tab1, tab2 = st.tabs(["📄 수능 시험지 실물 프리뷰", "👁️ AI Raw 데이터"])
    
    with tab1:
        st.markdown('<div class="ddalggak-paper-sheet">', unsafe_allow_html=True)
        
        # 업로드된 원본 이미지가 존재할 경우 Base64 인코딩하여 직접 주입
        if st.session_state.saved_image is not None:
            try:
                buffered = io.BytesIO()
                img_format = st.session_state.saved_image.format if st.session_state.saved_image.format else 'PNG'
                st.session_state.saved_image.save(buffered, format=img_format)
                img_str = base64.b64encode(buffered.getvalue()).decode()
                st.markdown(f'<img src="data:image/{img_format.lower()};base64,{img_str}" class="embedded-source-img" />', unsafe_allow_html=True)
            except Exception as img_err:
                st.warning(f"💡 원본 프리뷰 인코딩 유실 처리됨: {img_err}")
        
        # 생성된 변형 문제 순회
        for idx, q_content in enumerate(st.session_state.questions):
            st.markdown(f'<div class="question-title">【문항 {idx+1}번】</div>', unsafe_allow_html=True)
            st.markdown(q_content.strip())
            st.write("---")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 정답 및 해설 섹션
        st.subheader("💡 정답 및 출제위원 해설")
        for idx, e_content in enumerate(st.session_state.explanations):
            with st.expander(f"▶ 【문항 {idx+1}번】 정답 및 풀이 확인"):
                st.markdown(e_content.strip())
                
    with tab2:
        st.text_area("AI 원본 텍스트", st.session_state.raw_result, height=300)
        
    # 다운로드 파일 컴파일
    st.divider()
    html_content = ""
    
    if st.session_state.saved_image is not None:
        html_content += f'<div style="text-align:center; margin-bottom:30px;"><img src="data:image/{img_format.lower()};base64,{img_str}" style="max-width:100%; height:auto; border:1px solid #000;" /></div>'
        
    for idx, q_content in enumerate(st.session_state.questions):
        formatted_q = q_content.strip().replace(">", "<div style='border:2px solid #000; padding:18px; margin:12px 0; font-size:14px;'>").replace("\n", "<br>")
        html_content += f'<div style="margin-bottom: 40px; page-break-inside: avoid;"><b style="font-size: 18px;">{idx+1}.</b> {formatted_q}</div>'
        
    perfect_html = build_pdf_print_html(html_content)
    st.download_button(label="📥 초고화질 수능 양식 인쇄용 파일 다운로드 (딸깍)", data=perfect_html, file_name="ddalggak_math_print.html", mime="text/html")
