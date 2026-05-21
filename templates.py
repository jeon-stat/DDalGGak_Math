# templates.py

def build_pdf_print_html(content_html: str) -> str:
    """
    [딸깍매스 프리미엄 인쇄 전용 엔진]
    생성된 문항들을 다운로드하여 오프라인에서 수능 시험지 레이아웃으로 
    깨끗하게 출력되도록 도와주는 HTML 스킨 프레임입니다.
    """
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DDalGGak Math Premium Print Preview</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Serif KR', 'Batang', serif;
            font-size: 14px;
            line-height: 1.8;
            color: #000000;
            margin: 30px;
            background-color: #ffffff;
        }}
        blockquote {{
            border: 1.5px solid #000000 !important;
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
        document.addEventListener("DOMContentLoaded", function() {
            renderMathInElement(document.body, {{
                delimiters: [
                    {{left: "$$", right: "$$", display: true}},
                    {{left: "$", right: "$", display: false}}
                ],
                throwOnError : false
            }});
        });
    </script>
</body>
</html>"""
