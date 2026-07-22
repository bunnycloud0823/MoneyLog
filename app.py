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

# 현재 선택된 탭 및 날짜 상태 관리 (요청에 따라 첫 화면을 캘린더로 설정)
if 'current_tab' not in st.session_state:
    st.session_state['current_tab'] = 'Calendar'
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.today().day
if 'selected_year_month' not in st.session_state:
    st.session_state['selected_year_month'] = datetime.today().strftime("%Y-%m")
if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False
if 'tx_type' not in st.session_state:
    st.session_state['tx_type'] = '지출'

# --- [상단 고정 헤더] ---
st.markdown(f"""
<div class="sticky-header">
    <span class="app-title">Moneylog</span>
    <span class="page-title">{st.session_state['current_tab']}</span>
</div>
""", unsafe_allow_html=True)

# --- [내역 추가 모달 / 화면 영역] ---
if st.session_state['show_modal']:
    st.markdown("""
    <div class="card" style="border: 2px solid #FF7A7A; background-color: #FFFBFB; margin-top: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 18px; font-weight: 800; color: #191F28;">내역 추가</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_type1, col_type2 = st.columns(2)
    with col_type1:
        if st.button("지출", use_container_width=True, type="primary" if st.session_state['tx_type']=='지출' else "secondary"):
            st.session_state['tx_type'] = '지출'
            st.rerun()
    with col_type2:
        if st.button("수입", use_container_width=True, type="primary" if st.session_state['tx_type']=='수입' else "secondary"):
            st.session_state['tx_type'] = '수입'
            st.rerun()

    amount = st.text_input("금액 (원)", placeholder="금액을 입력하세요")
    category = st.selectbox("카테고리", ["식비", "교통", "쇼핑", "의료", "여가", "주거", "월급/수입"])
    memo = st.text_input("메모", placeholder="사용처나 내용을 입력하세요")
    tx_date = st.date_input("날짜", datetime.today())

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("기록하기", use_container_width=True, type="primary"):
            if amount:
                db.add_transaction(st.session_state['tx_type'], category, float(amount.replace(',', '')), memo, str(tx_date))
                st.session_state['show_modal'] = False
                st.success("내역이 저장되었습니다.")
                st.rerun()
            else:
                st.error("금액을 입력해주세요.")
    with col_btn2:
        if st.button("닫기", use_container_width=True):
            st.session_state['show_modal'] = False
            st.rerun()
            
    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

# --- [콘텐츠 영역 (탭별 라우팅)] ---
if st.session_state['current_tab'] == 'Calendar':
    # 첫 화면: 캘린더 뷰
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #FF9A8B 0%, #FF6A88 100%); color: white; padding: 24px; border-radius: 20px; margin-bottom: 20px;">
        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 6px;">2026년 7월 캘린더</div>
        <div style="font-size: 24px; font-weight: 800;">일별 가계부 한눈에 보기</div>
    </div>
    """, unsafe_allow_html=True)

    # 캘린더 카드 UI
    now = datetime.now()
    year, month = now.year, now.month
    cal = calendar.monthcalendar(year, month)
    
    calendar_html = '<div class="card"><div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">7월 캘린더</div>'
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
                if i == 0: color_class = "sun"
                elif i == 6: color_class = "sat"
                
                if day == st.session_state['selected_date']:
                    calendar_html += f'<td><span class="selected-day">{day}</span></td>'
                else:
                    calendar_html += f'<td><span class="{color_class}">{day}</span></td>'
        calendar_html += '</tr>'
    
    calendar_html += '</tbody></table></div>'
    st.markdown(calendar_html, unsafe_allow_html=True)

    # 선택된 날짜의 내역 카드
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">7월 {st.session_state['selected_date']}일 상세 내역</div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #F0F2F5;">
            <div>
                <div style="font-size: 15px; font-weight: 600;">스타벅스</div>
                <div style="font-size: 12px; color: #8B95A1;">식비 | 카페</div>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #FF5252;">-8,500원</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state['current_tab'] == 'Home':
    # 홈 대시보드 (그라디언트 잔액 카드, 지출/수입 추가 버튼, 카테고리별 지출, 최근 내역)
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #FF9A8B 0%, #FF6A88 100%); color: white; padding: 24px; border-radius: 20px; margin-bottom: 20px;">
        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">이번 달 잔액</div>
        <div style="font-size: 28px; font-weight: 800; margin-bottom: 16px;">+2,137,000원</div>
        <div style="display: flex; gap: 20px; font-size: 14px;">
            <div>수입 <strong style="font-size: 16px;">+353만</strong></div>
            <div>지출 <strong style="font-size: 16px;">-139만</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button("지출 추가", use_container_width=True):
            st.session_state['show_modal'] = True
            st.session_state['tx_type'] = '지출'
            st.rerun()
    with col_h2:
        if st.button("수입 추가", use_container_width=True):
            st.session_state['show_modal'] = True
            st.session_state['tx_type'] = '수입'
            st.rerun()

    st.markdown("""
    <div class="card" style="margin-top: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-size: 16px; font-weight: 700;">카테고리별 지출</span>
            <span style="font-size: 12px; color: #FF6A88; font-weight: 600;">전체 보기</span>
        </div>
        <div style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 6px;">
            <div style="min-width: 70px; text-align: center; background: #F8F9FA; padding: 12px 8px; border-radius: 12px;">
                <div style="font-size: 14px; font-weight: 600;">주거</div>
                <div style="font-size: 13px; color: #FF6A88; font-weight: 700; margin-top: 4px;">60만</div>
            </div>
            <div style="min-width: 70px; text-align: center; background: #F8F9FA; padding: 12px 8px; border-radius: 12px;">
                <div style="font-size: 14px; font-weight: 600;">쇼핑</div>
                <div style="font-size: 13px; color: #FF6A88; font-weight: 700; margin-top: 4px;">32만</div>
            </div>
            <div style="min-width: 70px; text-align: center; background: #F8F9FA; padding: 12px 8px; border-radius: 12px;">
                <div style="font-size: 14px; font-weight: 600;">식비</div>
                <div style="font-size: 13px; color: #FF6A88; font-weight: 700; margin-top: 4px;">21만</div>
            </div>
            <div style="min-width: 70px; text-align: center; background: #F8F9FA; padding: 12px 8px; border-radius: 12px;">
                <div style="font-size: 14px; font-weight: 600;">의료</div>
                <div style="font-size: 13px; color: #FF6A88; font-weight: 700; margin-top: 4px;">15만</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-size: 16px; font-weight: 700;">최근 내역</span>
            <span style="font-size: 12px; color: #FF6A88; font-weight: 600;">전체 보기</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #F0F2F5;">
            <div>
                <div style="font-size: 15px; font-weight: 600;">스타벅스</div>
                <div style="font-size: 12px; color: #8B95A1;">식비 · 카페 · 07/22</div>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #FF5252;">-8,500원</div>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0;">
            <div>
                <div style="font-size: 15px; font-weight: 600;">성과급 일부</div>
                <div style="font-size: 12px; color: #8B95A1;">보너스 · 성과급 · 07/21</div>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #3182F6;">+80,000원</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state['current_tab'] == 'History':
    # 내역 탭
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">전체 거래 내역</div>
        <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #F0F2F5;">
            <div>
                <div style="font-size: 15px; font-weight: 600;">스타벅스</div>
                <div style="font-size: 12px; color: #8B95A1;">식비 | 07/22</div>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #FF5252;">-8,500원</div>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #F0F2F5;">
            <div>
                <div style="font-size: 15px; font-weight: 600;">늦은 귀가 택시</div>
                <div style="font-size: 12px; color: #8B95A1;">교통 | 07/22</div>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #FF5252;">-45,000원</div>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 12px 0;">
            <div>
                <div style="font-size: 15px; font-weight: 600;">월급 입금</div>
                <div style="font-size: 12px; color: #8B95A1;">수입 | 07/10</div>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #3182F6;">+3,530,000원</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state['current_tab'] == 'Stats':
    # 통계 탭
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 12px;">월별 수입·지출 추이</div>
        <div style="height: 140px; display: flex; align-items: flex-end; justify-content: space-around; padding-top: 20px; border-bottom: 1px solid #F0F2F5; padding-bottom: 10px;">
            <div style="text-align: center;"><div style="width: 24px; height: 90px; background: #FF6A88; border-radius: 6px; margin: 0 auto;"></div><div style="font-size: 11px; color: #8B95A1; margin-top: 6px;">5월</div></div>
            <div style="text-align: center;"><div style="width: 24px; height: 85px; background: #FF6A88; border-radius: 6px; margin: 0 auto;"></div><div style="font-size: 11px; color: #8B95A1; margin-top: 6px;">6월</div></div>
            <div style="text-align: center;"><div style="width: 24px; height: 110px; background: #FF6A88; border-radius: 6px; margin: 0 auto;"></div><div style="font-size: 11px; color: #8B95A1; margin-top: 6px;">7월</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 4px;">이번 달 지출 분석</div>
        <div style="font-size: 13px; color: #8B95A1; margin-bottom: 16px;">총 1,393,000원</div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0;">
            <span>주거 (43%)</span>
            <strong style="color: #FF6A88;">600,000원</strong>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0;">
            <span>쇼핑 (23%)</span>
            <strong style="color: #FF6A88;">320,000원</strong>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0;">
            <span>식비 (15%)</span>
            <strong style="color: #FF6A88;">210,000원</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- [우측 하단 고정 플로팅 버튼 (FAB)] ---
if not st.session_state['show_modal']:
    if st.button("+", key="fab_add_btn"):
        st.session_state['show_modal'] = True
        st.rerun()

# --- [하단 고정 네비게이션 바] ---
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("홈", use_container_width=True, key="nav_home"):
        st.session_state['current_tab'] = 'Home'
        st.session_state['show_modal'] = False
        st.rerun()
with nav_col2:
    if st.button("캘린더", use_container_width=True, key="nav_calendar"):
        st.session_state['current_tab'] = 'Calendar'
        st.session_state['show_modal'] = False
        st.rerun()
with nav_col3:
    if st.button("내역", use_container_width=True, key="nav_history"):
        st.session_state['current_tab'] = 'History'
        st.session_state['show_modal'] = False
        st.rerun()
with nav_col4:
    if st.button("통계", use_container_width=True, key="nav_stats"):
        st.session_state['current_tab'] = 'Stats'
        st.session_state['show_modal'] = False
        st.rerun()
