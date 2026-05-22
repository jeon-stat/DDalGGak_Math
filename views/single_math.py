# views/single_math.py
# 역할: 단일 문항 변형 UI 및 결과 렌더링

import streamlit as st
from PIL import Image

from ai_engine import DDalGGakEngine
from components import render_sidebar
from config import PROVIDER_GEMINI, PROVIDER_OPENAI
from renderers.single_math_result import render_generated_result


def initialize_session_state() -> None:
    for key in ("qs", "es", "res"):
        if key not in st.session_state:
            st.session_state[key] = [] if key != "res" else None


render_sidebar("AI 단일 문항 변형")
initialize_session_state()

with st.sidebar:
    st.markdown("### 출제 설정")
    ai_provider = st.selectbox("AI 제공자", [PROVIDER_GEMINI, PROVIDER_OPENAI])
    st.caption("선택한 제공자의 API Key를 입력해야 문항을 생성할 수 있습니다.")
    api_label = "OpenAI API Key" if ai_provider == PROVIDER_OPENAI else "Gemini API Key"
    api_key = st.text_input(api_label, type="password")

    num_variants = st.slider("문항 수", 1, 5, 1)
    variant_type = st.radio(
        "변형 유형",
        ["유형 1: 숫자 변형", "유형 2: 발문 비틀기", "유형 3: 킬러 위장"],
    )

    st.markdown("---")
    st.caption("API Key는 앱에 저장하지 않고 현재 실행 세션에서만 사용합니다.")

st.markdown(
    """
    <div class="dd-page-header">
        <div class="dd-eyebrow">Question transformation console</div>
        <h1>AI 단일 문항 변형</h1>
        <p>
            원본 문항을 입력하고 변형 유형을 선택하면, 수업과 과제에 바로 쓸 수 있는
            변형 문항과 짧은 해설을 생성합니다.
        </p>
    </div>
    <div class="dd-workflow">
        <div class="dd-workflow-step"><strong>1. 원본 입력</strong><span>이미지 또는 텍스트로 문항을 전달합니다.</span></div>
        <div class="dd-workflow-step"><strong>2. 변형 설계</strong><span>숫자 변형, 발문 비틀기, 킬러 위장을 선택합니다.</span></div>
        <div class="dd-workflow-step"><strong>3. 결과 확인</strong><span>시험지 미리보기, 해설, 복사용 텍스트를 확인합니다.</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

input_col, info_col = st.columns([1.35, 0.65])

with input_col:
    st.markdown(
        """
        <div class="dd-section-title">
            <div>
                <h3>원본 문항</h3>
                <p>문항 이미지가 있다면 업로드하고, 텍스트가 있다면 직접 입력하세요.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_method = st.radio(
        "입력 방식",
        ["이미지 업로드", "직접 입력"],
        horizontal=True,
    )

    source_text, source_image = "", None

    if input_method == "직접 입력":
        source_text = st.text_area(
            "원본 문제 입력",
            height=220,
            placeholder="원본 문항의 발문, 조건, 선지를 입력하세요.",
        )
    else:
        uploaded_file = st.file_uploader(
            "이미지 업로드",
            type=["png", "jpg", "jpeg"],
        )
        if uploaded_file is not None:
            source_image = Image.open(uploaded_file)
            st.image(source_image, caption="원본 문항 프리뷰", width=360)

with info_col:
    st.markdown(
        f"""
        <div class="dd-section-title">
            <div>
                <h3>현재 설정</h3>
                <p>생성 전에 옵션을 확인하세요.</p>
            </div>
        </div>
        <div class="dd-panel">
            <p style="margin-top:0;"><b>AI 제공자</b><br>{ai_provider}</p>
            <p><b>문항 수</b><br>{num_variants}개</p>
            <p style="margin-bottom:0;"><b>변형 유형</b><br>{variant_type}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    run_button = st.button("AI 변형 실행", type="primary", use_container_width=True)

    st.markdown(
        """
        <div class="dd-section-title" style="margin-top:1.8rem;">
            <div>
                <h3>저장 설정</h3>
                <p>클라우드 보관함 연동을 위한 자리입니다.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    save_name = st.text_input(
        "저장 이름",
        placeholder="ex) 등차수열 절댓값 변형 01",
        disabled=True,
    )
    save_folder = st.selectbox(
        "저장 폴더",
        ["클라우드 저장 준비중"],
        disabled=True,
    )
    new_folder = st.text_input(
        "새 폴더",
        placeholder="ex) 수열 / 미적분 / 3월 모의고사",
        disabled=True,
    )
    st.button(
        "문제 보관함에 저장",
        disabled=True,
        use_container_width=True,
    )
    st.caption("로그인과 클라우드 저장소가 연결되면 원본과 생성 결과를 함께 저장할 수 있습니다.")

if run_button:
    if not api_key:
        st.error(f"사이드바에 {api_label}를 입력하세요.")
    elif input_method == "직접 입력" and not source_text.strip():
        st.error("원본 문제 텍스트를 입력하세요.")
    elif input_method == "이미지 업로드" and source_image is None:
        st.error("원본 문제 이미지를 업로드하세요.")
    else:
        with st.spinner("문항을 설계하는 중..."):
            try:
                engine = DDalGGakEngine(api_key, ai_provider)
                raw = engine.generate_variants(
                    source_text,
                    source_image,
                    variant_type,
                    num_variants,
                )
                qs, es = engine.parse_result(raw)

                st.session_state.qs = qs
                st.session_state.es = es
                st.session_state.res = raw
                st.success("문항 생성이 완료되었습니다.")
            except Exception as e:
                st.error(f"오류: {e}")

if st.session_state.res:
    st.markdown(
        """
        <div class="dd-section-title">
            <div>
                <h3>생성 결과</h3>
                <p>시험지 미리보기와 해설을 확인한 뒤 필요한 형식으로 복사하세요.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_generated_result(st.session_state.qs, st.session_state.es)
else:
    st.markdown(
        """
        <div class="dd-section">
            <div class="dd-panel-quiet">
                <h3 style="margin-top:0;">아직 생성된 문항이 없습니다</h3>
                <p style="color:var(--dd-muted); margin-bottom:0;">
                    원본 문항을 입력하고 사이드바에서 출제 설정을 확인한 뒤 AI 변형 실행을 눌러보세요.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
