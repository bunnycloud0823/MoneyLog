import streamlit as st

def apply_mobile_app_style():
    st.markdown("""
    <style>
        /* Streamlit 기본 툴바/헤더/푸터 숨기기 */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        
        /* 웹 전체 화면 배경 (모바일 프레임 외부) */
        [data-testid="stAppViewContainer"] {
            background-color: #0F172A;
        }
        
        /* 모바일 프레임 (최대 430px 폭 제한 및 고정 여백) */
        .main .block-container {
            max-width: 430px !important;
            margin: 0 auto !important;
            padding-top: 54px !important;
            padding-bottom: 95px !important;
            padding-left: 16px !important;
            padding-right: 16px !important;
            background-color: #FFF8F6;
            min-height: 100vh;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.4);
            border-radius: 30px;
            overflow-x: hidden;
        }

        /* 상단 고정 바 */
        .sticky-header {
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 430px;
            height: 54px;
            background-color: rgba(255, 248, 246, 0.95);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            border-bottom: 1px solid #F0E6E4;
            z-index: 9999;
            border-top-left-radius: 30px;
            border-top-right-radius: 30px;
        }
        .header-time { font-size: 13px; font-weight: 700; color: #555555; }
        .header-title { font-size: 15px; font-weight: 800; color: #FF5252; }

        /* 공통 카드 UI */
        .card {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
            border: 1px solid #F5EBE9;
            margin-bottom: 16px;
        }

        /* 홈 화면: 오렌지/코랄 그라데이션 잔액 카드 */
        .gradient-card {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFB199 100%);
            border-radius: 24px;
            padding: 24px 20px;
            color: #FFFFFF;
            box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
            margin-bottom: 16px;
        }
        .gradient-title { font-size: 13px; font-weight: 600; opacity: 0.9; margin-bottom: 4px; }
        .gradient-balance { font-size: 28px; font-weight: 800; margin-bottom: 18px; letter-spacing: -0.5px; }
        .gradient-sub-row { display: flex; border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 12px; }
        .gradient-sub-item { flex: 1; }
        .gradient-sub-label { font-size: 11px; opacity: 0.8; }
        .gradient-sub-val { font-size: 15px; font-weight: 700; }

        /* 카테고리별 요약 가로 스크롤 영역 */
        .cat-grid { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 8px; }
        .cat-box {
            min-width: 75px;
            background: #FFFFFF;
            border: 1px solid #F0E6E4;
            border-radius: 16px;
            padding: 12px 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }
        .cat-name { font-size: 13px; font-weight: 700; color: #333333; margin-bottom: 4px; }
        .cat-amt { font-size: 13px; font-weight: 800; color: #FF5252; }

        /* 거래 내역 리스트 행 */
        .tx-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #F5EBE9;
        }
        .tx-row:last-child { border-bottom: none; }
        .tx-title { font-size: 15px; font-weight: 700; color: #191F28; }
        .tx-sub { font-size: 12px; color: #8B95A1; margin-top: 2px; }
        .tx-minus { font-size: 15px; font-weight: 800; color: #FF5252; }
        .tx-plus { font-size: 15px; font-weight: 800; color: #00C48C; }

        /* 캘린더 테이블 */
        .calendar-table { width: 100%; border-collapse: collapse; text-align: center; margin-top: 10px; }
        .calendar-table th { padding-bottom: 14px; font-size: 13px; font-weight: 700; }
        .calendar-table td { padding: 10px 0; font-size: 15px; font-weight: 600; cursor: pointer; }
        .sun { color: #FF5252; }
        .sat { color: #3182F6; }
        .weekday { color: #333333; }
        .selected-day {
            background-color: #FFEBEE;
            color: #FF5252 !important;
            font-weight: 800;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: inline-block;
            line-height: 36px;
        }

        /* 통계 바 차트 */
        .bar-container { display: flex; align-items: flex-end; justify-content: space-around; height: 150px; padding-top: 20px; border-bottom: 1px solid #E5E8EB; }
        .bar-group { text-align: center; width: 40px; }
        .bar-fill { width: 20px; margin: 0 auto; background: #FF6B6B; border-radius: 6px 6px 0 0; }
        .bar-label { font-size: 12px; color: #666666; margin-top: 8px; font-weight: 600; }

        /* 하단 고정 네비게이션 바 및 플로팅(+) 버튼 연동 */
        div[data-testid="stHorizontalBlock"]:last-of-type {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 430px;
            background-color: #FFFFFF;
            border-top: 1px solid #F0E6E4;
            padding: 8px 16px;
            z-index: 9998;
            border-bottom-left-radius: 30px;
            border-bottom-right-radius: 30px;
        }
        
        div.stButton > button {
            border-radius: 12px;
            font-weight: 700;
            border: 1px solid #E5E8EB;
        }
        div.stButton > button[kind="primary"] {
            background-color: #FF5252;
            color: white;
            border: none;
            box-shadow: 0 4px 12px rgba(255, 82, 82, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)
