import streamlit as st


def apply_mobile_app_style():
    st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

* { font-family: 'Pretendard', sans-serif; box-sizing: border-box; }
html, body, .stApp { background: #F6F1EC; }
header, footer, #MainMenu { visibility: hidden; }

[data-testid="stAppViewContainer"] { background: #F6F1EC; }

.main .block-container {
    max-width: 430px;
    margin: auto;
    background: #FFF8F5;
    min-height: 100vh;
    padding: 78px 18px 100px 18px;
    border-radius: 30px;
    box-shadow: 0 20px 45px rgba(0,0,0,.15);
}

::-webkit-scrollbar { width: 0; height: 0; }

/* 상단 헤더 */
.sticky-header {
    position: fixed; top: 0; left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 430px; height: 64px;
    background: rgba(255,248,245,.95); backdrop-filter: blur(18px);
    display: flex; flex-direction: column; justify-content: center;
    padding: 0 22px; z-index: 9999;
    border-bottom: 1px solid #F1E7E1; border-radius: 30px 30px 0 0;
}
.header-time { font-size: 11px; color: #B7ADA4; font-weight: 600; }
.header-title { font-size: 19px; font-weight: 800; color: #2B2320; margin-top: 1px; }

/* 카드 공통 */
.card {
    background: #fff; border-radius: 22px; padding: 18px; margin-bottom: 16px;
    box-shadow: 0 5px 16px rgba(0,0,0,.04); border: 1px solid #F5EBE9;
}

/* 잔액 그라데이션 카드 */
.gradient-card {
    position: relative; overflow: hidden; border-radius: 24px; padding: 24px;
    margin-bottom: 18px; color: #fff;
    background: linear-gradient(135deg, #FF9A76 0%, #FF5E62 100%);
    box-shadow: 0 12px 28px rgba(255,94,98,.28);
}
.gradient-card::after {
    content: ""; position: absolute; right: -30px; top: -30px;
    width: 140px; height: 140px; border-radius: 50%;
    background: rgba(255,255,255,.14);
}
.gradient-title { font-size: 13px; font-weight: 700; opacity: .92; }
.gradient-balance { font-size: 32px; font-weight: 900; margin: 10px 0 20px 0; letter-spacing: -1px; }
.gradient-sub-row { display: flex; gap: 14px; border-top: 1px solid rgba(255,255,255,.25); padding-top: 14px; }
.gradient-sub-item { flex: 1; }
.gradient-sub-label { font-size: 12px; opacity: .85; margin-bottom: 3px; }
.gradient-sub-val { font-size: 16px; font-weight: 800; }

/* 카테고리 가로 스크롤 */
.cat-grid { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 4px; }
.cat-box {
    min-width: 78px; background: #fff; border: 1px solid #F5EBE9; border-radius: 18px;
    padding: 12px 10px; text-align: center; flex-shrink: 0;
}
.cat-icon { font-size: 20px; margin-bottom: 4px; }
.cat-name { font-size: 11px; font-weight: 700; color: #7A7168; }
.cat-amt { font-size: 13px; font-weight: 900; color: #FF5E62; margin-top: 3px; }

/* 캘린더 */
.calendar-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.calendar-table th { padding: 6px 0 10px 0; font-size: 12px; font-weight: 800; color: #B7ADA4; }
.cal-day-summary { text-align: center; min-height: 26px; margin-top: -6px; }
.cal-pill { font-size: 9.5px; font-weight: 800; line-height: 1.3; }
.cal-pill.income { color: #2BC194; }
.cal-pill.expense { color: #FF5E62; }
.sun { color: #FF5E62 !important; }
.sat { color: #4A8CFF !important; }
.weekday { color: #2B2320; }
.today-dot::after {
    content: ""; display: block; width: 4px; height: 4px; border-radius: 50%;
    background: #FF9A76; margin: 2px auto 0 auto;
}

/* 캘린더 날짜 버튼 (streamlit button 재활용) */
div[data-testid="stVerticalBlock"] div.stButton > button {
    width: 34px; height: 34px; min-width: 34px; padding: 0; margin: 0 auto;
    border-radius: 50%; font-weight: 700; font-size: 13px;
    border: 1px solid transparent; background: transparent; color: #2B2320; box-shadow: none;
}
div[data-testid="stVerticalBlock"] div.stButton > button:hover {
    background: #FFF1EE; border-color: #FFD4CB; color: #FF5E62;
}

/* 거래 내역 행 */
.tx-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 4px; border-bottom: 1px solid #F7F0EE;
}
.tx-row:last-child { border-bottom: none; }
.tx-title { font-size: 14.5px; font-weight: 800; color: #2B2320; }
.tx-sub { font-size: 12px; color: #A79E95; margin-top: 2px; }
.tx-plus { color: #2BC194; font-size: 15px; font-weight: 900; }
.tx-minus { color: #FF5E62; font-size: 15px; font-weight: 900; }

/* 통계 바 차트 */
.bar-container { display: flex; justify-content: space-around; align-items: flex-end; height: 150px; padding-top: 10px; }
.bar-group { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.bar-fill { width: 34px; border-radius: 10px 10px 4px 4px; background: linear-gradient(180deg, #FF9A76, #FF5E62); }
.bar-label { font-size: 12px; font-weight: 700; color: #A79E95; }

/* 빈 상태 */
.empty-state { text-align: center; padding: 34px 10px; color: #C6BDB4; font-size: 13.5px; }

/* 버튼 */
div.stButton > button {
    width: 100%; border-radius: 14px; font-weight: 800; border: 1px solid #F1E7E1;
    background: #fff; color: #4B443E; height: 42px;
}
div.stButton > button[kind="primary"] {
    background: #FF5E62; color: #fff; border: none; box-shadow: 0 4px 12px rgba(255,94,98,.25);
}

/* 입력 필드 */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input {
    border-radius: 14px !important; border: 1px solid #F1E7E1 !important; background: #fff !important;
}
div[data-testid="stSelectbox"] > div { border-radius: 14px !important; border-color: #F1E7E1 !important; }

/* 하단 네비게이션 */
.bottom-nav-spacer { height: 8px; }
</style>
    """, unsafe_allow_html=True)
