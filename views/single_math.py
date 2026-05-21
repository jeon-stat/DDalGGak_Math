# views/single_math.py
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import google.generativeai as genai
import re

# 🎨 기본 UI 컴포넌트 간결화 스킨 CSS
st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
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

# 🗺️ 사이드바 컨트롤러 메뉴
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

# 세션 상태 초기화 (2번 요구사항: 시스템 내부에 완벽한 문법 자산을 유지하기 위함)
if 'raw_result' not in st.session_state: st.session_state.raw_result = None
if 'questions' not in st.session_state: st.session_state.questions = []
if 'explanations' not in st.session_state: st.session_state.explanations = []

# [1단계: 문제 생성 및 무결성 변형 수집]
if st.button("AI 프리미엄 문제 변형 실행 (딸깍)", type="primary"):
    if not api_key:
        st.error("🔑 사이드바에 API Key를 입력하세요!")
    else:
        with st.spinner('AI 출제위원이 고품질 문항을 설계 중입니다...'):
            try:
                genai.configure(api_key=api_key)
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
                if source_image is not None: contents.append(source_image)
                contents.append(prompt)
                
                response = model.generate_content(contents)
                raw_result = response.text
                
                q_pattern = re.compile(r'\[QUESTION_START\](.*?)\[QUESTION_END\]', re.DOTALL)
                e_pattern = re.compile(r'\[EXPLANATION_START\](.*?)\[EXPLANATION_END\]', re.DOTALL)
                
                raw_questions = q_pattern.findall(raw_result)
                raw_explanations = e_pattern.findall(raw_result)
                
                # [2단계: 언제든 한글/워드로 변환 가능한 독립형 수식 자산(LaTeX 목록) 확보 완료]
                st.session_state.questions = [q.strip() for q in raw_questions]
                st.session_state.explanations = [e.strip() for e in raw_explanations]
                st.session_state.raw_result = raw_result
                st.success("🎉 문항 출제 완료!")
            except Exception as e:
                st.error(f"❌ 에러 발생: {e}")

# [3단계: 실제 시험지와 완벽히 일치하는 초고화질 미러링 프리뷰 렌더링 기믹]
if st.session_state.raw_result:
    st.divider()
    st.subheader("📄 수능 시험지 실물 프리뷰")
    
    # 가상 샌드박스 내부에 수능 전용 폰트, 인쇄용 흰색 바탕, 실시간 수식 렌더러(KaTeX) 배치
    html_iframe_body = ""
    for idx, q_content in enumerate(st.session_state.questions):
        # 마크다운 문법 찌꺼기 방어선 구축
        clean_q = q_content.replace("**", "").replace("###", "")
        html_iframe_body += f"""
        <div class="exam-question-box">
            <span class="exam-number">{idx+1}.</span>
            <div class="exam-text">{clean_q}</div>
        </div>
        """
        
    # 가상 시험지 완벽 컴파일 (CSS 충돌 완벽 차단용 독립 패키지 타겟팅)
    preview_sandbox_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: #ffffff !important;
                color: #000000 !important;
                margin: 0;
                padding: 30px 35px;
                font-family: 'Noto Serif KR', 'Batang', serif !important;
                font-size: 14.5px;
                line-height: 1.75;
            }}
            .exam-question-box {{
                margin-bottom: 40px;
                display: flex;
                align-items: flex-start;
            }}
            .exam-number {{
                font-weight: 800;
                font-size: 16px;
                margin-right: 8px;
                user-select: none;
            }}
            .exam-text {{
                width: 100%;
                word-break: break-all;
            }}
            blockquote {{
                border: 1.5px solid #000000 !important;
                padding: 15px !important;
                margin: 12px 0 !important;
                font-size: 13.5px;
            }}
        </style>
    </head>
    <body>
        {html_iframe_body}
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: "$$", right: "$$", display: true}},
                        {{left: "$", right: "$", display: false}}
                    ],
                    throwOnError : false
                }});
            });
        </script>
    </body>
    </html>
    """
    
    # 💡 [버그 종결] 코드가 튀어나오는 현상을 막고 실제 완벽한 시험지 모양의 독립 컴포넌트 렌더링 실행
    components.html(preview_sandbox_html, height=450, scrolling=True)
    
    # [2번 심화 파트: 선생님들을 위한 한글/워드 원본 서식 추출 다운로드 링크]
    st.divider()
    st.subheader("📥 다운로드 및 파일 편집용 문법 자산")
    
    # 선생님들이 그대로 복사해서 한글(HWP) 수식 편집기나 워드에 다이렉트로 붙여넣기 할 수 있는 날것의 텍스트 자산 제공
    raw_hwp_text = ""
    for idx, q_content in enumerate(st.session_state.questions):
        raw_hwp_text += f"[{idx+1}번 변형문제]\n{q_content}\n\n"
        
    st.info("💡 아래 상자의 수식 데이터를 복사하면, 한글(HWP) 및 Word 수식 입력기와 100% 호환되어 교재 편집이 즉시 가능합니다.")
    st.text_area("선생님 편집용 수식 텍스트 (전체 복사 가능)", value=raw_hwp_text.strip(), height=150)

    # 정답 및 해설 섹션
    st.write("")
    st.subheader("💡 정답 및 출제위원 해설")
    for idx, e_content in enumerate(st.session_state.explanations):
        with st.expander(f"▶ 【변형 문항 {idx+1}번】 정답 및 풀이 확인"):
            st.markdown(e_content.strip())
