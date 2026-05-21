# views/single_math.py
# 역할: 단일 문항 변형 UI 및 결과 렌더링
# AI 호출 → ai_engine.py / 프롬프트 → prompts.py / 사이드바 → components.py

import re

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from ai_engine import DDalGGakEngine
from components import render_sidebar

st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { background-color:var(--background-color) !important; border:1.5px solid rgba(128,128,128,0.3) !important; color:var(--text-color) !important; border-radius:8px !important; }
[data-testid="stSidebar"] { font-size:0.85rem !important; }
iframe { display:block; margin:0 auto !important; border:none !important; }
</style>
""", unsafe_allow_html=True)

# ── 사이드바 ──────────────────────────────────────────────
render_sidebar("🏠 Home > 📐 변형")

with st.sidebar:
    st.divider()
    st.header("⚙️ 출제 옵션")
    api_key      = st.text_input("Gemini API Key", type="password")
    num_variants = st.slider("문항 수", 1, 5, 1)
    variant_type = st.radio(
        "변형 유형",
        ["유형 1: 숫자 변형", "유형 2: 발문 비틀기", "유형 3: 킬러 위장"],
    )

# ── 메인 ─────────────────────────────────────────────────
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

# 세션 상태 초기화
for key in ("qs", "es", "res"):
    if key not in st.session_state:
        st.session_state[key] = [] if key != "res" else None

# ── 1. 문항 생성 ──────────────────────────────────────────
if st.button("AI 변형 실행 (딸깍)", type="primary"):
    if not api_key:
        st.error("사이드바에 API Key를 입력하세요.")
    else:
        with st.spinner("출제 중..."):
            try:
                engine = DDalGGakEngine(api_key)
                raw    = engine.generate_variants(source_text, source_image, variant_type, num_variants)
                qs, es = engine.parse_result(raw)

                st.session_state.qs  = qs
                st.session_state.es  = es
                st.session_state.res = raw
                st.success("출제 완료!")
            except Exception as e:
                st.error(f"오류: {e}")

# ── 2. 시험지 프리뷰 렌더링 ───────────────────────────────
if st.session_state.res:
    st.divider()
    st.subheader("📄 수능 시험지 실물 프리뷰")

    html_body = ""
    for idx, q in enumerate(st.session_state.qs):
        clean_q = q.replace("`", "$").replace("**", "").replace("###", "").replace("\n", "<br>")
        html_body += (
            f"<div style='margin-bottom:30px;display:flex;align-items:flex-start;'>"
            f"<b style='font-size:16px;margin-right:8px;user-select:none;'>{idx+1}.</b>"
            f"<div style='width:100%;word-break:break-all;white-space:pre-wrap;'>{clean_q}</div>"
            f"</div>"
        )

    iframe_src = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
        "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'>"
        "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'></script>"
        "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js'></script>"
        "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&display=swap' rel='stylesheet'>"
        "<style>"
        "body{margin:0;padding:10px;background-color:transparent;"
        "font-family:'Noto Serif KR','Batang',serif;font-size:14.5px;line-height:1.7;}"
        ".paper-box{background-color:#ffffff;color:#000000;padding:35px 40px;"
        "max-width:520px;margin:0 auto;border:1px solid #ccc;"
        "box-shadow:0px 4px 12px rgba(0,0,0,0.1);border-radius:4px;overflow:hidden;}"
        "</style></head><body>"
        f"<div class='paper-box' id='paper'>{html_body}</div>"
        "<script>"
        "document.addEventListener('DOMContentLoaded',function(){"
        "renderMathInElement(document.body,{delimiters:["
        "{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],"
        "throwOnError:false});"
        "function sendHeight(){"
        "var paper=document.getElementById('paper');"
        "var h=paper.getBoundingClientRect().height;"
        "window.parent.postMessage({type:'streamlit:setFrameHeight',height:h+40},'*');"
        "}"
        "renderMathInElement(document.body,{"
        "delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],"
        "throwOnError:false,"
        "afterTypeset:function(){sendHeight();}"  # ← 수식 렌더링 완료 직후 높이 전송
        "});"
        "sendHeight();"  # 혹시 수식 없을 때를 위한 즉시 실행
        "var last=0;"
        "setInterval(function(){"  # 0.1초마다 높이 변화 감지
        "var h=document.getElementById('paper').getBoundingClientRect().height+40;"
        "if(Math.abs(h-last)>2){last=h;"
        "window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');}"
        "},100);"
        "</script></body></html>"
    )
    components.html(iframe_src, height=2000, scrolling=False))

    # ── 3. 해설 출력 ──────────────────────────────────────
    st.divider()
    st.subheader("💡 정답 및 해설")

    if not st.session_state.es:
        st.warning("AI가 해설 포맷을 생성하지 못했습니다. 아래 Raw 데이터를 확인하세요.")
    else:
        for idx, e in enumerate(st.session_state.es):
            with st.expander(f"▶ {idx+1}번 문항 해설 보기", expanded=True):
                safe_e = e.replace("`", "$")
                safe_e = re.sub(r"\.\s+", ".\n\n", safe_e)
                safe_e = re.sub(r"\n{3,}", "\n\n", safe_e)
                st.markdown(safe_e)

    # ── 4. 편집용 Raw 데이터 ──────────────────────────────
    st.write("")
    with st.expander("📥 선생님 편집용 수식 텍스트 (HWP/Word 복사용)"):
        raw_text = "\n\n".join(
            f"[{idx+1}번]\n{q.replace('`', '$')}"
            for idx, q in enumerate(st.session_state.qs)
        )
        st.text_area("LaTeX 데이터", value=raw_text.strip(), height=150)
