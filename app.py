import streamlit as st
import calendar
from datetime import datetime
from style import apply_mobile_app_style
import database as db

# 페이지 설정 (모바일 앱 스타일을 위해 centered 레이아웃 사용)
st.set_page_config(page_title="Moneylog", layout="centered", initial_sidebar_state="collapsed")

# 데이터베이스 초기화 실행
db.init_db()

# 모바일 앱 스타일 및 CSS 적용
apply_mobile_app_style()

# 현재 선택된 탭 및 날짜 상태 관리
if 'current_tab' not in st.session_state:
    st.session_state['current_tab'] = 'Home'
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.today().day
if 'selected_year_month' not in st.session_state:
    st.session_state['selected_year_month'] = datetime.today().strftime("%Y-%m")

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

    # 캘린더 카드 UI (이미지 참고: 일요일 분홍/빨강, 토요일 파랑, 선택된 날짜 원형 분홍 하이라이트)
    now = datetime.now()
    year, month = now.year, now.month
    cal = calendar.monthcalendar(year, month)
    
    calendar_html = '<div class="card"><div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">월별 내역</div>'
    calendar_html += '<table class="calendar-table"><thead><tr>'
    
    days_label = [('<span class="sun">일</span>'), '월', '화', '수', '목', '금', '<span class="sat">토</span>']
    for day in days_label:
        calendar_html += f'<th>{day}</th>'
    calendar_html += '</tr></thead><tbody>'
    
    for week in cal:
        calendar_html += '<tr>'
        for i, day in enumerate(week):
            if day == 0:
                calendar_html += '<td></td>'
            else:
                color_class = "weekday"
                if i == 0: 
                    color_class = "sun"
                elif i == 6: 
                    color_class = "sat"
                
                # 선택된 날짜 확인 및 하이라이트 적용
                if day == st.session_state['selected_date']:
                    calendar_html += f'<td><span class="selected-day">{day}</span></td>'
                else:
                    calendar_html += f'<td><span class="{color_class}">{day}</span></td>'
        calendar_html += '</tr>'
    
    calendar_html += '</tbody></table></div>'
    st.markdown(calendar_html, unsafe_allow_html=True)

    # 날짜별 내역 선택 버튼들 (인터랙션 연동용)
    st.markdown("<div style='font-size: 13px; font-weight: 600; color: #6b7684; margin-bottom: 6px;'>날짜 선택하기</div>", unsafe_allow_html=True)
    date_cols = st.columns(7)
    for i in range(1, 8):  # 예시로 1일부터 7일까지 인터랙션 버튼 배치
        with date_cols[(i-1)%7]:
            if st.button(f"{i}일", key=f"date_btn_{i}", use_container_width=True):
                st.session_state['selected_date'] = i
                st.rerun()

    # 최근 지출 내역 카드
    st.markdown("""
    <div class="card" style="margin-top: 16px;">
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

elif st.session_state['current_tab'] == 'Account':
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">가계부 상세 내역</div>
        <div style="color: #8B95A1; font-size: 14px;">등록된 내역이 여기에 표시됩니다.</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state['current_tab'] == 'Stats':
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">소비 통계</div>
        <div style="color: #8B95A1; font-size: 14px;">카테고리별 지출 분석이 제공됩니다.</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state['current_tab'] == 'Settings':
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">설정 및 관리</div>
        <div style="color: #8B95A1; font-size: 14px;">자산 및 카테고리를 관리할 수 있습니다.</div>
    </div>
    """, unsafe_allow_html=True)

# --- [하단 네비게이션 바 고정 영역] ---
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

# 하단 탭 전환 버튼들을 나란히 배치하여 모바일 네비게이션 바 구현
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("홈", use_container_width=True, key="nav_home"):
        st.session_state['current_tab'] = 'Home'
        st.rerun()
with nav_col2:
    if st.button("가계부", use_container_width=True, key="nav_account"):
        st.session_state['current_tab'] = 'Account'
        st.rerun()
with nav_col3:
    if st.button("통계", use_container_width=True, key="nav_stats"):
        st.session_state['current_tab'] = 'Stats'
        st.rerun()
with nav_col4:
    if st.button("설정", use_container_width=True, key="nav_settings"):
        st.session_state['current_tab'] = 'Settings'
        st.rerun()

# 지출 추가 플로팅 버튼
if st.button("+ 지출 추가", use_container_width=True, type="primary"):
    st.toast("지출 추가 창이 열립니다.")
