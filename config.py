# config.py
# 전역 설정 및 상수를 이 파일 하나에서 관리합니다.
# 모델 변경, 태그 수정 등 공통 값은 반드시 여기서만 수정하세요.

# ── AI 모델 ──────────────────────────────────────────────
MODEL_NAME = "gemini-2.5-flash"

# ── 파싱용 특수 태그 ──────────────────────────────────────
Q_TAG_START = "[QUESTION_START]"
Q_TAG_END   = "[QUESTION_END]"
E_TAG_START = "[EXPLANATION_START]"
E_TAG_END   = "[EXPLANATION_END]"

# ── 앱 메타 정보 ──────────────────────────────────────────
APP_TITLE   = "DDalGGak Math Pro - 프리미엄 AI 수학 문제 변형 플랫폼"
APP_ICON    = "📐"
