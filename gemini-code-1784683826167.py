import streamlit as st

def apply_toss_style():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    body {
        background-color: #f9f9f9;
        color: #191f28;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #f9f9f9;
        max-width: 100%;
        padding-top: 1rem;
    }
    
    .toss-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #f0f0f0;
    }
    
    .toss-title {
        font-size: 14px;
        font-weight: 600;
        color: #8b95a1;
        margin-bottom: 8px;
    }
    
    .toss-value {
        font-size: 24px;
        font-weight: 700;
        color: #191f28;
    }
    
    .toss-blue {
        color: #3182f6;
    }
    
    .toss-red {
        color: #f04452;
    }
    
    div[data-testid="stButton"] > button {
        background-color: #3182f6;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #1b64da;
        color: white;
    }
    
    div[data-testid="stTabs"] button[role="tab"] {
        font-size: 16px;
        font-weight: 600;
        color: #8b95a1;
        padding: 10px 16px;
    }
    
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #3182f6;
        border-bottom: 2px solid #3182f6;
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