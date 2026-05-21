# views/single_math.py
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import google.generativeai as genai
import re

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

/* 💡 프리뷰 컴포넌트 여백 초기화 및 중앙 정렬 */
iframe { display: block; margin: 0 auto !important; border: none !important; }
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

if 'qs' not in st.session_state: st.session_state.qs = []
if 'es' not in st.session_state: st.session_state.es = []
if 'res' not in st.session_state: st.session_state.res = None

# 1. 문제 생성 파이프라인
if st.button("AI 변형 실행 (딸깍)", type="primary"):
    if not api_key:
        st.error("사이드바에 API Key를 입력하세요.")
    else:
        with st.spinner('출제 중...'):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # 💡 해설 수식 깨짐 방지를 위한 초강력 프롬프트
                p = "당신은 수능 수학 출제위원입니다. 다음 원본 문제를 변형하여 '5지선다형 객관식' 문항을 출제하십시오.\n" \
                    "문항 수: " + str(num_variants) + "\n" \
                    "유형: " + variant_type + "\n\n" \
                    "⚠️ [치명적 중요 지침 - 위반 시 감점] ⚠️\n" \
                    "1. 모든 수식은 절대로 백틱(`) 기호를 사용하여 코드 형태로 묶지 마십시오!!\n" \
                    "2. 수식은 무조건 $ 기호를 사용하여 감싸십시오. (예: $2\\sin\\theta + 1 = 0$)\n" \
                    "3. [QUESTION_START] 토큰 안에 문제 발문, 조건, ①~⑤ 선지를 모두 작성하십시오.\n" \
                    "4. [EXPLANATION_START] 토큰 안에 정답과 해설을 작성하십시오.\n\n" \
                    "[해설 출력 예시]\n" \
                    "[EXPLANATION_START]\n" \
                    "**[정답]** ⑤\n\n" \
                    "**[출제 의도]** 삼각함수의 덧셈정리 활용\n\n" \
                    "**[단계별 풀이]**\n" \
                    "- **Step 1:** 방정식 $\\sin x = 1$ 을 전개한다.\n" \
                    "- **Step 2:** 주어진 식에 대입하여 $\\cos x$ 를 구한다.\n" \
                    "[EXPLANATION_END]\n\n" \
                    "원본 데이터: " + source_text

                contents = [source_image, p] if source_image else [p]
                response = model.generate_content(contents)
                full_text = response.text
                
                qs = re.findall(r'\[QUESTION_START\](.*?)\[QUESTION_END\]', full_text, re.DOTALL)
                es = re.findall(r'\[EXPLANATION_START\](.*?)\[EXPLANATION_END\]', full_text, re.DOTALL)
                
                st.session_state.qs = [q.strip() for q in qs]
                st.session_state.es = [e.strip() for e in es]
                st.session_state.res = full_text
                st.success("출제 완료!")
            except Exception as e:
                st.error("오류: " + str(e))

# =======================================================================================
# 💡 [핵심 방어선] AI가 백틱(`)을 썼다면 강제로 $ 수식 기호로 치환하는 무결성 클리너 함수
# =======================================================================================
def clean_latex_backticks(text):
    if not text: return text
    # 1. ```math 형식의 블록 치환
    text = re.sub(r'```[a-zA-Z]*\n(.*?)\n```', r'$$\1$$', text, flags=re.DOTALL)
    # 2. 잔여 백틱(`)을 $로 치환 (인라인 코드 해결)
    text = re.sub(r'`([^`]+)`', r'$\1$', text)
    return text

# 2. 결과 렌더링
if st.session_state.res:
    st.divider()
    st.subheader("📄 수능 시험지 실물 프리뷰")
    
    html_body = ""
    for idx, q in enumerate(st.session_state.qs):
        # 마크다운 찌꺼기 및 백틱 완전 정화
        clean_q = clean_latex_backticks(q.replace("**", "").replace("###", ""))
        html_body += "<div style='margin-bottom: 20px; display: flex; align-items: flex-start;'>" \
                     "<b style='font-size: 16px; margin-right: 8px; user-select: none;'>" + str(idx+1) + ".</b> " \
                     "<div style='width: 100%; word-break: break-all;'>" + clean_q + "</div>" \
                     "</div>"
        
    # 💡 [핵심 교정] 위/아래 여백을 정확히 일치시키고, ResizeObserver로 세로 높이 자동 맞춤
    iframe_src = "<!DOCTYPE html><html><head><meta charset='UTF-8'>" \
                 "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'></script>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js'></script>" \
                 "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&display=swap' rel='stylesheet'>" \
                 "<style>" \
                 "html, body { background-color: #eef2f5 !important; margin: 0; padding: 20px 0; display: flex; justify-content: center; overflow: hidden; }" \
                 ".paper-box { background-color: #ffffff; color: #000000; padding: 50px 45px; width: 480px; box-sizing: border-box; font-family: 'Noto Serif KR', 'Batang', serif; font-size: 14.5px; line-height: 1.75; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }" \
                 "</style></head><body>" \
                 "<div class='paper-box'>" + html_body + "</div>" \
                 "<script>" \
                 "document.addEventListener('DOMContentLoaded', function(){" \
                 "  renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}], throwOnError:false});" \
                 "  const observer = new ResizeObserver(entries => {" \
                 "    for (let entry of entries) {" \
                 "      const height = document.documentElement.scrollHeight;" \
                 "      window.parent.postMessage({type: 'streamlit:setFrameHeight', height: height}, '*');" \
                 "    }" \
                 "  });" \
                 "  observer.observe(document.body);" \
                 "});" \
                 "</script></body></html>"
    
    components.html(iframe_src, width=540, scrolling=False)
    
    # 3. 정답 및 해설 (수식 깨짐 제로 방어선)
    st.divider()
    st.subheader("💡 정답 및 해설")
    if not st.session_state.es:
        st.warning("AI가 해설 포맷을 생성하지 못했습니다. 아래 Raw 데이터를 확인하세요.")
    else:
        for idx, e in enumerate(st.session_state.es):
            with st.expander(f"▶ {idx+1}번 문항 해설 보기", expanded=True):
                # AI가 뱉어낸 모든 백틱 코드를 $로 정화하여 렌더링
                safe_e = clean_latex_backticks(e)
                st.markdown(safe_e)

    # 4. 파일 편집용 자산
    st.write("")
    with st.expander("📥 선생님 편집용 수식 텍스트 (HWP/Word 복사용)"):
        raw_text = ""
        for idx, q in enumerate(st.session_state.qs):
            raw_text += f"[{idx+1}번]\n{clean_latex_backticks(q)}\n\n"
        st.text_area("LaTeX 데이터", value=raw_text.strip(), height=150)
