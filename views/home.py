# views/home.py
# 역할: 제품 홈 화면 렌더링 및 피드백 폼 처리

import time

import requests
import streamlit as st

from components import render_sidebar


FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfMMoBOa7hBNNpPcsMxePiXmAGfgI8eL20NK54p9rZv4usnvw/formResponse"


render_sidebar("Home")

st.markdown(
    """
    <div class="dd-shell">
        <section class="dd-hero">
            <div class="dd-eyebrow">Open beta · AI math item studio</div>
            <h1>수학 문항 제작을<br>더 빠르고 정교하게.</h1>
            <p>
                DDalGGak Math는 원본 문항의 핵심 사고과정을 분석해 변형 문항,
                정답 해설, 시험지 미리보기, 복사용 수식 텍스트까지 한 흐름으로 만드는
                교육용 AI 문항 제작 플랫폼입니다.
            </p>
            <div class="dd-stat-row">
                <div class="dd-stat"><strong>1문항</strong><span>원본 문항 기반 변형 생성</span></div>
                <div class="dd-stat"><strong>3유형</strong><span>숫자 변형 · 발문 비틀기 · 킬러 위장</span></div>
                <div class="dd-stat"><strong>즉시</strong><span>시험지 프리뷰와 해설 출력</span></div>
            </div>
        </section>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="dd-section-title">
        <div>
            <h2>문항 제작 워크플로우</h2>
            <p>수업 준비에 필요한 결과물을 한 번에 정리합니다.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="dd-feature">
            <div class="dd-feature-kicker">INPUT</div>
            <h3>원본 문항 입력</h3>
            <p>이미지 업로드 또는 직접 입력으로 기출 문항의 조건과 수식을 전달합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="dd-feature">
            <div class="dd-feature-kicker">DESIGN</div>
            <h3>변형 유형 선택</h3>
            <p>동일 구조, 발문 비틀기, 사고과정 위장 중 수업 목적에 맞는 출제 방식을 고릅니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="dd-feature">
            <div class="dd-feature-kicker">OUTPUT</div>
            <h3>시험지와 해설 출력</h3>
            <p>5지선다 문항, 간결한 해설, HWP/Word 복사용 수식 텍스트를 확인합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="dd-section-title">
        <div>
            <h2>출제 품질을 위한 기준</h2>
            <p>단순 치환보다 수업에 쓸 수 있는 결과물에 집중합니다.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

q1, q2 = st.columns(2)

with q1:
    st.markdown(
        """
        <div class="dd-panel">
            <h3 style="margin-top:0;">문항의 구조를 먼저 읽습니다</h3>
            <p style="color:var(--dd-muted); line-height:1.65;">
                원본 문항의 단원, 핵심 개념, 풀이 아이디어를 기준으로 유지할 조건과 바꿀 조건을 분리합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with q2:
    st.markdown(
        """
        <div class="dd-panel">
            <h3 style="margin-top:0;">해설은 짧고 실전적으로 씁니다</h3>
            <p style="color:var(--dd-muted); line-height:1.65;">
                장황한 전개보다 핵심 관계식, 결정적 계산, 정답 도출만 남기는 문제집식 해설을 지향합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="dd-section-title">
        <div>
            <h2>오픈 베타 안내</h2>
            <p>현재는 사용자의 API Key로 AI 모델을 호출하는 테스트 버전입니다.</p>
        </div>
    </div>
    <div class="dd-panel-quiet">
        <p style="margin-top:0; color:var(--dd-muted); line-height:1.65;">
            Gemini 또는 GPT를 선택해 테스트할 수 있습니다. 각 제공자의 API Key가 필요하며,
            키는 앱에 저장하지 않고 입력한 세션에서만 사용합니다.
        </p>
        <p style="margin-bottom:0;">
            Gemini 키는 <a href="https://aistudio.google.com/" target="_blank">Google AI Studio</a>,
            OpenAI 키는 <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI Platform</a>에서 발급할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="dd-section-title">
        <div>
            <h2>제품 피드백</h2>
            <p>실제 수업 준비에 쓰기 위해 필요한 점을 알려주세요.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

feedback_col, guide_col = st.columns([1.2, 0.8])

with feedback_col:
    user_info_input = st.text_input("직업", placeholder="ex) 교사, 강사, 학생, 학부모")
    feedback_text = st.text_area(
        "의견 또는 개선 요청",
        height=120,
        placeholder="ex) 유형 2 변형이 원본과 너무 비슷해요",
    )
    msg_slot = st.empty()

    if st.button("의견 전송하기", type="secondary"):
        if not feedback_text:
            msg_slot.warning("내용을 입력하신 후 전송해 주세요.")
        elif not user_info_input:
            msg_slot.warning("피드백 관리를 위해 직업을 먼저 입력해 주세요.")
        else:
            with st.spinner("피드백을 기록하는 중..."):
                payload = {
                    "entry.1056156260": feedback_text,
                    "entry.1147584167": user_info_input,
                }
                try:
                    response = requests.post(FORM_URL, data=payload, timeout=10)
                    if response.status_code == 200:
                        msg_slot.success("감사합니다. 피드백이 기록되었습니다.")
                        time.sleep(2.5)
                        msg_slot.empty()
                    else:
                        msg_slot.error("전송 중 지연이 발생했습니다. 잠시 후 다시 시도해 주세요.")
                except Exception as e:
                    msg_slot.error(f"피드백 전송 오류: {e}")

with guide_col:
    st.markdown(
        """
        <div class="dd-panel">
            <h3 style="margin-top:0;">좋은 피드백 예시</h3>
            <p style="color:var(--dd-muted); line-height:1.65;">
                생성된 문항이 원본과 얼마나 다른지, 해설이 수업에 바로 쓰기 좋은지,
                선지가 자연스러운지 중심으로 알려주시면 개선에 가장 도움이 됩니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
