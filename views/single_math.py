import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import re
# 💡 분리된 AI 엔진을 직접 임포트하여 사용
from ai_engine import DDalGGakEngine

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

/* iframe 컴포넌트 여백 초기화 및 중앙 정렬 */
iframe { display: block; margin: 0 auto !important; border: 1px solid rgba(128,128,128,0.2) !important; border-radius: 4px; }
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

# 1. 문제 생성 파이프라인 (ai_engine 호출)
if st.button("AI 변형 실행 (딸깍)", type="primary"):
    if not api_key:
        st.error("사이드바에 API Key를 입력하세요.")
    else:
        with st.spinner('출제 중... (선지 및 해설 최적화)'):
            try:
                engine = DDalGGakEngine(api_key=api_key)
                raw_result = engine.generate_variants(source_text, source_image, variant_type, num_variants)
                qs, es = engine.parse_result(raw_result)
                
                st.session_state.qs = qs
                st.session_state.es = es
                st.session_state.res = raw_result
                st.success("출제 완료!")
            except Exception as e:
                st.error("오류: " + str(e))

# 2. 결과 렌더링
if st.session_state.res:
    st.divider()
    st.subheader("📄 수능 시험지 실물 프리뷰")
    
    # 임시 엔진 객체를 만들어 클리너 함수 사용
    cleaner_engine = DDalGGakEngine(api_key="dummy") 
    
    html_body = ""
    for idx, q in enumerate(st.session_state.qs):
        clean_q = cleaner_engine.clean_latex(q).replace("**", "").replace("###", "")
        # 선지가 무조건 아래로 내려가도록 줄바꿈을 <br>로 치환
        clean_q = clean_q.replace("\n", "<br>")
        
        html_body += "<div style='display: flex; align-items: flex-start; margin-bottom: 10px;'>" \
                     "<div style='font-weight: bold; margin-right: 8px; white-space: nowrap;'>" + str(idx+1) + ".</div>" \
                     "<div style='width: 100%; word-break: keep-all;'>" + clean_q + "</div>" \
                     "</div>"
        
    iframe_src = "<!DOCTYPE html><html><head><meta charset='UTF-8'>" \
                 "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'></script>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js'></script>" \
                 "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&display=swap' rel='stylesheet'>" \
                 "<style>" \
                 "html, body { background-color: #ffffff; color: #000000; margin: 0; padding: 15px 20px; font-family: 'Noto Serif KR', 'Batang', serif; font-size: 15px; line-height: 1.8; overflow: hidden; }" \
                 "</style></head><body>" \
                 "<div id='paper'>" + html_body + "</div>" \
                 "<script>" \
                 "document.addEventListener('DOMContentLoaded', function(){" \
                 "  renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}], throwOnError:false});" \
                 "  const observer = new ResizeObserver(entries => {" \
                 "    for (let entry of entries) {" \
                 "      const height = document.body.scrollHeight;" \
                 "      window.parent.postMessage({type: 'streamlit:setFrameHeight', height: height}, '*');" \
                 "    }" \
                 "  });" \
                 "  observer.observe(document.body);" \
                 "});" \
                 "</script></body></html>"
    
    components.html(iframe_src, width=540, scrolling=False)
    
    # 3. 정답 및 해설 (마침표 뒤 무조건 두 줄 바꿈 강제)
    st.divider()
    st.subheader("💡 정답 및 해설")
    if not st.session_state.es:
        st.warning("AI가 해설 포맷을 생성하지 못했습니다. 아래 Raw 데이터를 확인하세요.")
    else:
        for idx, e in enumerate(st.session_state.es):
            with st.expander(f"▶ {idx+1}번 문항 해설 보기", expanded=True):
                safe_e = cleaner_engine.clean_latex(e)
                # 💡 [버그 종결] 마크다운 특성상 마침표 뒤에 띄어쓰기나 엔터가 1번만 있으면 글이 이어집니다. 
                # 이를 파괴하기 위해 모든 마침표(.) 뒤를 무조건 두 번의 엔터(\n\n)로 강제 확장합니다.
                safe_e = re.sub(r'\.\s+', '.\n\n', safe_e)
                safe_e = safe_e.replace('\n', '\n\n')
                # 과도하게 늘어난 엔터(3개 이상)는 2개로 압축하여 예쁜 간격 유지
                safe_e = re.sub(r'\n{3,}', '\n\n', safe_e)
                
                st.markdown(safe_e)

    # 4. 파일 편집용 자산
    st.write("")
    with st.expander("📥 선생님 편집용 수식 텍스트 (HWP/Word 복사용)"):
        raw_text = ""
        for idx, q in enumerate(st.session_state.qs):
            raw_text += f"[{idx+1}번]\n{cleaner_engine.clean_latex(q)}\n\n"
        st.text_area("LaTeX 데이터", value=raw_text.strip(), height=150)
