# views/single_math.py
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import google.generativeai as genai
import re

# 🎨 UI 및 사이드바 컴팩트 스타일
st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}
[data-testid="stSidebar"] { font-size: 0.85rem !important; }
[data-testid="stSidebar"] h2 { font-size: 1.2rem !important; }
[data-testid="stSidebar"] .stHeader { font-size: 0.95rem !important; font-weight: 600 !important; }

/* 💡 프리뷰 중앙 정렬 및 테두리 스킨 */
iframe { display: block; margin: 0 auto !important; border: 1px solid rgba(128,128,128,0.2) !important; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0;'>📐 DDalGGak Math</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; opacity:0.6; margin-bottom:20px;'>Premium EdTech SaaS</p>", unsafe_allow_html=True)
    st.write("현재 위치: **🏠 Home > 📐 변형**")
    st.divider()
    st.header("⚙️ 출제 옵션")
    api_key = st.text_input("Gemini API Key", type="password")
    num_variants = st.slider("문항 수", 1, 5, 1)
    variant_type = st.radio("변형 유형", ["유형 1: 숫자 변형", "유형 2: 발문 비틀기", "유형 3: 킬러 위장"])

st.title("📐 AI 단일 문항 변형 엔진")
st.write("")

input_method = st.radio("입력 방식", ["📷 이미지 업로드", "✍️ 직접 입력"])
source_text, source_image = "", None

if input_method == "✍️ 직접 입력":
    source_text = st.text_area("원본 문제 입력", height=150)
else:
    uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        source_image = Image.open(uploaded_file)
        st.image(source_image, caption="원본 기출문제 프리뷰", width=280)

# 세션 상태 강제 고정
if 'qs' not in st.session_state: st.session_state.qs = []
if 'es' not in st.session_state: st.session_state.es = []
if 'res' not in st.session_state: st.session_state.res = None

# 1. 문제 생성 로직
if st.button("AI 변형 실행 (딸깍)", type="primary"):
    if not api_key:
        st.error("사이드바에 API Key를 입력하세요.")
    else:
        with st.spinner('출제 중...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # 💡 [프롬프트 개혁] 5지선다 선지 출력 및 컴팩트한 Step-by-Step 해설 가이드라인 주입
                p = "당신은 수능 수학 출제위원입니다. 다음 원본 문제를 변형하여 '5지선다형 객관식' 문항을 출제하십시오.\n" \
                    "문항 수: " + str(num_variants) + "\n" \
                    "유형: " + variant_type + "\n\n" \
                    "⚠️ [중요 준수 사항] ⚠️\n" \
                    "1. 수식은 무조건 $...$로 감싸고 LaTeX 문법을 사용하십시오.\n" \
                    "2. 문제의 발문과 조건, 그리고 ①~⑤ 선지 전체를 [QUESTION_START] 토큰 안에 모두 포함시키십시오.\n" \
                    "3. 정답과 단계별 풀이 과정을 [EXPLANATION_START] 토큰 안에 포함시키십시오.\n\n" \
                    "[출력 프로토콜 데이터 형식 예시]\n" \
                    "[QUESTION_START]\n" \
                    "(여기에 문제 발문과 조건 제시)\n" \
                    "$$ f(x) = ... $$\n\n" \
                    "① $ 10 $ ② $ 20 $ ③ $ 30 $ ④ $ 40 $ ⑤ $ 50 $\n" \
                    "[QUESTION_END]\n\n" \
                    "[EXPLANATION_START]\n" \
                    "**[정답]** ⑤\n\n" \
                    "**[출제 의도]** (개념 및 추론 핵심 한 줄 요약)\n\n" \
                    "**[단계별 풀이]**\n" \
                    "- **Step 1:** (조건 분석 및 첫 수식 전개)\n" \
                    "- **Step 2:** (핵심 뼈대 연산 및 케이스 분류)\n" \
                    "- **Step 3:** (최종 답 도출)\n" \
                    "⚠️ 줄글로 길게 늘어놓지 말고, 수식과 지시어를 활용해 핵심 연산 흐름만 컴팩트하게 압축하십시오.\n" \
                    "[EXPLANATION_END]\n\n" \
                    "원본 데이터: " + source_text

                contents = [source_image, p] if source_image else [p]
                response = model.generate_content(contents)
                full_text = response.text
                
                # 정규표현식 파싱
                qs = re.findall(r'\[QUESTION_START\](.*?)\[QUESTION_END\]', full_text, re.DOTALL)
                es = re.findall(r'\[EXPLANATION_START\](.*?)\[EXPLANATION_END\]', full_text, re.DOTALL)
                
                st.session_state.qs = [q.strip() for q in qs]
                st.session_state.es = [e.strip() for e in es]
                st.session_state.res = full_text
                st.success("출제 완료!")
            except Exception as e:
                st.error("오류: " + str(e))

# 2. 결과 렌더링
if st.session_state.res:
    st.divider()
    st.subheader("📄 수능 시험지 실물 프리뷰")
    
    html_body = ""
    for idx, q in enumerate(st.session_state.qs):
        # 마크다운 찌꺼기 제거
        clean_q = q.replace("**", "").replace("###", "")
        html_body += "<div style='margin-bottom:25px; display: flex; align-items: flex-start;'>" \
                     "<b style='font-size:16px; margin-right: 6px; user-select: none;'>" + str(idx+1) + ".</b> " \
                     "<div style='width: 100%; word-break: break-all;'>" + clean_q + "</div>" \
                     "</div>"
        
    iframe_src = "<!DOCTYPE html><html><head><meta charset='UTF-8'>" \
                 "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'></script>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js'></script>" \
                 "<style>body { background-color:#fff; color:#000; margin:0; padding:20px; font-family:'serif'; line-height:1.6; font-size: 14.5px; }</style>" \
                 "</head><body>" + html_body + \
                 "<script>document.addEventListener('DOMContentLoaded', function(){renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});});</script>" \
                 "</body></html>"
    
    # 💡 세로가 150px로 잘리는 현상을 막기 위해 높이를 550으로 고정하고 스크롤 허용
    components.html(iframe_src, width=320, height=550, scrolling=True)
    
    # 3. 해설 출력 (컴팩트한 Step-by-Step 렌더링)
    st.divider()
    st.subheader("💡 정답 및 해설")
    if not st.session_state.es:
        st.warning("AI가 해설 포맷을 생성하지 못했습니다. 아래 Raw 데이터를 확인하세요.")
    else:
        for idx, e in enumerate(st.session_state.es):
            with st.expander(f"▶ {idx+1}번 문항 해설 보기", expanded=True):
                st.markdown(e)

    # 4. 파일 편집용 Raw 데이터
    st.write("")
    with st.expander("📥 선생님 편집용 수식 텍스트 (HWP/Word 복사용)"):
        raw_text = ""
        for idx, q in enumerate(st.session_state.qs):
            raw_text += f"[{idx+1}번]\n{q}\n\n"
        st.text_area("LaTeX 데이터", value=raw_text.strip(), height=150)
