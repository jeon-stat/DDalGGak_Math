# ai_engine.py
import google.generativeai as genai
import json
import re

class DDalGGakEngine:
    def __init__(self, api_key: str):
        """
        딸깍 매스 프리미엄 AI 출제 엔진 초기화
        """
        genai.configure(api_key=api_key)
        # 수학적 추론 및 무결성 제어 능력이 가장 탁월한 gemini-2.5-pro 모델 고정 (flash 쓰는 중)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_variants(self, source_text: str, source_image, variant_type: str, num_variants: int) -> str:
        """
        사이드바에서 선택된 변형 메커니즘 옵션을 프롬프트에 100% 주입하여 문항을 역산 생성합니다.
        """
        
        # 💡 [핵심 개혁] templates.py에 의존하지 않고 엔진 내부에서 유형별 수학적 출제 가이드라인을 강제 주입
        prompt = f"""
당신은 대한민국 한국교육과정평가원 수능 출제위원 기조의 최고 권위 수학 EdTech 출제 인공지능입니다.
입력된 수학 기출문제를 분석하고, 지정된 '변형 메커니즘' 요구사항을 절대적으로 준수하여 수학적 오류가 전혀 없는 무결성 변형 문항을 출제하십시오.

[출제 세부 옵션 정보]
- 생성할 변형 문항 수: {num_variants}개
- 선택된 변형 메커니즘 유형: {variant_type}

⚠️ [매우 중요] 변형 메커니즘별 절대 준수 지침 ⚠️
1. 사용자가 "유형 1: 숫자 및 단순 조건 변형 (동일 구조)"을 선택한 경우:
   - 원본 문항의 발문 구조, 기하학적/대수적 뼈대와 핵심 조건의 틀은 100% 동일하게 유지하십시오.
   - 오직 문항에 사용된 상수, 함수식의 계수, 미지수의 숫자 조건만 치환하십시오.
   - 변형된 숫자로 인해 중간 연산이나 최종 정답이 분수/무리수로 지저분하게 찢어지지 않고, 수능 기조에 맞게 깔끔한 '정수 또는 유리수'로 딱 떨어지도록 치밀하게 역산 설계하십시오.

2. 사용자가 "유형 2: 표현 및 형태 변형 (발문 비틀기)"을 선택한 경우:
   - 원본 문항이 내포한 핵심 수학적 개념(예: 도함수의 정의, 사잇값 정리 등)과 본질은 완벽하게 공유해야 합니다.
   - 하지만 원본의 발문 형태를 완전히 비틀어 표현하십시오. 최댓값을 구하라는 문제를 'g(t)가 불연속이 되는 점의 개수'로 바꾸거나, 연립방정식을 '두 곡선이 만나는 교점의 개수' 같은 조건 제시형 보기(가, 나) 박스로 위장하십시오.

3. 사용자가 "유형 3: 사고과정 공유 변형 (완전 위장 / 킬러)"을 선택한 경우:
   - 원본 문제의 대수식이나 구체적인 숫자를 절대 복사하거나 그대로 사용하지 마십시오. (복사 발견 시 오답 처리)
   - 원본 킬러 문항이 요구하는 최고 난도 상위 사고과정(예: 대칭성을 활용한 케이스 분류, 역함수와 합성함수의 미분계수 극점 추론 등)의 '논리적 상속'만 취하십시오.
   - 아예 초면인 완전히 새로운 함수 구조(지수, 로그, 삼각함수의 정교한 합성식)를 창조하여, 외관상으로는 원본과 완전히 다른 출제위원의 창작 문제처럼 위장하십시오.

[입력 원본 기출문제 텍스트 데이터]
{source_text}

----------------------------------------------------------------------
[출력 데이터 형식 지정 가이드]
프론트엔드 파서와의 완벽한 호환을 위해, 반드시 아래의 특수 토큰 태그 구조를 정확히 지켜서 일반 텍스트로 답변을 렌더링하십시오. 다른 설명이나 인사말은 절대 포함하지 마십시오.

[QUESTION_START]
(여기에 변형된 문항의 발문과 조건을 작성하십시오. 수식은 반드시 LaTeX 기호인 $...$ 또는 $$...$$로 감싸야 합니다.)
[QUESTION_END]
[EXPLANATION_START]
(여기에 해당 문항의 정답과 정교한 출제위원급 단계별 풀이 과정을 작성하십시오. 수식은 LaTeX 필수.)
[EXPLANATION_END]

문항 수가 {num_variants}개이므로, 위 특수 토큰 세트를 총 {num_variants}번 반복하여 출력하십시오.
"""

        # 이미지 입력과 텍스트 입력을 동시에 방어하는 멀티모달 아키텍처 가동
        contents = []
        if source_image is not None:
            contents.append(source_image)
        
        contents.append(prompt)

        # Gemini Pro 모델 호출 실행
        response = self.model.generate_content(contents)
        return response.text

    def parse_result(self, raw_result: str):
        """
        AI가 출력한 Raw 텍스트에서 특수 토큰 태그를 기준으로 
        문제부와 해설부를 정밀 분리하여 리스트로 반환합니다.
        """
        questions = []
        explanations = []

        # 정규표현식을 이용한 토큰 매칭 및 캡처
        q_pattern = re.compile(r'\[QUESTION_START\](.*?)\[QUESTION_END\]', re.DOTALL)
        e_pattern = re.compile(r'\[EXPLANATION_START\](.*?)\[EXPLANATION_END\]', re.DOTALL)

        raw_questions = q_pattern.findall(raw_result)
        raw_explanations = e_pattern.findall(raw_result)

        for q in raw_questions:
            questions.append(q.strip())
            
        for e in raw_explanations:
            explanations.append(e.strip())

        # 만약 AI가 토큰 포맷을 안 지키고 날것으로 줬을 때를 대비한 예외 방어선 코드
        if not questions:
            # 전체 데이터를 통째로 1번 문제로 패싱하여 화면 깨짐 방지
            questions.append(raw_result)
            explanations.append("해설 포맷 분리 실패 - Raw 데이터를 참조하십시오.")

        return questions, explanations
