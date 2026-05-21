import google.generativeai as genai
import json
import re

class DDalGGakEngine:
    def __init__(self, api_key: str):
        """
        딸깍 매스 프리미엄 AI 출제 엔진 초기화
        """
        genai.configure(api_key=api_key)
        # 수학적 추론 및 무결성 제어 능력이 탁월하고 속도가 빠른 flash 모델 고정
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_variants(self, source_text: str, source_image, variant_type: str, num_variants: int) -> str:
        """
        사이드바에서 선택된 변형 메커니즘 옵션을 프롬프트에 100% 주입하여 문항을 역산 생성합니다.
        """
        
        # 💡 [핵심 개혁] 옵션 반영(유형 1,2,3) + 5지선다 + 백틱 금지 + Step해설 모두 포함
        prompt = f"""
당신은 대한민국 한국교육과정평가원 수능 출제위원 기조의 최고 권위 수학 EdTech 출제 인공지능입니다.
입력된 수학 기출문제를 분석하고, 지정된 '변형 메커니즘' 요구사항을 절대적으로 준수하여 수학적 오류가 전혀 없는 '5지선다형 객관식' 무결성 변형 문항을 출제하십시오.

[출제 세부 옵션 정보]
- 생성할 변형 문항 수: {num_variants}개
- 선택된 변형 메커니즘 유형: {variant_type}

⚠️ [매우 중요] 변형 메커니즘별 절대 준수 지침 ⚠️
1. 사용자가 "유형 1: 숫자 및 단순 조건 변형 (동일 구조)"을 선택한 경우:
   - 원본 문항의 발문 구조, 기하학적/대수적 뼈대와 핵심 조건의 틀은 100% 동일하게 유지하십시오.
   - 오직 문항에 사용된 상수, 함수식의 계수, 미지수의 숫자 조건만 치환하십시오.
   - 변형된 숫자로 인해 중간 연산이나 최종 정답이 분수/무리수로 지저분하게 찢어지지 않고, 깔끔한 '정수 또는 유리수'로 딱 떨어지도록 치밀하게 역산 설계하십시오.

2. 사용자가 "유형 2: 표현 및 형태 변형 (발문 비틀기)"을 선택한 경우:
   - 원본 문항이 내포한 핵심 수학적 개념과 본질은 완벽하게 공유해야 합니다.
   - 하지만 원본의 발문 형태를 완전히 비틀어 표현하십시오. 최댓값을 구하라는 문제를 'g(t)가 불연속이 되는 점의 개수'로 바꾸거나, 연립방정식을 조건 제시형 보기(가, 나) 박스로 위장하십시오.

3. 사용자가 "유형 3: 사고과정 공유 변형 (완전 위장 / 킬러)"을 선택한 경우:
   - 원본 문제의 대수식이나 구체적인 숫자를 절대 복사하거나 그대로 사용하지 마십시오.
   - 원본 킬러 문항이 요구하는 최고 난도 상위 사고과정의 '논리적 상속'만 취하십시오.
   - 아예 초면인 완전히 새로운 함수 구조를 창조하여, 외관상으로는 원본과 완전히 다른 신작 문제처럼 위장하십시오.

⚠️ [치명적 렌더링 지침 - 위반 시 감점] ⚠️
1. 모든 수식은 절대로 백틱(`) 기호를 사용하여 코드 형태로 묶지 마십시오!!
2. 수식은 무조건 $ 기호를 사용하여 감싸십시오. (예: $2\\sin\\theta + 1 = 0$)
3. 문제 발문이 끝난 후, 반드시 '엔터(줄바꿈)'를 두 번 넣고 ①~⑤ 선지를 아래에 배치하십시오.

[입력 원본 기출문제 텍스트 데이터]
{source_text}

----------------------------------------------------------------------
[출력 데이터 형식 지정 가이드]
프론트엔드 파서와의 완벽한 호환을 위해, 아래 태그 구조를 정확히 지키십시오.

[QUESTION_START]
(여기에 변형된 문항 발문과 조건 제시)
$$ f(x) = ... $$

① $ 10 $ ② $ 20 $ ③ $ 30 $ ④ $ 40 $ ⑤ $ 50 $
[QUESTION_END]

[EXPLANATION_START]
**[정답]** ⑤

**[출제 의도]** (개념 및 추론 핵심 한 줄 요약)

**[단계별 풀이]**
- **Step 1:** (조건 분석 및 첫 수식 전개)
- **Step 2:** (핵심 뼈대 연산 및 케이스 분류)
- **Step 3:** (최종 답 도출)
(줄글로 길게 늘어놓지 말고, 수식과 지시어를 활용해 컴팩트하게 압축)
[EXPLANATION_END]

문항 수가 {num_variants}개이므로, 위 특수 토큰 세트를 총 {num_variants}번 반복하여 출력하십시오.
"""

        contents = []
        if source_image is not None:
            contents.append(source_image)
        contents.append(prompt)

        response = self.model.generate_content(contents)
        return response.text

    def parse_result(self, raw_result: str):
        """
        AI가 출력한 Raw 텍스트에서 특수 토큰 태그를 기준으로 
        문제부와 해설부를 정밀 분리하여 리스트로 반환합니다.
        """
        questions = []
        explanations = []

        q_pattern = re.compile(r'\[QUESTION_START\](.*?)\[QUESTION_END\]', re.DOTALL)
        e_pattern = re.compile(r'\[EXPLANATION_START\](.*?)\[EXPLANATION_END\]', re.DOTALL)

        raw_questions = q_pattern.findall(raw_result)
        raw_explanations = e_pattern.findall(raw_result)

        for q in raw_questions:
            questions.append(q.strip())
            
        for e in raw_explanations:
            explanations.append(e.strip())

        if not questions:
            questions.append(raw_result)
            explanations.append("해설 포맷 분리 실패 - Raw 데이터를 참조하십시오.")

        return questions, explanations
