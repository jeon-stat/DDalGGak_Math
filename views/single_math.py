# views/single_math.py
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import google.generativeai as genai
import re

# 🎨 UI 및 사이드바 컴팩트 스타일
st.markdown("""
<style>
.stTextArea textarea, .stTextInput input, .stSelectbox div { 
    background-color: var(--background-color) !important; 
    border: 1.5px solid rgba(128, 128, 128, 0.3) !important; 
    color: var(--text-color) !important; 
    border-radius: 8px !important; 
}
[data-testid="stSidebar"] { font-size: 0.85rem !important; }
[data-testid="stSidebar"] h2 { font-size: 1.2rem !important; }
[data-testid="stSidebar"] .stHeader { font-size: 0.95rem !important; font-weight: 600 !important; }

/* 💡 프리뷰 컴포넌트 여백 초기화 및 테두리 스킨 */
iframe { display: block; margin: 0 auto !important; border: 1px solid rgba(128,128,128,0.2) !important; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0;'>📐 DDalGGak Math</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; opacity:0.6; margin-bottom:20px;'>Premium EdTech SaaS</p>", unsafe_allow_html=True)
    st.write("현재 위치: **🏠 Home > 📐 변형**")
    st.divider()
    st.header("⚙️ 출제 옵션")
    api_key = st.text_input("Gemini API Key", type="password")
    num_variants = st.slider("문항 수", 1, 5, 1)
    variant_type = st.radio("변형 유형", ["유형 1: 숫자 변형", "유형 2: 발문 비틀기", "유형 3: 킬러 위장"])

st.title("📐 AI 단일 문항 변형 엔진")
st.write("")

input_method = st.radio("입력 방식", ["📷 이미지 업로드", "✍️ 직접 입력"])
source_text, source_image = "", None

if input_method == "✍️ 직접 입력":
    source_text = st.text_area("원본 문제 입력", height=150)
else:
    uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        source_image = Image.open(uploaded_file)
        st.image(source_image, caption="원본 기출문제 프리뷰", width=280)

if 'qs' not in st.session_state: st.session_state.qs = []
if 'es' not in st.session_state: st.session_state.es = []
if 'res' not in st.session_state: st.session_state.res = None

# =======================================================================================
# 💡 [핵심 방어선] 초록색 박스(인라인 코드)를 완벽하게 파괴하고 수식 기호 $로 변환하는 클리너
# =======================================================================================
def clean_latex(text):
    if not text: return text
    # 1. 마크다운 코드 블록 (```math ... ```) 강제 제거
    text = re.sub(r'
http://googleusercontent.com/immersive_entry_chip/0

---

### 🚀 최종 확인 방법
1. 위 두 파일의 코드를 모두 교체하고 저장(`Commit`)해 주세요.
2. 우측 하단의 **`Reboot app`**을 눌러주세요.
3. **매우 중요:** 세션에 남아있는 이전의 잘못된 데이터를 밀어내기 위해 **반드시 [AI 변형 실행 (딸깍)] 버튼을 눌러 문항을 새로 하나 생성해 주셔야 합니다.**

새로 생성된 문항을 확인해 보시면, 배경색이 완벽히 하얀색으로 깔끔하게 통일되고, 문제와 선지가 줄바꿈으로 예쁘게 나뉘어 있으며, 해설 역시 초록색 박스 없이 완벽한 수학 기호로 렌더링된 것을 확인하실 수 있을 것입니다. 거듭 죄송하고, 또 감사합니다.
