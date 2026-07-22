# pages.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import calendar
import database as db
import utils

def render_home():
    # ---------------- 1. 상단 잔액 & 이번달 요약 카드 ----------------
    now_ym = datetime.now().strftime("%Y-%m")
    df_all = db.get_transactions()
    
    if not df_all.empty:
        df_month = df_all[df_all['date'].str.startswith(now_ym)]
        income_month = df_month[df_month['type'] == '수입']['amount'].sum()
        expense_month = df_month[df_month['type'] == '지출']['amount'].sum()
    else:
        df_month = pd.DataFrame()
        income_month = 0
        expense_month = 0
        
    assets_df = db.get_assets()
    total_assets = assets_df['balance'].sum() if not assets_df.empty else 0
    
    col1, col2, col3 = st.columns([1.2, 1, 1])
    with col1:
        st.markdown(f"""
        <div class="toss-card card-balance">
            <div class="toss-title">총 잔액 및 자산</div>
            <div class="toss-value" style="color:white;">+{utils.format_currency(total_assets)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="toss-card card-income">
            <div class="toss-title">📈 수입</div>
            <div class="toss-value toss-blue">{utils.format_currency(income_month)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="toss-card card-expense">
            <div class="toss-title">📉 지출</div>
            <div class="toss-value toss-red">{utils.format_currency(expense_month)}</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- 2. 홈 화면 메인: 캘린더 & 날짜별 내역 ----------------
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = date.today()
        
    cal_col, detail_col = st.columns([1.5, 1])
    
    with cal_col:
        st.markdown("### 🗓️ 이달의 가계부 캘린더")
        
        # 년월 선택
        c1, c2 = st.columns([1, 1])
        with c1:
            cal_year = st.selectbox("연도", range(2024, 2031), index=st.session_state.selected_date.year - 2024, key="cal_y")
        with c2:
            cal_month = st.selectbox("월", range(1, 13), index=st.session_state.selected_date.month - 1, key="cal_m")
            
        target_ym = f"{cal_year:04d}-{cal_month:02d}"
        df_target = df_all[df_all['date'].str.startswith(target_ym)] if not df_all.empty else pd.DataFrame()
        
        # 일별 통계 맵 생성
        day_summary = {}
        if not df_target.empty:
            for _, row in df_target.iterrows():
                d_num = int(row['date'].split('-')[2])
                if d_num not in day_summary:
                    day_summary[d_num] = {'수입': 0, '지출': 0}
                if row['type'] in ['수입', '지출']:
                    day_summary[d_num][row['type']] += row['amount']

        # 요일 헤더
        days_kr = ["일", "월", "화", "수", "목", "금", "토"]
        cols = st.columns(7)
        for i, d in enumerate(days_kr):
            color = "#ff5c6a" if i == 0 else ("#3182f6" if i == 6 else "#555")
            cols[i].markdown(f"<div class='cal-header' style='color:{color};'>{d}</div>", unsafe_allow_html=True)
            
        # 달력 매트릭스 계산 (일요일 시작 기준)
        first_weekday, num_days = calendar.monthrange(cal_year, cal_month)
        first_weekday = (first_weekday + 1) % 7 # 일요일이 0이 되도록 조정
        
        current_day = 1
        for week in range(6):
            if current_day > num_days:
                break
            cols = st.columns(7)
            for dow in range(7):
                if (week == 0 and dow < first_weekday) or current_day > num_days:
                    cols[dow].markdown("<div style='height:75px;'></div>", unsafe_allow_html=True)
                else:
                    d_info = day_summary.get(current_day, {'수입': 0, '지출': 0})
                    inc_txt = f"<div style='color:#2bc194; font-size:11px; font-weight:700;'>+{d_info['수입']//1000}k</div>" if d_info['수입'] > 0 else ""
                    exp_txt = f"<div style='color:#ff5c6a; font-size:11px; font-weight:700;'>-{d_info['지출']//1000}k</div>" if d_info['지출'] > 0 else ""
                    
                    is_selected = (st.session_state.selected_date == date(cal_year, cal_month, current_day))
                    bg_style = "background-color: #fff0f1; border: 2px solid #ff5c6a; border-radius: 12px;" if is_selected else "background-color: #fff; border: 1px solid #f0ece6; border-radius: 12px;"
                    
                    with cols[dow]:
                        # 날짜 클릭용 버튼
                        if st.button(f"{current_day}", key=f"btn_day_{cal_year}_{cal_month}_{current_day}"):
                            st.session_state.selected_date = date(cal_year, cal_month, current_day)
                            st.rerun()
                        # 버튼 아래 수입/지출 텍스트
                        st.markdown(f"<div style='text-align:center; margin-top:-10px; margin-bottom:5px; min-height:28px;'>{inc_txt}{exp_txt}</div>", unsafe_allow_html=True)
                    current_day += 1

    with detail_col:
        sel_dt_str = st.session_state.selected_date.strftime("%Y-%m-%d")
        st.markdown(f"### 📍 {st.session_state.selected_date.month}월 {st.session_state.selected_date.day}일 내역")
        
        # 빠른 추가 버튼 (지출/수입)
        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("💸 지출 빠른 추가"):
                st.session_state.quick_add = "지출"
        with bc2:
            if st.button("💰 수입 빠른 추가"):
                st.session_state.quick_add = "수입"
                
        # 빠른 추가 팝업 형태의 폼
        if st.session_state.get("quick_add"):
            q_type = st.session_state.quick_add
            st.markdown(f"""<div style="background:#fff3f4; padding:15px; border-radius:15px; margin-bottom:15px; border:1px solid #ffd1d5;">
                        <b>✨ {sel_dt_str} {q_type} 기록하기</b></div>""", unsafe_allow_html=True)
            with st.form("quick_add_form", clear_on_submit=True):
                q_merchant = st.text_input("어디서 쓰셨나요? (거래처/내용)", placeholder="예: 스타벅스")
                q_amount = st.number_input("금액 (원)", min_value=0, step=1000)
                
                # 자동 카테고리 매칭
                auto_major, auto_minor, auto_pay = None, None, None
                if q_merchant:
                    hist = db.get_merchant_history(q_merchant)
                    if hist:
                        _, auto_major, auto_minor, auto_pay = hist
                
                cats_df = db.get_categories(q_type)
                majors = cats_df['major'].unique().tolist() if not cats_df.empty else ["기본"]
                m_idx = majors.index(auto_major) if auto_major in majors else 0
                q_major = st.selectbox("카테고리", majors, index=m_idx)
                
                minors = cats_df[cats_df['major'] == q_major]['minor'].tolist() if not cats_df.empty else ["기본"]
                mi_idx = minors.index(auto_minor) if auto_minor in minors else 0
                q_minor = st.selectbox("세부 항목", minors, index=mi_idx)
                
                pays_df = db.get_payment_methods()
                p_list = pays_df['name'].tolist() if not pays_df.empty else ["현금"]
                p_idx = p_list.index(auto_pay) if auto_pay in p_list else 0
                q_pay = st.selectbox("결제 수단", p_list, index=p_idx)
                
                assets_df = db.get_assets()
                a_list = assets_df['name'].tolist() if not assets_df.empty else ["현금"]
                q_asset = st.selectbox("자산 계좌", a_list)
                
                q_memo = st.text_input("간단 메모", placeholder="메모를 적어보세요")
                
                col_sub1, col_sub2 = st.columns([1, 1])
                with col_sub1:
                    if st.form_submit_button(" 💖 등록하기 "):
                        if q_amount > 0:
                            db.add_transaction(sel_dt_str, q_type, q_amount, q_merchant, q_major, q_minor, q_pay, q_asset, q_memo, 1)
                            st.session_state.quick_add = None
                            st.success("등록 완료!")
                            st.rerun()
                        else:
                            st.error("금액을 입력해주세요!")
                with col_sub2:
                    if st.form_submit_button("닫기"):
                        st.session_state.quick_add = None
                        st.rerun()

        # 선택한 날짜의 리스트 표시
        df_day = df_all[df_all['date'] == sel_dt_str] if not df_all.empty else pd.DataFrame()
        if not df_day.empty:
            for _, row in df_day.iterrows():
                icon = db.get_category_icon(row['major_cat'], row['minor_cat'])
                color_class = "toss-blue" if row['type'] == '수입' else ("toss-red" if row['type'] == '지출' else "")
                sign = "+" if row['type'] == '수입' else "-" if row['type'] == '지출' else ""
                
                st.markdown(f"""
                <div class="toss-card" style="padding: 15px 20px; margin-bottom: 10px; display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center;">
                        <div style="font-size:26px; margin-right:14px; background:#f7f4ee; padding:8px; border-radius:14px;">{icon}</div>
                        <div>
                            <div style="font-weight:800; font-size:16px; color:#222;">{row['merchant'] if row['merchant'] else row['major_cat']}</div>
                            <div style="font-size:12px; color:#999; margin-top:2px;">{row['major_cat']} · {row['minor_cat']} | {row['pay_method']}</div>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div class="{color_class}" style="font-weight:800; font-size:16px;">{sign}{utils.format_currency(row['amount'])}</div>
                        {f'<div style="font-size:11px; color:#aaa; margin-top:2px;">{row["memo"]}</div>' if row['memo'] else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🗑️ 삭제", key=f"del_home_{row['id']}"):
                    db.delete_transaction(row['id'])
                    st.rerun()
        else:
            st.markdown("""
            <div class="toss-card" style="text-align:center; padding: 40px 20px; color:#a09a93;">
                🌿<br><br>이 날은 기록된 내역이 없어요.<br>위 버튼을 눌러 내역을 추가해보세요!
            </div>
            """, unsafe_allow_html=True)

    # ---------------- 3. 홈 화면 하단: 예산 & TOP5 ----------------
    st.markdown("<hr style='border:none; height:1px; background-color:#eae5df; margin: 30px 0;'>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown("### 📊 이번 달 예산 진행률")
        budgets_df = db.get_budgets(now_ym)
        if not budgets_df.empty and not df_month.empty:
            df_exp = df_month[df_month['type'] == '지출']
            for _, row in budgets_df.iterrows():
                cat = row['major_cat']
                limit = row['amount']
                used = df_exp[df_exp['major_cat'] == cat]['amount'].sum()
                rate = min(int((used / limit) * 100), 100) if limit > 0 else 0
                icon = db.get_category_icon(cat)
                st.write(f"**{icon} {cat}** ({utils.format_currency(used)} / {utils.format_currency(limit)}) - {rate}%")
                st.progress(rate / 100.0)
        else:
            st.info("💡 설정된 예산이 없습니다. [자산 및 설정] 탭에서 이번 달 예산을 만들어보세요!")
            
    with b_col2:
        st.markdown("### 🔥 이번 달 소비 TOP 5")
        if not df_month.empty:
            df_exp = df_month[df_month['type'] == '지출']
            if not df_exp.empty:
                top5 = df_exp.groupby('merchant')['amount'].sum().reset_index().sort_values('amount', ascending=False).head(5)
                for idx, row in top5.iterrows():
                    st.markdown(f"""
                    <div class="toss-card" style="padding: 12px 18px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-weight: 700;">#{idx+1} {row['merchant']}</span>
                            <span class="toss-red" style="font-weight: 800;">{utils.format_currency(row['amount'])}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("이번 달 지출 내역이 없습니다.")
        else:
            st.write("이번 달 지출 내역이 없습니다.")


def render_transactions():
    st.markdown("### 📝 전체 거래 내역 관리")
    
    with st.expander("➕ 새 거래 상세 등록하기 (클릭하여 열기)", expanded=False):
        with st.form("add_trans_form", clear_on_submit=True):
            t_type = st.selectbox("거래 종류", ["지출", "수입", "이체"])
            t_date = st.date_input("날짜", date.today()).strftime("%Y-%m-%d")
            merchant = st.text_input("거래처 (예: 스타벅스, 입력 시 이전 카테고리 자동 선택)")
            
            auto_major, auto_minor, auto_pay = None, None, None
            if merchant:
                history = db.get_merchant_history(merchant)
                if history:
                    _, auto_major, auto_minor, auto_pay = history
            
            cats_df = db.get_categories(t_type)
            majors = cats_df['major'].unique().tolist() if not cats_df.empty else ["기본"]
            def_major_idx = majors.index(auto_major) if auto_major in majors else 0
            major_cat = st.selectbox("대분류", majors, index=def_major_idx)
            
            minors = cats_df[cats_df['major'] == major_cat]['minor'].tolist() if not cats_df.empty else ["기본"]
            def_minor_idx = minors.index(auto_minor) if auto_minor in minors else 0
            minor_cat = st.selectbox("소분류", minors, index=def_minor_idx)
            
            amount = st.number_input("금액 (원)", min_value=0, step=1000)
            
            pay_methods_df = db.get_payment_methods()
            pay_list = pay_methods_df['name'].tolist() if not pay_methods_df.empty else ["현금"]
            def_pay_idx = pay_list.index(auto_pay) if auto_pay in pay_list else 0
            pay_method = st.selectbox("결제 수단", pay_list, index=def_pay_idx)
            
            assets_df = db.get_assets()
            asset_list = assets_df['name'].tolist() if not assets_df.empty else ["현금"]
            asset_name = st.selectbox("자산 계좌", asset_list)
            
            install_months = st.number_input("할부 개월 수 (일시불은 1)", min_value=1, max_value=36, value=1)
            memo = st.text_input("메모")
            
            submit = st.form_submit_button("💖 등록 완료")
            if submit:
                if amount > 0:
                    db.add_transaction(t_date, t_type, amount, merchant, major_cat, minor_cat, pay_method, asset_name, memo, install_months)
                    st.success("거래가 성공적으로 등록되었습니다.")
                    st.rerun()
                else:
                    st.error("금액을 1원 이상 입력해주세요.")

    st.markdown("### 🔍 내역 검색 및 필터")
    col1, col2 = st.columns([1, 2])
    with col1:
        filter_type = st.selectbox("분류 필터", ["전체", "지출", "수입", "이체"])
    with col2:
        search_kw = st.text_input("키워드 검색 (거래처, 메모, 카테고리)")
        
    df_trans = db.get_transactions(trans_type=filter_type, keyword=search_kw if search_kw else None)
    
    if not df_trans.empty:
        for _, row in df_trans.iterrows():
            icon = db.get_category_icon(row['major_cat'], row['minor_cat'])
            color_class = "toss-blue" if row['type'] == '수입' else ("toss-red" if row['type'] == '지출' else "")
            sign = "+" if row['type'] == '수입' else "-" if row['type'] == '지출' else ""
            
            st.markdown(f"""
            <div class="toss-card" style="padding: 18px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px; align-items:center;">
                    <div style="display:flex; align-items:center;">
                        <span style="font-size:24px; margin-right:10px;">{icon}</span>
                        <div>
                            <span style="font-weight: 800; font-size: 16px;">{row['merchant'] if row['merchant'] else row['major_cat']}</span>
                            <span style="font-size: 12px; color: #a09a93; margin-left: 8px;">[{row['type']}]</span>
                        </div>
                    </div>
                    <span class="{color_class}" style="font-weight: 800; font-size: 18px;">{sign}{utils.format_currency(row['amount'])}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #666; margin-left:34px;">
                    <span>{row['date']} | {row['major_cat']} > {row['minor_cat']}</span>
                    <span>💳 {row['pay_method']} ({row['asset_name']})</span>
                </div>
                {f'<div style="font-size: 12px; color: #999; margin-top: 6px; margin-left:34px;">💬 {row["memo"]}</div>' if row['memo'] else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("삭제", key=f"del_trans_{row['id']}"):
                db.delete_transaction(row['id'])
                st.rerun()
    else:
        st.write("조회된 거래 내역이 없습니다.")


def render_stats():
    st.markdown("### 📊 통계 및 소비 분석")
    df_all = db.get_transactions()
    
    if df_all.empty:
        st.write("분석할 거래 내역이 없습니다.")
        return
        
    df_all['month'] = df_all['date'].str.slice(0, 7)
    now_ym = datetime.now().strftime("%Y-%m")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🍩 이번 달 카테고리별 지출")
        df_month_exp = df_all[(df_all['month'] == now_ym) & (df_all['type'] == '지출')]
        if not df_month_exp.empty:
            cat_sum = df_month_exp.groupby('major_cat')['amount'].sum().reset_index()
            fig_pie = px.pie(cat_sum, values='amount', names='major_cat', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.write("이번 달 지출 내역이 없습니다.")
            
    with col2:
        st.markdown("#### 📈 월별 수입/지출 추이")
        monthly_sum = df_all.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0).reset_index()
        if not monthly_sum.empty:
            fig_bar = px.bar(monthly_sum, x='month', y=[col for col in ['수입', '지출'] if col in monthly_sum.columns], barmode='group', color_discrete_map={'수입': '#2bc194', '지출': '#ff5c6a'})
            fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="", yaxis_title="")
            st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("#### 💡 지난달과 비교 분석")
    months = sorted(df_all['month'].unique())
    if len(months) >= 2:
        last_m, curr_m = months[-2], months[-1]
        last_exp = df_all[(df_all['month'] == last_m) & (df_all['type'] == '지출')]['amount'].sum()
        curr_exp = df_all[(df_all['month'] == curr_m) & (df_all['type'] == '지출')]['amount'].sum()
        diff = curr_exp - last_exp
        status_text = f"{utils.format_currency(abs(diff))} 더 썼어요! 💦" if diff > 0 else f"{utils.format_currency(abs(diff))} 아꼈어요! 최고! 👍"
        st.success(f"지난달({last_m})보다 이번 달({curr_m})에 **{status_text}**")
    else:
        st.info("🌱 데이터가 2개월 이상 쌓이면 지난달과 비교해 드려요!")


def render_settings():
    st.markdown("### ⚙️ 자산 및 환경 설정")
    
    st.markdown("#### 1. 💰 내 자산 계좌 관리")
    assets_df = db.get_assets()
    for _, row in assets_df.iterrows():
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{row['name']}** ({row['type']})")
        with col2:
            new_bal = st.number_input(f"{row['name']} 잔액", value=int(row['balance']), key=f"bal_{row['id']}")
            if new_bal != row['balance']:
                db.update_asset_balance(row['id'], new_bal)
                st.rerun()
        with col3:
            if st.button("삭제", key=f"del_asset_{row['id']}"):
                db.delete_asset(row['id'])
                st.rerun()
                
    with st.form("add_asset_form", clear_on_submit=True):
        new_a_name = st.text_input("새 자산 이름 (예: 카카오뱅크)")
        new_a_type = st.selectbox("자산 종류", ["현금", "은행", "카드", "적금", "투자", "대출"])
        new_a_bal = st.number_input("초기 잔액", value=0, step=10000)
        if st.form_submit_button("✨ 자산 추가하기") and new_a_name:
            db.add_asset(new_a_name, new_a_type, new_a_bal)
            st.rerun()
            
    st.markdown("#### 2. 🏷️ 카테고리 관리 (아이콘 포함)")
    with st.form("add_cat_form", clear_on_submit=True):
        c_col1, c_col2 = st.columns([1, 1])
        with c_col1:
            c_type = st.selectbox("구분", ["지출", "수입"])
            c_major = st.text_input("대분류 (예: 식비)")
        with c_col2:
            c_icon = st.text_input("아이콘 (이모지 1개)", value="🍕")
            c_minor = st.text_input("소분류 (예: 야식)")
        if st.form_submit_button("✨ 카테고리 추가") and c_major and c_minor:
            db.add_category(c_type, c_major, c_minor, c_icon)
            st.rerun()
            
    cats_df = db.get_categories()
    if not cats_df.empty:
        for _, row in cats_df.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{row.get('icon', '🏷️')} **[{row['type']}]** {row['major']} > {row['minor']}")
            with col2:
                if st.button("삭제", key=f"del_cat_{row['id']}"):
                    db.delete_category(row['id'])
                    st.rerun()
                    
    st.markdown("#### 3. 💳 결제 수단 관리")
    with st.form("add_pay_form", clear_on_submit=True):
        p_name = st.text_input("결제 수단 이름 (예: 네이버페이)")
        if st.form_submit_button("✨ 결제 수단 추가") and p_name:
            db.add_payment_method(p_name)
            st.rerun()
            
    pay_df = db.get_payment_methods()
    for _, row in pay_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"💳 {row['name']}")
        with col2:
            if st.button("삭제", key=f"del_pay_{row['id']}"):
                db.delete_payment_method(row['id'])
                st.rerun()

    st.markdown("#### 4. 🎯 이번 달 예산 설정")
    now_ym = datetime.now().strftime("%Y-%m")
    with st.form("add_budget_form", clear_on_submit=True):
        b_cat = st.selectbox("예산 설정할 대분류", db.get_categories('지출')['major'].unique())
        b_amount = st.number_input("이번 달 예산 금액(원)", min_value=0, step=10000)
        if st.form_submit_button("✨ 예산 저장하기") and b_cat:
            db.set_budget(now_ym, b_cat, b_amount)
            st.rerun()

    st.markdown("#### 5. 💾 데이터 백업 및 엑셀 내보내기")
    df_all = db.get_transactions()
    if not df_all.empty:
        csv_data = df_all.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 CSV 파일로 내보내기", data=csv_data, file_name="moneybook_backup.csv", mime="text/csv")
        
        with open(db.DB_PATH, "rb") as f:
            st.download_button("💾 SQLite DB 파일 백업", data=f, file_name="moneybook.db", mime="application/x-sqlite3")
