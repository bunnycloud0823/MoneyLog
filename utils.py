# utils.py
import streamlit as st

def apply_toss_style():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    body, .stApp {
        background-color: #fdfbf7 !important;
        color: #333333;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 따뜻하고 귀여운 카드 CSS */
    .toss-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        border: 1.5px solid #f2eee8;
    }
    
    .card-balance {
        background: linear-gradient(135ff, #ff7e87 0%, #ff5c6a 100%);
        color: white;
        border: none;
    }
    
    .card-income {
        background: #ffffff;
        border: 1.5px solid #e2f3e8;
    }
    
    .card-expense {
        background: #ffffff;
        border: 1.5px solid #fde8ea;
    }

    .toss-title {
        font-size: 14px;
        font-weight: 600;
        color: #888888;
        margin-bottom: 6px;
    }
    
    .card-balance .toss-title {
        color: rgba(255, 255, 255, 0.9);
    }
    
    .toss-value {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .toss-blue { color: #2bc194; } /* 맑은 민트 수입 */
    .toss-red { color: #ff5c6a; }  /* 따뜻한 코랄 핑크 지출 */
    
    /* 버튼 스타일링 */
    div[data-testid="stButton"] > button {
        background-color: #ff5c6a;
        color: white;
        border-radius: 14px;
        border: none;
        padding: 0.6rem 1rem;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 4px 10px rgba(255, 92, 106, 0.2);
        transition: all 0.2s ease;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #f04452;
        color: white;
        transform: translateY(-2px);
    }
    
    /* 탭 스타일 */
    div[data-testid="stTabs"] button[role="tab"] {
        font-size: 16px;
        font-weight: 700;
        color: #a09a93;
        padding: 12px 18px;
        background: transparent;
    }
    
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #ff5c6a;
        border-bottom: 3px solid #ff5c6a;
    }
    
    /* 입력 폼 필드 디자인 */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] div {
        border-radius: 12px !important;
        border-color: #e8e3dc !important;
        background-color: #ffffff !important;
    }
    
    /* 캘린더 요일/날짜 셀 커스텀 */
    .cal-header {
        font-weight: 700;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

def format_currency(amount):
    if amount is None:
        return "0원"
    return f"{int(amount):,}원"

def get_current_year_month():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m")
