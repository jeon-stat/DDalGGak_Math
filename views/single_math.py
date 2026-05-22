# views/single_math.py
# 역할: 단일 문항 변형 UI 및 결과 렌더링
# AI 호출 → ai_engine.py / 프롬프트 → prompts.py / 사이드바 → components.py

import streamlit as st
from PIL import Image

from ai_engine import DDalGGakEngine
from components import render_sidebar
from renderers.single_math_result import render_generated_result

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

if st.session_state.res:
    render_generated_result(st.session_state.qs, st.session_state.es)
