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

/* 💡 프리뷰 중앙 정렬 강제 */
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
        # 💡 지민님이 지정하신 프리뷰 크기 (280px)
        st.image(source_image, caption="원본 기출문제 프리뷰", width=280)

# 세션 상태 강제 고정 (해설 유실 방지)
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
                
                p = "수능 수학 출제위원으로서 다음 문제를 변형하십시오.\n" \
                    "문항 수: " + str(num_variants) + "\n" \
                    "유형: " + variant_type + "\n\n" \
                    "조건: 수식은 반드시 $...$로 감싸고, 다음 태그를 정확히 지키십시오.\n" \
                    "[QUESTION_START] 문제 내용 [QUESTION_END]\n" \
                    "[EXPLANATION_START] 정답과 해설 [EXPLANATION_END]\n\n" \
                    "원본 데이터: " + source_text

                contents = [source_image, p] if source_image else [p]
                response = model.generate_content(contents)
                full_text = response.text
                
                # 정규표현식으로 정밀 파싱
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
    
    # 💡 [핵심 교정] 업로드 이미지 크기와 맞춘 컴팩트 렌더링 (가로 280px 규격)
    html_body = ""
    for idx, q in enumerate(st.session_state.qs):
        html_body += "<div style='margin-bottom:25px;'>" \
                     "<b style='font-size:16px;'>" + str(idx+1) + ".</b> " \
                     "<span style='font-size:14px;'>" + q + "</span>" \
                     "</div>"
        
    iframe_src = "<!DOCTYPE html><html><head><meta charset='UTF-8'>" \
                 "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'></script>" \
                 "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js'></script>" \
                 "<style>body { background-color:#fff; color:#000; margin:0; padding:20px; font-family:'serif'; line-height:1.6; }</style>" \
                 "</head><body>" + html_body + \
                 "<script>document.addEventListener('DOMContentLoaded', function(){renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});});</script>" \
                 "</body></html>"
    
    # 💡 width를 300으로 설정하여 280px 이미지와 시각적 크기를 맞춤
    components.html(iframe_src, width=320, height=400, scrolling=True)
    
    # 3. 해설 출력 (버그 해결: 세션 상태에서 직접 불러옴)
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
