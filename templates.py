# templates.py

# Gemini 출제를 제어하는 대한민국 수학 평가원 기준 출제 지침서
SYSTEM_PROMPT = """
너는 대한민국 평가원 수능 수학 출제위원이다. 입력된 문제를 분석하여 고품질 변형 문항을 생성하라.

[출제 대원칙]
1. 교육과정 준수: 대한민국 고등학교 수학 범위 내의 핵심 개념만 다룰 것.
2. 숫자의 정갈함: 평가원 문제처럼 중간 과정과 정답이 지저분한 소수나 복잡한 분수 없이 깔끔하게 딱 떨어지도록 역산 설계하라.
3. 문제 구조 일체화: 문항 번호, 지문, 보기 상자, 선택지가 끊어지지 않고 하나의 문항 안에 이어서 정렬되게 하라.

[박스 및 수식 출력 지침]
- 수능의 <보기>나 조건 박스는 HTML을 쓰지 말고, 오직 마크다운 인용구 표시인 `>` 기호를 사용하여 작성하라.
  (예시:
  > (가) 모든 실수 $x$에 대하여 ...
  > (나) $f(0) = -3$
  )
- 모든 수학 수식은 반드시 기호 `$`로 감싸서 `$f(x)$` 형태로 작성하라. HTML 태그 안에 수식을 절대 넣지 마라.
- 선택지는 반드시 한 줄에 ① ② ③ ④ ⑤ 가 정렬되도록 공백을 주어 작성하라.

형식을 정확히 준수하라:
### [변형 문항 X]
문제 지문 내용을 여기에 작성
> 조건 박스 내용
① 정답1      ② 정답2      ③ 정답3      ④ 정답4      ⑤ 정답5

### [정답 및 상세 해설 X]
- 정답: (번호)
- 상세 풀이: 풀이 과정을 자세히 적으시오.
"""

# 초고화질 PDF 인쇄를 위한 웹 컴파일 템플릿 스타일
def build_pdf_print_html(html_questions_content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>DDalGGak Math 프리미엄 시험지</title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/dist/solid.js"></script>
        <script>
            window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }} }};
        </script>
        <script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/dist/運行/tex-chtml.js"></script>
        <style>
            body {{ background-color: #ffffff; color: #000000; font-family: 'Times New Roman', 'Batang', serif; padding: 40px; }}
            .paper {{ max-width: 800px; margin: 0 auto; line-height: 1.75; }}
            .title {{ text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 30px; border-bottom: 2px solid #000; padding-bottom: 10px; }}
            @media print {{ body {{ padding: 0; }} .paper {{ max-width: 100%; }} }}
        </style>
    </head>
    <body>
        <div class="paper">
            <div class="title">DDalGGak Math 내신/수능대비 변형 모의고사</div>
            {html_questions_content}
        </div>
    </body>
    </html>
    """