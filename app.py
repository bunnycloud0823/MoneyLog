import streamlit as st
import database as db
import utils
import pages

# 모바일 최적화를 위한 레이아웃 설정
st.set_page_config(
    page_title="나만의 가계부",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DB 초기화 및 따뜻한 토스 스타일 CSS 적용
db.init_db()
utils.apply_toss_style()

# 상단 헤더
st.markdown("<h2 style='text-align: center; color: #222222; font-weight: 800; margin-bottom: 25px;'>🌸 나만의 가계부</h2>", unsafe_allow_html=True)

# 메인 네비게이션 탭 (첫 화면에 캘린더가 있는 홈 탭 배치)
tab1, tab2, tab3, tab4 = st.tabs(["🏠 홈 (캘린더)", "📝 전체 내역", "📊 통계", "⚙️ 자산/설정"])

with tab1:
    pages.render_home()
    
with tab2:
    pages.render_transactions()
    
with tab3:
    pages.render_stats()
    
with tab4:
    pages.render_settings()
