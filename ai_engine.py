# ai_engine.py
# 딸깍 매스 프리미엄 AI 출제 엔진
# 역할: Gemini API 호출 및 응답 파싱만 담당합니다.
# 프롬프트 내용 → prompts.py / 상수 → config.py

import re

import google.generativeai as genai

from config import MODEL_NAME, Q_TAG_START, Q_TAG_END, E_TAG_START, E_TAG_END
from prompts import build_variant_prompt


class DDalGGakEngine:

    def __init__(self, api_key: str):
        """딸깍 매스 AI 출제 엔진 초기화"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate_variants(
        self,
        source_text: str,
        source_image,
        variant_type: str,
        num_variants: int,
    ) -> str:
        """
        변형 문항을 생성하고 Raw 텍스트를 반환합니다.

        Args:
            source_text:   원본 기출문제 텍스트
            source_image:  원본 이미지 (없으면 None)
            variant_type:  선택된 변형 메커니즘 유형
            num_variants:  생성할 변형 문항 수

        Returns:
            AI가 생성한 Raw 텍스트 응답
        """
        prompt = build_variant_prompt(source_text, variant_type, num_variants)

        contents = []
        if source_image is not None:
            contents.append(source_image)
        contents.append(prompt)

        response = self.model.generate_content(contents)
        return response.text

    def parse_result(self, raw_result: str):
        """
        AI Raw 텍스트에서 특수 토큰 태그를 기준으로 문제부와 해설부를 분리합니다.

        Args:
            raw_result: generate_variants()가 반환한 Raw 텍스트

        Returns:
            (questions, explanations): 각각 str 리스트
        """
        q_pattern = re.compile(
            rf"\{Q_TAG_START}(.*?)\{Q_TAG_END}", re.DOTALL
        )
        e_pattern = re.compile(
            rf"\{E_TAG_START}(.*?)\{E_TAG_END}", re.DOTALL
        )

        questions    = [q.strip() for q in q_pattern.findall(raw_result)]
        explanations = [e.strip() for e in e_pattern.findall(raw_result)]

        if not questions:
            questions    = [raw_result]
            explanations = ["해설 포맷 분리 실패 - Raw 데이터를 참조하십시오."]

        return questions, explanations
