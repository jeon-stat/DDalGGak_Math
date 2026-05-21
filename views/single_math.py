# views/single_math.py
import streamlit as st
from PIL import Image
import google.generativeai as genai
import json
import re

# 🎨 라이트/다크모드 완벽 대응 및 수능 시험지 양식 프레임 CSS
st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}
/* 📄 수능 시험지 전용 독립 프리프레임 */
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

/* 📐 왼쪽 사이드바 옵션 글씨 크기 정밀 축소 스킨 */
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

# 🗺️ 사이드바 옵션 및 컨트롤러 메뉴
with st.sidebar:
    st.markdown("<h2 style='font-size:1.4rem; font-weight:700; margin-bottom:5px;'>📐 DDalGGak Math</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; opacity:0.6; margin-bottom:25px;'>Premium EdTech SaaS</p>", unsafe_allow_html=True)
    st.write("현재 위치: **📐 단일 문항 변형**")
    
    st.divider()
    
    st.header("⚙️ 출제 세부 옵션")
    api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    num_variants = st.slider("생성할 변형 문항 수", min_value=1, max_value=5, value=1)
    variant_type = st.radio("변형 메커니즘 선택", options=["유형 1: 숫자 및 단순 조건 변형 (동일 구조)", "유형 2: 표현 및 형태 변형 (발문 비틀기)", "유형 3: 사고과정 공유 변형 (완전 위장 / 킬러)"])

st.title("📐 AI 단일 문항 변형 엔진")
st.markdown("수능 및 내신 기출문제를 완벽하게 분석하여 무결성 변형 문제를 생성합니다.")
st.write("")

input_method = st.radio("원본 문제 입력 방식", ["📷 이미지/PDF 업로드", "✍️ 텍스트 직접 입력"])
source_text, source_image = "", None

if input_method == "✍️ 텍스트 직접 입력":
    source_text = st.text_area("원본 문제를 입력하세요", height=150)
else:
    uploaded_file = st.file_uploader("문제 이미지 파일 업로드", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        source_image = Image.open(uploaded_file)
        st.image(source_image, caption="업로드된 원본 기출문제", width=280)

# 세션 상태 메모리 방어선 초기화
if 'raw_result' not in st.session_state: st.session_state.raw_result = None
if 'questions' not in st.session_state: st.session_state.questions = []
if 'explanations' not in st.session_state: st.session_state.explanations = []

# 변형 실행 메인 스케줄러
if st.button("AI 프리미엄 문제 변형 실행 (딸깍)", type="primary"):
    if not api_key:
        st.error("🔑 사이드바에 API Key를 입력하세요!")
    else:
        with st.spinner('AI 출제위원이 고품질 문항을 설계 중입니다...'):
            try:
                genai.configure(api_key=api_key)
                # 🛠️ 할당량 차단 에러(429)를 방지하기 위해 속도가 빠르고 제한이 널널한 flash 모델로 세팅
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
당신은 대한민국 한국교육과정평가원 수학 출제위원 기조의 최고 전문가 AI입니다.
입력된 수학 문제를 분석하여, 지정된 '변형 메커니즘' 옵션 조건에 맞는 최상위 무결성 변형 문항을 출제하십시오.

[출제 요구 사양]
- 생성 문항 수: {num_variants}개
- 선택된 변형 메커니즘: {variant_type}

★ 메커니즘별 변형 가이드라인 ★
1. "유형 1: 숫자 및 단순 조건 변형 (동일 구조)" 선택 시:
   - 문제의 상황, 발문 구조, 대수적/기하학적 핵심 성질은 원본과 완벽히 일치해야 합니다.
   - 오직 상수, 함수식의 계수 등 숫자 데이터만 치환하십시오.
   - 단, 치환된 숫자로 인해 정답이 분수나 무리수로 깨지지 않고, 깔끔한 '정수 또는 유리수'로 떨어지도록 역산 설계하십시오.

2. "유형 2: 표현 및 형태 변형 (발문 비틀기)" 선택 시:
   - 원본 문항과 수학적 본질(동일 단원, 동일 행동영역)은 공유해야 합니다.
   - 다만 발문 스타일을 완전히 새롭게 비틀어 표현하십시오. (예: 최댓값 구하기를 '합성함수가 불연속이 되는 점의 개수' 또는 박스형 보기 조건으로 위장)

3. "유형 3: 사고과정 공유 변형 (완전 위장 / 킬러)" 선택 시:
   - 원본의 구체적인 수식이나 대수 구조를 절대로 그대로 복사해 쓰지 마십시오.
   - 원본 킬러 문항이 내포한 고난도 사고과정(예: 대칭성을 이용한 추론, 케이스 분류 메커니즘 등)만 핵심 논리로 상속받으십시오.
   - 완전히 초면인 새로운 지수/로그/삼각함수 합성식을 설계하여 외관상 100% 다른 신작 문항처럼 위장하십시오.

[입력 데이터]
텍스트: {source_text}

----------------------------------------------------------------------
[출력 데이터 프로토콜 포맷]
반드시 프론트엔드 파서 규칙을 준수하여 다른 인사말 없이 아래 태그 구조로만 일반 텍스트 답변을 출력하십시오.

[QUESTION_START]
(여기에 변형된 문항 발문을 작성하십시오. 수식은 무조건 LaTeX 기호인 $...$ 또는 $$...$$로 감싸야 합니다.)
[QUESTION_END]
[EXPLANATION_START]
(여기에 정답 및 단계별 해설을 작성하십시오. 수식은 LaTeX 필수.)
[EXPLANATION_END]

문항 수 조건이 {num_variants}개이므로, 위 세트를 총 {num_variants}번 반복하여 렌더링하십시오.
"""
                contents = []
                if source_image is not None:
                    contents.append(source_image)
                contents.append(prompt)
                
                response = model.generate_content(contents)
                raw_result = response.text
                
                # 텍스트 파싱 처리
                q_pattern = re.compile(r'\[QUESTION_START\](.*?)\[QUESTION_END\]', re.DOTALL)
                e_pattern = re.compile(r'\[EXPLANATION_START\](.*?)\[EXPLANATION_END\]', re.DOTALL)
                
                raw_questions = q_pattern.findall(raw_result)
                raw_explanations = e_pattern.findall(raw_result)
                
                questions = [q.strip() for q in raw_questions]
                explanations = [e.strip() for e in raw_explanations]
                
                if not questions:
                    questions.append(raw_result)
                    explanations.append("해설 분리 실패 - Raw 데이터 참조")
                    
                st.session_state.raw_result = raw_result
                st.session_state.questions = questions
                st.session_state.explanations = explanations
                st.success("🎉 문항 출제 완료!")
            except Exception as e:
                st.error(f"❌ 에러 발생: {e}")

# 📄 최종 결과 렌더링 파트
if st.session_state.raw_result:
    st.divider()
    
    st.subheader("📄 수능 시험지 실물 프리뷰")
    st.markdown('<div class="ddalggak-paper-sheet">', unsafe_allow_html=True)
    for idx, q_content in enumerate(st.session_state.questions):
        st.markdown(f'<div class="question-title">【변형 문항 {idx+1}번】</div>', unsafe_allow_html=True)
        st.markdown(q_content.strip(), unsafe_allow_html=True)
        st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("💡 정답 및 출제위원 해설")
    for idx, e_content in enumerate(st.session_state.explanations):
        with st.expander(f"▶ 【변형 문항 {idx+1}번】 정답 및 풀이 확인"):
            st.markdown(e_content.strip())
            
    st.write("")
    with st.expander("👁️ AI Raw 데이터 확인 (개발 및 검증용)"):
        st.text_area("AI 원본 텍스트", st.session_state.raw_result, height=200)
