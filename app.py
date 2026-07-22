import streamlit as st
import calendar
from datetime import datetime
from style import apply_mobile_app_style
import database as db

# 1. 페이지 설정 및 DB 초기화
st.set_page_config(page_title="Moneylog", layout="centered", initial_sidebar_state="collapsed")
db.init_db()
apply_mobile_app_style()

# 2. 상태 관리 (첫 화면은 반드시 '캘린더'로 시작)
if 'current_tab' not in st.session_state:
    st.session_state['current_tab'] = '캘린더'
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.today().day
if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False

now = datetime.now()
curr_year = now.year
curr_month = now.month

# --- [상단 고정 헤더] ---
now_str = now.strftime("%p %I:%M").replace("AM", "오전").replace("PM", "오후")
st.markdown(f"""
<div class="sticky-header">
    <span class="header-time">{now_str}</span>
    <span class="header-title">가계부 [{st.session_state['current_tab']}]</span>
</div>
""", unsafe_allow_html=True)

# --- [내역 추가 모달 창 (DB 저장 연동)] ---
if st.session_state['show_modal']:
    st.markdown("""
    <div class="card" style="border: 2px solid #FF5252; background: #FFFDFD;">
        <div style="font-size: 18px; font-weight: 800; color: #191F28; margin-bottom: 12px;">새 내역 추가</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        tx_type = st.radio("유형 선택", ["지출", "수입"], horizontal=True)
        tx_amt = st.number_input("금액 (원)", min_value=0, step=1000, value=10000)
        tx_cat = st.selectbox("카테고리", ["식비", "교통", "쇼핑", "의료", "여가", "주거", "급여", "보너스", "기타"])
        tx_sub = st.text_input("세부 항목", "외식")
        tx_memo = st.text_input("상세 내용 (지출처/수입처)", "점심 식사")
        tx_date = st.date_input("날짜 선택", datetime.today())
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("취소", use_container_width=True):
                st.session_state['show_modal'] = False
                st.rerun()
        with col_m2:
            if st.button("기록 저장", type="primary", use_container_width=True):
                date_str = tx_date.strftime("%Y-%m-%d")
                db.add_transaction(tx_memo, tx_cat, tx_sub, date_str, tx_amt, tx_type)
                st.session_state['show_modal'] = False
                st.rerun()
    st.write("---")

# --- [메인 화면 렌더링] ---

# [1. 캘린더 화면]
if st.session_state['current_tab'] == '캘린더':
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 18px; font-weight: 800; color: #191F28; margin-bottom: 12px;">{curr_year}년 {curr_month}월</div>
        <table class="calendar-table">
            <thead>
                <tr>
                    <th><span class="sun">일</span></th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th><span class="sat">토</span></th>
                </tr>
            </thead>
            <tbody>
    """, unsafe_allow_html=True)
    
    cal = calendar.monthcalendar(curr_year, curr_month)
    cal_html = ""
    for week in cal:
        cal_html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                cal_html += "<td></td>"
            else:
                color_class = "weekday"
                if i == 0: color_class = "sun"
                elif i == 6: color_class = "sat"
                
                if day == st.session_state['selected_date']:
                    cal_html += f'<td><span class="selected-day">{day}</span></td>'
                else:
                    cal_html += f'<td><span class="{color_class}">{day}</span></td>'
        cal_html += "</tr>"
    
    st.markdown(cal_html + "</tbody></table></div>", unsafe_allow_html=True)
    
    # 선택된 날짜의 실제 DB 조회 내역 표시
    target_date_str = f"{curr_year:04d}-{curr_month:02d}-{st.session_state['selected_date']:02d}"
    daily_txs = db.get_transactions_by_date(target_date_str)
    
    st.markdown(f'<div class="card"><div style="font-size: 15px; font-weight: 700; margin-bottom: 10px;">{curr_month}월 {st.session_state["selected_date"]}일 내역</div>', unsafe_allow_html=True)
    if not daily_txs:
        st.markdown('<div style="color: #8B95A1; font-size: 14px; padding: 10px 0;">등록된 내역이 없습니다.</div>', unsafe_allow_html=True)
    else:
        for tx in daily_txs:
            amt_str = f"+{tx['amount']:,}원" if tx['tx_type'] == '수입' else f"-{tx['amount']:,}원"
            color_cls = "tx-plus" if tx['tx_type'] == '수입' else "tx-minus"
            st.markdown(f"""
            <div class="tx-row">
                <div>
                    <div class="tx-title">{tx['name']}</div>
                    <div class="tx-sub">{tx['category']} | {tx['sub_category']}</div>
                </div>
                <div class="{color_cls}">{amt_str}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# [2. 홈 화면 (대시보드)]
elif st.session_state['current_tab'] == '홈':
    summary = db.get_month_summary(curr_year, curr_month)
    bal_str = f"+{summary['잔액']:,}원" if summary['잔액'] >= 0 else f"{summary['잔액']:,}원"
    
    # 오렌지/코랄 그라데이션 잔액 카드
    st.markdown(f"""
    <div class="gradient-card">
        <div class="gradient-title">이번 달 잔액</div>
        <div class="gradient-balance">{bal_str}</div>
        <div class="gradient-sub-row">
            <div class="gradient-sub-item">
                <div class="gradient-sub-label">수입</div>
                <div class="gradient-sub-val">+{summary['수입']:,}원</div>
            </div>
            <div class="gradient-sub-item">
                <div class="gradient-sub-label">지출</div>
                <div class="gradient-sub-val">-{summary['지출']:,}원</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("지출 추가", use_container_width=True):
            st.session_state['show_modal'] = True
            st.rerun()
    with col_btn2:
        if st.button("수입 추가", use_container_width=True):
            st.session_state['show_modal'] = True
            st.rerun()

    # 실제 DB 기반 카테고리 지출 요약
    cat_expenses = db.get_category_expenses(curr_year, curr_month)
    st.markdown("""
    <div style="margin: 20px 0 10px 0; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 16px; font-weight: 800; color: #191F28;">카테고리별 지출</span>
        <span style="font-size: 13px; color: #FF5252; font-weight: 700;">전체 보기</span>
    </div>
    <div class="cat-grid">
    """, unsafe_allow_html=True)
    
    if not cat_expenses:
        st.markdown('<div style="color: #8B95A1; font-size: 13px; padding: 10px;">지출 내역이 없습니다.</div>', unsafe_allow_html=True)
    else:
        for cat in cat_expenses:
            st.markdown(f"""
            <div class="cat-box">
                <div class="cat-name">[{cat['category']}]</div>
                <div class="cat-amt">{cat['total']:,}원</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 실제 DB 최근 내역 (최대 5건)
    recent_txs = db.get_all_transactions(limit=5)
    st.markdown("""
    <div style="margin: 24px 0 10px 0; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 16px; font-weight: 800; color: #191F28;">최근 내역</span>
    </div>
    <div class="card">
    """, unsafe_allow_html=True)
    
    if not recent_txs:
        st.markdown('<div style="color: #8B95A1; font-size: 14px; padding: 10px 0;">거래 내역이 없습니다.</div>', unsafe_allow_html=True)
    else:
        for tx in recent_txs:
            amt_str = f"+{tx['amount']:,}원" if tx['tx_type'] == '수입' else f"-{tx['amount']:,}원"
            color_cls = "tx-plus" if tx['tx_type'] == '수입' else "tx-minus"
            date_short = tx['tx_date'][5:].replace('-', '/')
            st.markdown(f"""
            <div class="tx-row">
                <div>
                    <div class="tx-title">{tx['name']}</div>
                    <div class="tx-sub">{tx['category']} | {tx['sub_category']} - {date_short}</div>
                </div>
                <div class="{color_cls}">{amt_str}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# [3. 내역 화면]
elif st.session_state['current_tab'] == '내역':
    all_txs = db.get_all_transactions()
    st.markdown('<div class="card"><div style="font-size: 16px; font-weight: 800; margin-bottom: 12px;">전체 거래 내역</div>', unsafe_allow_html=True)
    if not all_txs:
        st.markdown('<div style="color: #8B95A1; font-size: 14px; padding: 10px 0;">기록된 거래 내역이 없습니다.</div>', unsafe_allow_html=True)
    else:
        for tx in all_txs:
            amt_str = f"+{tx['amount']:,}원" if tx['tx_type'] == '수입' else f"-{tx['amount']:,}원"
            color_cls = "tx-plus" if tx['tx_type'] == '수입' else "tx-minus"
            date_short = tx['tx_date'][5:].replace('-', '/')
            st.markdown(f"""
            <div class="tx-row">
                <div>
                    <div class="tx-title">{tx['name']}</div>
                    <div class="tx-sub">{tx['category']} | {tx['sub_category']} - {date_short}</div>
                </div>
                <div class="{color_cls}">{amt_str}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# [4. 통계 화면]
elif st.session_state['current_tab'] == '통계':
    summary = db.get_month_summary(curr_year, curr_month)
    cat_expenses = db.get_category_expenses(curr_year, curr_month)
    trend = db.get_monthly_trend(curr_year)
    
    # 월별 지출 바 차트 (최근 3개월: 5월, 6월, 7월 기준 시각화)
    max_val = max([trend[m]["지출"] for m in ["05", "06", "07"]] + [1])
    h_05 = int((trend["05"]["지출"] / max_val) * 120)
    h_06 = int((trend["06"]["지출"] / max_val) * 120)
    h_07 = int((trend["07"]["지출"] / max_val) * 120)
    
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 16px; font-weight: 800; margin-bottom: 16px;">월별 지출 추이 ({curr_year}년)</div>
        <div class="bar-container">
            <div class="bar-group"><div class="bar-fill" style="height: {max(h_05, 5)}px;"></div><div class="bar-label">5월</div></div>
            <div class="bar-group"><div class="bar-fill" style="height: {max(h_06, 5)}px;"></div><div class="bar-label">6월</div></div>
            <div class="bar-group"><div class="bar-fill" style="height: {max(h_07, 5)}px;"></div><div class="bar-label">7월</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 이번 달 지출 분석
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 16px; font-weight: 800; margin-bottom: 8px;">이번 달 지출 분석</div>
        <div style="font-size: 13px; color: #8B95A1; margin-bottom: 16px;">총 {summary['지출']:,}원</div>
    """, unsafe_allow_html=True)
    
    if not cat_expenses or summary['지출'] == 0:
        st.markdown('<div style="color: #8B95A1; font-size: 14px;">지출 내역이 없습니다.</div>', unsafe_allow_html=True)
    else:
        for cat in cat_expenses:
            ratio = int((cat['total'] / summary['지출']) * 100)
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #F5EBE9;">
                <div style="font-size: 14px; font-weight: 700;">[{cat['category']}] {ratio}%</div>
                <div style="font-size: 14px; font-weight: 700; color: #FF5252;">{cat['total']:,}원</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 하단 네비게이션 여백
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

# --- [하단 고정 네비게이션 바] ---
col_nav1, col_nav2, col_nav3, col_nav4, col_fab = st.columns([1, 1, 1, 1, 1])

with col_nav1:
    if st.button("홈", use_container_width=True):
        st.session_state['current_tab'] = '홈'
        st.rerun()
with col_nav2:
    if st.button("캘린더", use_container_width=True):
        st.session_state['current_tab'] = '캘린더'
        st.rerun()
with col_nav3:
    if st.button("내역", use_container_width=True):
        st.session_state['current_tab'] = '내역'
        st.rerun()
with col_nav4:
    if st.button("통계", use_container_width=True):
        st.session_state['current_tab'] = '통계'
        st.rerun()
with col_fab:
    if st.button("+", type="primary", use_container_width=True):
        st.session_state['show_modal'] = not st.session_state['show_modal']
        st.rerun()
