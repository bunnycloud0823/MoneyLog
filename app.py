import streamlit as st
import calendar
from datetime import datetime
from style import apply_mobile_app_style

# 페이지 설정
st.set_page_config(page_title="Moneylog", layout="centered", initial_sidebar_state="collapsed")

# 스타일 적용
apply_mobile_app_style()

# --- [상태 관리 (State)] ---
# 필수 요구사항: 첫 화면은 '캘린더'로 시작
if 'current_tab' not in st.session_state:
    st.session_state['current_tab'] = '캘린더'
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.today().day
if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False

# 임시 초기 샘플 데이터 (DB 연동 전에 이미지와 동일한 화면을 보여주기 위함)
if 'tx_list' not in st.session_state:
    st.session_state['tx_list'] = [
        {"name": "스타벅스", "cat": "식비", "sub": "카페", "date": "07/22", "amt": -8500, "type": "지출"},
        {"name": "늦은 귀가 택시", "cat": "교통", "sub": "택시", "date": "07/22", "amt": -45000, "type": "지출"},
        {"name": "성과급 일부", "cat": "보너스", "sub": "성과급", "date": "07/21", "amt": 80000, "type": "수입"},
        {"name": "월세 이체", "cat": "주거", "sub": "월세", "date": "07/20", "amt": -600000, "type": "지출"}
    ]

# --- [상단 고정 헤더] ---
now_str = datetime.now().strftime("%p %I:%M").replace("AM", "오전").replace("PM", "오후")
st.markdown(f"""
<div class="sticky-header">
    <span class="header-time">{now_str}</span>
    <span class="header-title">가계부 [{st.session_state['current_tab']}]</span>
</div>
""", unsafe_allow_html=True)

# --- [모달: 내역 추가 창] ---
if st.session_state['show_modal']:
    st.markdown("""
    <div class="card" style="border: 2px solid #FF5252; background: #FFFDFD;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 18px; font-weight: 800; color: #191F28;">내역 추가</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        tx_type = st.radio("유형 선택", ["지출", "수입"], horizontal=True)
        tx_amt = st.number_input("금액 (원)", min_value=0, step=1000, value=10000)
        tx_cat = st.selectbox("카테고리", ["식비", "교통", "쇼핑", "의료", "여가", "주거", "급여", "기타"])
        tx_sub = st.text_input("세부 항목 (예: 외식, 배달, 택시)", "외식")
        tx_memo = st.text_input("상세 내역 (지출처)", "맛있는 점심")
        tx_date = st.date_input("날짜 선택", datetime.today())
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("취소", use_container_width=True):
                st.session_state['show_modal'] = False
                st.rerun()
        with col_m2:
            if st.button("기록 저장", type="primary", use_container_width=True):
                new_item = {
                    "name": tx_memo,
                    "cat": tx_cat,
                    "sub": tx_sub,
                    "date": tx_date.strftime("%m/%d"),
                    "amt": -tx_amt if tx_type == "지출" else tx_amt,
                    "type": tx_type
                }
                st.session_state['tx_list'].insert(0, new_item)
                st.session_state['show_modal'] = False
                st.rerun()
    st.write("---")

# --- [메인 화면 렌더링] ---

# 1. 캘린더 화면 (기본 첫 화면)
if st.session_state['current_tab'] == '캘린더':
    st.markdown("""
    <div class="card">
        <div style="font-size: 18px; font-weight: 800; color: #191F28; margin-bottom: 12px;">2026년 7월</div>
        <table class="calendar-table">
            <thead>
                <tr>
                    <th><span class="sun">일</span></th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th><span class="sat">토</span></th>
                </tr>
            </thead>
            <tbody>
    """, unsafe_allow_html=True)
    
    cal = calendar.monthcalendar(2026, 7)
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
    
    # 선택된 날짜 내역 요약
    st.markdown(f"""
    <div class="card">
        <div style="font-size: 15px; font-weight: 700; margin-bottom: 10px;">7월 {st.session_state['selected_date']}일 내역</div>
        <div class="tx-row">
            <div>
                <div class="tx-title">스타벅스</div>
                <div class="tx-sub">식비 | 카페</div>
            </div>
            <div class="tx-minus">-8,500원</div>
        </div>
        <div class="tx-row">
            <div>
                <div class="tx-title">늦은 귀가 택시</div>
                <div class="tx-sub">교통 | 택시</div>
            </div>
            <div class="tx-minus">-45,000원</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 2. 홈 화면 (대시보드)
elif st.session_state['current_tab'] == '홈':
    # 그라데이션 잔액 카드
    st.markdown("""
    <div class="gradient-card">
        <div class="gradient-title">이번 달 잔액</div>
        <div class="gradient-balance">+2,137,000원</div>
        <div class="gradient-sub-row">
            <div class="gradient-sub-item">
                <div class="gradient-sub-label">수입</div>
                <div class="gradient-sub-val">+353만</div>
            </div>
            <div class="gradient-sub-item">
                <div class="gradient-sub-label">지출</div>
                <div class="gradient-sub-val">-139만</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 지출/수입 추가 버튼 (모달 오픈)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("지출 추가", use_container_width=True):
            st.session_state['show_modal'] = True
            st.rerun()
    with col_btn2:
        if st.button("수입 추가", use_container_width=True):
            st.session_state['show_modal'] = True
            st.rerun()

    # 카테고리별 지출 요약
    st.markdown("""
    <div style="margin: 20px 0 10px 0; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 16px; font-weight: 800; color: #191F28;">카테고리별 지출</span>
        <span style="font-size: 13px; color: #FF5252; font-weight: 700;">전체 보기</span>
    </div>
    <div class="cat-grid">
        <div class="cat-box"><div class="cat-name">[주거]</div><div class="cat-amt">60만</div></div>
        <div class="cat-box"><div class="cat-name">[쇼핑]</div><div class="cat-amt">32만</div></div>
        <div class="cat-box"><div class="cat-name">[식비]</div><div class="cat-amt">21만</div></div>
        <div class="cat-box"><div class="cat-name">[의료]</div><div class="cat-amt">15만</div></div>
    </div>
    """, unsafe_allow_html=True)

    # 최근 내역 리스트
    st.markdown("""
    <div style="margin: 24px 0 10px 0; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 16px; font-weight: 800; color: #191F28;">최근 내역</span>
        <span style="font-size: 13px; color: #FF5252; font-weight: 700;">전체 보기</span>
    </div>
    <div class="card">
    """, unsafe_allow_html=True)
    
    for tx in st.session_state['tx_list'][:4]:
        amt_str = f"{tx['amt']:+,}원" if tx['type'] == '수입' else f"{tx['amt']:,}원"
        color_cls = "tx-plus" if tx['type'] == '수입' else "tx-minus"
        st.markdown(f"""
        <div class="tx-row">
            <div>
                <div class="tx-title">{tx['name']}</div>
                <div class="tx-sub">{tx['cat']} | {tx['sub']} - {tx['date']}</div>
            </div>
            <div class="{color_cls}">{amt_str}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3. 내역 화면
elif st.session_state['current_tab'] == '내역':
    st.markdown('<div class="card"><div style="font-size: 16px; font-weight: 800; margin-bottom: 12px;">전체 거래 내역</div>', unsafe_allow_html=True)
    for tx in st.session_state['tx_list']:
        amt_str = f"{tx['amt']:+,}원" if tx['type'] == '수입' else f"{tx['amt']:,}원"
        color_cls = "tx-plus" if tx['type'] == '수입' else "tx-minus"
        st.markdown(f"""
        <div class="tx-row">
            <div>
                <div class="tx-title">{tx['name']}</div>
                <div class="tx-sub">{tx['cat']} | {tx['sub']} - {tx['date']}</div>
            </div>
            <div class="{color_cls}">{amt_str}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. 통계 화면
elif st.session_state['current_tab'] == '통계':
    # 월별 추이 바 차트
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 800; margin-bottom: 16px;">월별 수입·지출 추이</div>
        <div class="bar-container">
            <div class="bar-group"><div class="bar-fill" style="height: 100px;"></div><div class="bar-label">5월</div></div>
            <div class="bar-group"><div class="bar-fill" style="height: 95px;"></div><div class="bar-label">6월</div></div>
            <div class="bar-group"><div class="bar-fill" style="height: 120px;"></div><div class="bar-label">7월</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 지출 분석 비율
    st.markdown("""
    <div class="card">
        <div style="font-size: 16px; font-weight: 800; margin-bottom: 8px;">이번 달 지출 분석</div>
        <div style="font-size: 13px; color: #8B95A1; margin-bottom: 16px;">총 1,393,000원</div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
            <div style="font-size: 14px; font-weight: 700;">[주거] 43%</div>
            <div style="font-size: 14px; font-weight: 700; color: #FF5252;">600,000원</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
            <div style="font-size: 14px; font-weight: 700;">[쇼핑] 23%</div>
            <div style="font-size: 14px; font-weight: 700; color: #FF5252;">320,000원</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
            <div style="font-size: 14px; font-weight: 700;">[식비] 15%</div>
            <div style="font-size: 14px; font-weight: 700; color: #FF5252;">210,000원</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 하단 고정 네비게이션 바와의 여백 확보
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

# --- [하단 고정 네비게이션 바 (Streamlit 네이티브 버튼 연동)] ---
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
    # 우측 하단 고정 FAB (+) 버튼 역할
    if st.button("+", type="primary", use_container_width=True):
        st.session_state['show_modal'] = not st.session_state['show_modal']
        st.rerun()
