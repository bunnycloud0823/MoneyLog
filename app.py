import streamlit as st
import database as db
import utils
import pages

st.set_page_config(
    page_title="개인 가계부",
    layout="centered",
    initial_sidebar_state="collapsed"
)

db.init_db()
utils.apply_toss_style()

st.markdown("<h2 style='text-align: center; color: #191f28; margin-bottom: 20px;'>나만의 가계부</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["홈", "거래 관리", "캘린더", "통계 및 분석", "자산 및 설정"])

with tab1:
    pages.render_home()
    
with tab2:
    pages.render_transactions()
    
with tab3:
    pages.render_calendar()
    
with tab4:
    pages.render_stats()
    
with tab5:
    pages.render_settings()
