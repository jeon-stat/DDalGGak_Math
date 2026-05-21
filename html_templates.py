# html_templates.py  (구: templates.py)
# HTML 렌더링 템플릿을 이 파일에서만 관리합니다.
# 인쇄 레이아웃 스타일을 수정할 때는 이 파일만 열면 됩니다.


def build_pdf_print_html(content_html: str) -> str:
    """
    생성된 문항들을 수능 시험지 레이아웃으로 출력하기 위한 HTML 프레임을 반환합니다.

    Args:
        content_html: 렌더링할 문항 HTML 문자열

    Returns:
        KaTeX가 포함된 완성된 인쇄용 HTML 문자열
    """
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>DDalGGak Math Print</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<style>
body {{
    font-family: serif;
    font-size: 14px;
    line-height: 1.8;
    color: #000;
    margin: 30px;
    background-color: #fff;
}}
blockquote {{
    border: 1.5px solid #000 !important;
    padding: 15px !important;
    margin: 12px 0 !important;
}}
</style>
</head>
<body>
<div class="print-page">
    {content_html}
</div>
<script>
document.addEventListener("DOMContentLoaded", function() {{
    renderMathInElement(document.body, {{
        delimiters: [
            {{left: "$$", right: "$$", display: true}},
            {{left: "$",  right: "$",  display: false}}
        ],
        throwOnError: false
    }});
}});
</script>
</body>
</html>"""
