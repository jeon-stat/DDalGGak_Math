# DDalGGak Math

AI가 보조하는 수학 문제 변형과 복습을 위한 Streamlit 기반 학습 도구입니다.

## 요약

이 프로젝트는 연습과 복습을 위한 작은 웹 앱입니다.

- 홈 화면과 여러 학습 모드
- 단일 문제 변형 생성
- 실전 시험 형태의 연습 모드
- 어려운 문제를 모아두는 질문함
- 커스텀 스타일과 가벼운 로컬 실행 흐름

## 프로젝트 구조

- `app.py`: Streamlit 진입점
- `views/`: 학습 모드별 화면 정의
- `renderers/`: UI 렌더링 보조 코드
- `components.py`: 공통 Streamlit 컴포넌트
- `styles.py`: 공통 CSS
- `config.py`: 앱 제목과 아이콘 설정
- `launch_app.ps1` 및 `DDalGGak Math 열기.bat`: 로컬 실행 보조 스크립트

## 실행

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Windows에서는 제공된 실행 스크립트를 사용해도 됩니다.

## 참고

- 이 저장소는 주로 로컬 학습용 앱입니다.
- 프로젝트 파일에서 공개 배포 사이트는 확인되지 않았기 때문에, 로컬 실행 경로 중심으로 정리했습니다.
