import streamlit as st

def apply_mobile_app_style():
    st.markdown("""
    <style>
        /* Streamlit 기본 헤더/푸터/메뉴 숨기기 */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        
        /* 전체 배경 (웹 데스크탑 화면에서 앱 프레임 바깥 영역) */
        [data-testid="stAppViewContainer"] {
            background-color: #F2F4F8;
        }
        
        /* 모바일 앱 컨테이너 폭 제한 (최대 430px) 및 중앙 정렬 */
        .main .block-container {
            max-width: 430px !important;
            margin: 0 auto !important;
            padding-top: 60px !important;    /* 상단 고정 헤더 높이만큼 여백 */
            padding-bottom: 90px !important; /* 하단 고정 메뉴 높이만큼 여백 */
            padding-left: 16px !important;
            padding-right: 16px !important;
            background-color: #FFFFFF;
            min-height: 100vh;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
            overflow-y: auto;
        }

        /* 1. 상단 고정 헤더 (Sticky Header) */
        .sticky-header {
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 430px;
            height: 54px;
            background-color: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            border-bottom: 1px solid #F0F2F5;
            z-index: 9999;
        }
        .app-title {
            font-size: 14px;
            font-weight: 700;
            color: #3182F6; /* 토스 블루 */
        }
        .page-title {
            font-size: 18px;
            font-weight: 700;
            color: #191F28;
        }

        /* 2. 카드(Card) UI 기본 스타일 */
        .card {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
            border: 1px solid #F0F2F5;
            margin-bottom: 16px;
        }

        /* 3. 하단 네비게이션 바 고정 */
        .bottom-nav-container {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 430px;
            height: 70px;
            background-color: #FFFFFF;
            border-top: 1px solid #F0F2F5;
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 9998;
        }

        /* 4. 플로팅 액션 버튼 (FAB - 지출 추가) */
        .fab-button {
            position: fixed;
            bottom: 85px;
            left: calc(50% + 135px); /* 430px 폭 기준 우측 하단 배치 */
            width: 56px;
            height: 56px;
            background-color: #3182F6;
            color: white !important;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0 4px 16px rgba(49, 130, 246, 0.4);
            text-decoration: none;
            z-index: 9999;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .fab-button:hover {
            transform: scale(1.05);
        }

        /* 5. 캘린더 UI 커스텀 스타일 (첨부 사진 완벽 반영) */
        .calendar-table {
            width: 100%;
            border-collapse: collapse;
            text-align: center;
            margin-top: 10px;
        }
        .calendar-table th {
            padding-bottom: 14px;
            font-size: 13px;
            font-weight: 600;
        }
        .calendar-table td {
            padding: 10px 0;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
        }
        .sun { color: #FF5252; } /* 일요일: 빨간색/분홍색 */
        .sat { color: #3182F6; } /* 토요일: 파란색 */
        .weekday { color: #333333; }
        
        /* 선택된 날짜 (원형 분홍색 하이라이트) */
        .selected-day {
            background-color: #FFEBEE;
            color: #FF5252 !important;
            font-weight: 700;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: inline-block;
            line-height: 36px;
        }
    </style>
    """, unsafe_allow_html=True)
