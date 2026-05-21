# app.py
import streamlit as st

st.set_page_config(page_title="DDalGGak Math - AI 수학 문제 변형 SaaS", page_icon="📐", layout="wide")

st.markdown("""
    <style>
    .hero-section { text-align: center; padding: 80px 20px; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); color: white; border-radius: 12px; margin-bottom: 50px; }
    .hero-title { font-size: 3.2rem; font-weight: 800; margin-bottom: 20px; }
    .hero-subtitle { font-size: 1.4rem; color: #94A3B8; margin-bottom: 40px; }
    .feature-card { background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; text-align: center; height: 100%; }
    .price-card { border: 2px solid #3B82F6; background-color: #ffffff; padding: 40px 30px; border-radius: 12px; text-align: center; box-shadow: 0 10px 25px rgba(59,130,246,0.1); }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-section">
        <div class="hero-title">수학 교재 제작의 신세계, DDalGGak Math</div>
        <div class="hero-subtitle">시험지 이미지 업로드 단 한번으로, 평가원 감성의 무결성 변형 문제를 '딸깍' 찍어내세요.</div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.info("💡 왼쪽 메뉴에서 **[📐 DDalGGak Math]**를 누르시면 바로 AI 문제 변형 엔진을 사용할 수 있습니다!")

st.markdown("### ✨ 왜 DDalGGak Math 인가요?")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='feature-card'><h4>📐 평가원급 역산 설계</h4><p>정답이 소름 돋게 딱 떨어지는 정갈한 수치를 제공합니다.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='feature-card'><h4>📦 실물 시험지 완벽 복제</h4><p>수능형 보기 상자와 5지선다 배치를 완벽 재현합니다.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='feature-card'><h4>🔥 사고과정 공유 변형</h4><p>핵심 논리만 상속받고 겉모습을 위장한 킬러 문항을 창조합니다.</p></div>", unsafe_allow_html=True)

st.divider()
st.markdown("### 💳 합리적인 강사 전용 요금제")
p_col1, p_col2 = st.columns([1, 2])
with p_col1:
    st.markdown("<div class='price-card'><h3>강사 프리미엄</h3><h2 style='color:#3B82F6;'>월 39,000원</h2><p>과외/학원 내신 기출 변형 무제한 생성</p></div>", unsafe_allow_html=True)
with p_col2:
    st.markdown("### 🚀 지금 바로 무료로 체험해 보세요")
    st.warning("👈 왼쪽 사이드바 메뉴에서 **[📐 DDalGGak Math]**를 딸깍 누르시면 변형기 화면으로 바로 진입합니다!")