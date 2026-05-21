# templates.py

def build_pdf_print_html(content_html: str) -> str:
    """
    [딸깍매스 프리미엄 인쇄 전용 엔진]
    AI가 생성한 수학 문항들을 실제 종이에 인쇄하거나 PDF로 저장할 때 
    B4/A4 규격의 수능 시험지 레이아웃으로 컴파일하는 초고화질 HTML 스킨입니다.
    """
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>DDalGGak Math Premium Print Preview</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap" rel="stylesheet">
        
        <style>
            @page {{
                size: A4;
                margin: 20mm 15mm;
            }}
            body {{
                font-family: 'Noto Serif KR', 'Batang', serif;
                font-size: 14px;
                line-height: 1.8;
                color: #000000;
                margin: 0;
                padding: 0;
                background-color: #ffffff;
            }}
            .print-page {{
                width: 100%;
                box-sizing: border-box;
            }}
            /* 수능 특유의 합답형 박스 보기 레이아웃 방어 */
            blockquote {{
                border: 1.5px solid #000000 !important;
                padding: 15px !important;
                margin: 12px 0 !important;
                background: transparent !important;
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
                        {{left: "$", right: "$", display: false}},
                        {{left: "\\\\(", right: "\\\\)", display: false}},
                        {{left: "\\\\[", right: "\\\\]", display: true}}
                    ],
                    throwOnError : false
                }});
            });
        </script>
    </body>
    </html>
    """
    return html_template
