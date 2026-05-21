# ai_engine.py
import google.generativeai as genai
import re
from templates import SYSTEM_PROMPT

class DDalGGakEngine:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_variants(self, source_text: str, source_image, variant_type: str, num_variants: int) -> str:
        user_prompt = f"""
        [출제 요청 파라미터]
        - 변형 유형: {variant_type}
        - 생성 문항 수: {num_variants}개
        
        [원본 정보]
        {source_text if source_text else '제공된 이미지를 시각적으로 파악하여 분석할 것'}
        """
        contents = [SYSTEM_PROMPT, user_prompt]
        if source_image:
            contents.append(source_image)
            
        response = self.model.generate_content(contents)
        return response.text

    @staticmethod
    def parse_result(raw_text: str):
        questions = re.findall(r'###\s*\[?변형\s*문항\s*\d+\]?(.*?)(?=###\s*\[?정답|$)', raw_text, re.DOTALL)
        explanations = re.findall(r'###\s*\[?정답\s*및\s*상세\s*해설\s*\d+\]?(.*?)(?=###\s*\[?변형|$)', raw_text, re.DOTALL)
        return questions, explanations