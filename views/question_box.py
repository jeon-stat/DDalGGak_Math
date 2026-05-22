# views/question_box.py
# 역할: 향후 클라우드 문제 보관함 UI 렌더링

import streamlit as st

from components import render_sidebar


render_sidebar("나만의 문제 보관함")

st.markdown(
    """
    <div class="dd-page-header">
        <div class="dd-eyebrow">Problem library · cloud-ready</div>
        <h1>나만의 문제 보관함</h1>
        <p>
            생성한 문항의 원본, 변형 결과, 정답 해설을 폴더별로 정리하는 공간입니다.
            현재는 UI와 저장 구조만 준비되어 있으며, 실제 저장은 로그인과 클라우드 DB 연동 후 활성화됩니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="dd-section-title">
        <div>
            <h3>클라우드 보관함 구조</h3>
            <p>나중에 로그인 기능이 붙으면 아래 흐름으로 저장됩니다.</p>
        </div>
    </div>
    <div class="dd-workflow">
        <div class="dd-workflow-step"><strong>1. 폴더 생성</strong><span>단원, 시험지, 수업별로 폴더를 구성합니다.</span></div>
        <div class="dd-workflow-step"><strong>2. 문제 저장</strong><span>원본 입력과 생성 결과를 하나의 기록으로 저장합니다.</span></div>
        <div class="dd-workflow-step"><strong>3. 다시 활용</strong><span>저장된 문항을 확인하고 수업 자료로 재사용합니다.</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

folder_col, list_col, detail_col = st.columns([0.8, 1.05, 1.35])

with folder_col:
    st.markdown(
        """
        <div class="dd-section-title">
            <div>
                <h3>폴더</h3>
                <p>클라우드 연결 후 생성 가능</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("새 폴더 이름", placeholder="ex) 수열", disabled=True)
    st.button("폴더 만들기", disabled=True, use_container_width=True)
    st.markdown(
        """
        <div class="dd-panel" style="margin-top:1rem;">
            <p style="margin-top:0;"><b>전체 문제</b><br><span style="color:var(--dd-muted);">0개</span></p>
            <p><b>수열</b><br><span style="color:var(--dd-muted);">예시 폴더</span></p>
            <p style="margin-bottom:0;"><b>미적분</b><br><span style="color:var(--dd-muted);">예시 폴더</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with list_col:
    st.markdown(
        """
        <div class="dd-section-title">
            <div>
                <h3>저장된 문제</h3>
                <p>폴더를 선택하면 문제 목록이 표시됩니다.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="dd-panel-quiet">
            <h3 style="margin-top:0;">아직 저장된 문제가 없습니다</h3>
            <p style="color:var(--dd-muted); line-height:1.65;">
                생성 페이지에서 저장 이름과 폴더를 선택하면, 나중에는 이곳에 문제 카드가 쌓입니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with detail_col:
    st.markdown(
        """
        <div class="dd-section-title">
            <div>
                <h3>문제 상세</h3>
                <p>원본과 생성 결과를 함께 확인합니다.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="dd-panel">
            <div class="dd-feature-kicker">PREVIEW</div>
            <h3 style="margin-top:0;">클라우드 저장 준비중</h3>
            <p style="color:var(--dd-muted); line-height:1.65;">
                로그인, 사용자별 폴더, 문제 DB, 이미지 저장소가 연결되면
                원본 문항과 AI 생성 문항, 해설, 생성 옵션이 이 영역에 표시됩니다.
            </p>
            <hr style="border:none; border-top:1px solid var(--dd-border); margin:1rem 0;">
            <p style="margin-bottom:0; color:var(--dd-muted);">
                예정 데이터: 원본 입력 · 생성 문항 · 정답/해설 · AI 제공자 · 변형 유형 · 생성 일시
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="dd-section">
        <div class="dd-panel-quiet">
            <h3 style="margin-top:0;">저장은 언제 활성화되나요?</h3>
            <p style="color:var(--dd-muted); line-height:1.65; margin-bottom:0;">
                이 화면은 Supabase 같은 클라우드 인증/DB/스토리지를 붙이기 위한 제품 구조입니다.
                지금은 로컬 용량을 쓰지 않도록 실제 저장을 비활성화해 두었습니다.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
