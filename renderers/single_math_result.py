import re

import streamlit as st
import streamlit.components.v1 as components


def render_generated_result(questions: list[str], explanations: list[str]) -> None:
    """Render generated questions, explanations, and copy-friendly text."""
    st.divider()
    render_exam_preview(questions)
    render_explanations(explanations)
    render_copy_text(questions)


def render_exam_preview(questions: list[str]) -> None:
    """Render the generated questions in a CSAT-style paper preview."""
    st.subheader("📄 수능 시험지 실물 프리뷰")
    html_body = build_question_html(questions)
    components.html(build_exam_iframe(html_body), height=400, scrolling=False)


def build_question_html(questions: list[str]) -> str:
    """Convert generated question text into HTML blocks."""
    blocks = []
    for idx, question in enumerate(questions):
        clean_question = (
            question.replace("`", "$")
            .replace("**", "")
            .replace("###", "")
            .replace("\n", "<br>")
        )
        blocks.append(
            "<div style='margin-bottom:30px;display:flex;align-items:flex-start;'>"
            f"<b style='font-size:16px;margin-right:8px;user-select:none;'>{idx + 1}.</b>"
            f"<div style='width:100%;word-break:break-all;white-space:pre-wrap;'>{clean_question}</div>"
            "</div>"
        )
    return "".join(blocks)


def build_exam_iframe(html_body: str) -> str:
    """Build the isolated HTML document used by Streamlit components."""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css'>
<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js'></script>
<script src='https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js'></script>
<link href='https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&display=swap' rel='stylesheet'>
<style>
* {{ box-sizing: border-box; }}
html, body {{
    margin: 0;
    padding: 0;
    background-color: transparent;
    font-family: 'Noto Serif KR', 'Batang', serif;
    font-size: 14.5px;
    line-height: 1.7;
}}
.paper-box {{
    background-color: #ffffff;
    color: #000000;
    padding: 35px 40px;
    max-width: 520px;
    margin: 0 auto;
    border: 1px solid #ccc;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    border-radius: 4px;
}}
</style>
</head>
<body>
<div class='paper-box' id='paper'>{html_body}</div>
<script>
function sendHeight() {{
    var h = document.getElementById('paper').getBoundingClientRect().height;
    window.parent.postMessage({{type: 'streamlit:setFrameHeight', height: Math.ceil(h) + 20}}, '*');
}}

document.addEventListener('DOMContentLoaded', function() {{
    renderMathInElement(document.body, {{
        delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$',  right: '$',  display: false}}
        ],
        throwOnError: false
    }});

    sendHeight();

    new ResizeObserver(function() {{
        sendHeight();
    }}).observe(document.getElementById('paper'));
}});
</script>
</body>
</html>"""


def render_explanations(explanations: list[str]) -> None:
    """Render answer explanations in expandable sections."""
    st.divider()
    st.subheader("💡 정답 및 해설")

    if not explanations:
        st.warning("AI가 해설 포맷을 생성하지 못했습니다. 아래 Raw 데이터를 확인하세요.")
        return

    for idx, explanation in enumerate(explanations):
        with st.expander(f"▶ {idx + 1}번 문항 해설 보기", expanded=True):
            safe_explanation = explanation.replace("`", "$")
            safe_explanation = re.sub(r"\.\s+", ".\n\n", safe_explanation)
            safe_explanation = re.sub(r"\n{3,}", "\n\n", safe_explanation)
            st.markdown(safe_explanation)


def render_copy_text(questions: list[str]) -> None:
    """Render copy-friendly LaTeX text for HWP or Word editing."""
    st.write("")
    with st.expander("📥 선생님 편집용 수식 텍스트 (HWP/Word 복사용)"):
        raw_text = "\n\n".join(
            f"[{idx + 1}번]\n{question.replace('`', '$')}"
            for idx, question in enumerate(questions)
        )
        st.text_area("LaTeX 데이터", value=raw_text.strip(), height=150)
