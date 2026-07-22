import streamlit as st
import calendar
from datetime import datetime
from style import apply_mobile_app_style

# 페이지 설정 (폭 제한을 위해 centered 사용)
st.set_page_config(page_title="Moneylog", layout="centered", initial_sidebar_state="collapsed")

# 모바일 앱 스타일 적용
apply_mobile_app_style()

# 현재 선택된 메뉴 상태 관리
if 'current_tab' not in st.session_state:
    st.session_state['current_tab'] = 'Home'
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.today().day

# --- [상단 고정 헤더] ---
st.markdown(f"""
<div class="sticky-header">
    <span class="app-title">Moneylog</span>
    <span class="page-title">{st.session_state['current_tab']}</span>
</div>
""", unsafe_allow_html=True)

# --- [콘텐츠 영역 (스크롤 가능)] ---
if st.session_state['current_tab'] == 'Home':
    # 자산 요약 카드 UI
    st.markdown("""
    <div class="card">
        <div style="font-size: 13px; color: #8B95A1; margin-bottom: 8px;">이번 달 총 지출</div>
        <div style="font-size: 26px; font-weight: 800; color: #191F28;">1,245,000원</div>
    </div>
    """, unsafe_allow_html=True)

    # 캘린더 카드 UI 구현
    now = datetime.now()
    year, month = now.year, now.month
    cal = calendar.monthcalendar(year, month)
    
    calendar_html = '<div class="card"><div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">월별 내역</div>'
    calendar_html += '<table class="calendar-table"><thead><tr>'
    
    # 요일 헤더 (일요일: 빨간색, 토요일: 파란색)
    days_label = [('<span class="sun">일</span>'), '월', '화', '수', '목', '금', '<span class="sat">토</span>']
    for day in days_label:
        calendar_html += f'<th>{day}</th>'
    calendar_html += '</tr></thead><tbody>'
    
    # 날짜 그리드 생성
    for week in cal:
        calendar_html += '<tr>'
        for i, day in enumerate(week):
            if day == 0:
                calendar_html += '<td></td>'
            else:
                # 색상 클래스 결정
                color_class = "weekday"
                if i == 0: color_class = "sun"
                elif i == 6: color_class = "sat"
                
                # 선택된 날짜 (당일 또는 클릭한 날짜) 하이라이트
                if day == st.session_state['selected_date']:
                    calendar_html += f'<td><span class="selected-day">{day}</span></td>'
                else:
                    calendar_html += f'<td><span class="{color_class}">{day}</span></td>'
        calendar_html += '</tr>'
    
    calendar_html += '</tbody></table></div>'
    st.markdown(calendar_html, unsafe_allow_html=True)

    # 최근 내역 카드
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">최근 지출</div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #F0F2F5;">
            <div>
                <div style="font-size: 15px; font-weight: 600;">점심 식대</div>
                <div style="font-size: 12px; color: #8B95A1;">체크카드 | 식비</div>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #191F28;">-12,000원</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- [우측 하단 고정 플로팅 버튼 (FAB)] ---
st.markdown("""
<a href="?action=add" target="_self" class="fab-button">+</a>
""", unsafe_allow_html=True)

# --- [하단 네비게이션 바 고정] ---
st.markdown("""
<div class="bottom-nav-container">
    <a href="?tab=Home" target="_self" style="text-decoration: none; color: #3182F6; font-weight: 700; font-size: 13px;">Home</a>
    <a href="?tab=Account" target="_self" style="text-decoration: none; color: #8B95A1; font-weight: 600; font-size: 13px;">가계부</a>
    <a href="?tab=Stats" target="_self" style="text-decoration: none; color: #8B95A1; font-weight: 600; font-size: 13px;">통계</a>
    <a href="?tab=Settings" target="_self" style="text-decoration: none; color: #8B95A1; font-weight: 600; font-size: 13px;">설정</a>
</div>
""", unsafe_allow_html=True)

# URL 쿼리 파라미터를 통한 네비게이션 탭 전환 처리
query_params = st.query_params
if 'tab' in query_params:
    st.session_state['current_tab'] = query_params['tab']
if 'action' in query_params and query_params['action'] == 'add':
    # 지출 추가 팝업 또는 페이지 진입 로직
    st.toast("지출 추가 창을 엽니다.")
