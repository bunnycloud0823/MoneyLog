import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import database as db
import utils

def render_home():
    st.markdown("### 요약 정보")
    
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
    month_balance = income_month - expense_month
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="toss-card">
            <div class="toss-title">이번 달 수입</div>
            <div class="toss-value toss-blue">{utils.format_currency(income_month)}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="toss-card">
            <div class="toss-title">현재 총 자산</div>
            <div class="toss-value">{utils.format_currency(total_assets)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="toss-card">
            <div class="toss-title">이번 달 지출</div>
            <div class="toss-value toss-red">{utils.format_currency(expense_month)}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="toss-card">
            <div class="toss-title">이번 달 잔액</div>
            <div class="toss-value">{utils.format_currency(month_balance)}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 예산 진행률")
    budgets_df = db.get_budgets(now_ym)
    if not budgets_df.empty and not df_month.empty:
        df_exp = df_month[df_month['type'] == '지출']
        for _, row in budgets_df.iterrows():
            cat = row['major_cat']
            limit = row['amount']
            used = df_exp[df_exp['major_cat'] == cat]['amount'].sum()
            rate = min(int((used / limit) * 100), 100) if limit > 0 else 0
            st.write(f"**{cat}** ({utils.format_currency(used)} / {utils.format_currency(limit)}) - {rate}%")
            st.progress(rate / 100.0)
    else:
        st.info("설정된 예산이나 지출 내역이 없습니다. [자산 및 설정] 탭에서 예산을 설정해보세요.")
        
    st.markdown("### 이번 달 소비 TOP 5")
    if not df_month.empty:
        df_exp = df_month[df_month['type'] == '지출']
        if not df_exp.empty:
            top5 = df_exp.groupby('merchant')['amount'].sum().reset_index().sort_values('amount', ascending=False).head(5)
            for idx, row in top5.iterrows():
                st.markdown(f"""
                <div class="toss-card" style="padding: 12px 20px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 600;">{row['merchant']}</span>
                        <span class="toss-red" style="font-weight: 700;">{utils.format_currency(row['amount'])}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("이번 달 지출 내역이 없습니다.")
    else:
        st.write("이번 달 지출 내역이 없습니다.")

    st.markdown("### 최근 거래")
    if not df_all.empty:
        recent = df_all.head(5)
        for _, row in recent.iterrows():
            color_class = "toss-blue" if row['type'] == '수입' else ("toss-red" if row['type'] == '지출' else "")
            st.markdown(f"""
            <div class="toss-card" style="padding: 12px 20px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-weight: 600;">{row['merchant'] if row['merchant'] else row['major_cat']}</span>
                    <span class="{color_class}" style="font-weight: 700;">{utils.format_currency(row['amount'])}</span>
                </div>
                <div style="font-size: 12px; color: #8b95a1;">
                    {row['date']} | {row['major_cat']} > {row['minor_cat']} | {row['pay_method']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("등록된 거래 내역이 없습니다.")

def render_transactions():
    st.markdown("### 거래 내역 관리")
    
    with st.expander("새 거래 추가", expanded=False):
        with st.form("add_trans_form", clear_on_submit=True):
            t_type = st.selectbox("거래 종류", ["지출", "수입", "이체"])
            t_date = st.date_input("날짜", date.today()).strftime("%Y-%m-%d")
            merchant = st.text_input("거래처 (예: 스타벅스, 입력 시 자동 분류)")
            
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
            asset_name = st.selectbox("자산", asset_list)
            
            install_months = st.number_input("할부 개월 수 (일시불은 1)", min_value=1, max_value=36, value=1)
            memo = st.text_input("메모")
            
            submit = st.form_submit_button("거래 등록")
            if submit:
                if amount > 0:
                    db.add_transaction(t_date, t_type, amount, merchant, major_cat, minor_cat, pay_method, asset_name, memo, install_months)
                    st.success("거래가 성공적으로 등록되었습니다.")
                    st.rerun()
                else:
                    st.error("금액을 1원 이상 입력해주세요.")

    st.markdown("### 내역 검색 및 조회")
    col1, col2 = st.columns([1, 2])
    with col1:
        filter_type = st.selectbox("분류 필터", ["전체", "지출", "수입", "이체"])
    with col2:
        search_kw = st.text_input("키워드 검색 (거래처, 메모, 카테고리)")
        
    df_trans = db.get_transactions(trans_type=filter_type, keyword=search_kw if search_kw else None)
    
    if not df_trans.empty:
        for _, row in df_trans.iterrows():
            color_class = "toss-blue" if row['type'] == '수입' else ("toss-red" if row['type'] == '지출' else "")
            st.markdown(f"""
            <div class="toss-card" style="padding: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <div>
                        <span style="font-weight: 700; font-size: 16px;">{row['merchant'] if row['merchant'] else row['major_cat']}</span>
                        <span style="font-size: 12px; color: #8b95a1; margin-left: 8px;">{row['type']}</span>
                    </div>
                    <span class="{color_class}" style="font-weight: 700; font-size: 16px;">{utils.format_currency(row['amount'])}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #4e5968;">
                    <span>{row['date']} | {row['major_cat']} > {row['minor_cat']}</span>
                    <span>{row['pay_method']} ({row['asset_name']})</span>
                </div>
                {f'<div style="font-size: 12px; color: #8b95a1; margin-top: 6px;">메모: {row["memo"]}</div>' if row['memo'] else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("삭제", key=f"del_{row['id']}"):
                db.delete_transaction(row['id'])
                st.rerun()
    else:
        st.write("조회된 거래 내역이 없습니다.")

def render_calendar():
    st.markdown("### 캘린더 보기")
    df_all = db.get_transactions()
    
    if df_all.empty:
        st.write("등록된 거래 내역이 없습니다.")
        return
        
    df_all['date'] = pd.to_datetime(df_all['date'])
    daily_summary = df_all.groupby(['date', 'type'])['amount'].sum().unstack(fill_value=0).reset_index()
    
    st.markdown("#### 일별 수입/지출 요약")
    for _, row in daily_summary.sort_values('date', ascending=False).iterrows():
        dt_str = row['date'].strftime("%Y-%m-%d")
        inc = row['수입'] if '수입' in row else 0
        exp = row['지출'] if '지출' in row else 0
        st.markdown(f"""
        <div class="toss-card" style="padding: 12px 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 700; font-size: 16px;">{dt_str}</span>
                <div>
                    <span class="toss-blue" style="margin-right: 12px; font-weight: 600;">+ {utils.format_currency(inc)}</span>
                    <span class="toss-red" style="font-weight: 600;">- {utils.format_currency(exp)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    selected_date = st.date_input("특정 날짜 거래 내역 보기", date.today()).strftime("%Y-%m-%d")
    df_day = df_all[df_all['date'].dt.strftime("%Y-%m-%d") == selected_date]
    
    st.markdown(f"#### {selected_date} 상세 내역")
    if not df_day.empty:
        for _, row in df_day.iterrows():
            st.write(f"- **[{row['type']}]** {row['merchant']} : {utils.format_currency(row['amount'])} ({row['major_cat']} > {row['minor_cat']})")
    else:
        st.write("해당 날짜의 거래 내역이 없습니다.")

def render_stats():
    st.markdown("### 통계 및 분석")
    df_all = db.get_transactions()
    
    if df_all.empty:
        st.write("분석할 거래 내역이 없습니다.")
        return
        
    df_all['month'] = df_all['date'].str.slice(0, 7)
    now_ym = datetime.now().strftime("%Y-%m")
    
    st.markdown("#### 이번 달 카테고리별 지출 비중")
    df_month_exp = df_all[(df_all['month'] == now_ym) & (df_all['type'] == '지출')]
    if not df_month_exp.empty:
        cat_sum = df_month_exp.groupby('major_cat')['amount'].sum().reset_index()
        fig_pie = px.pie(cat_sum, values='amount', names='major_cat', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.write("이번 달 지출 내역이 없습니다.")
        
    st.markdown("#### 월별 수입 및 지출 추이")
    monthly_sum = df_all.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0).reset_index()
    if not monthly_sum.empty:
        fig_bar = px.bar(monthly_sum, x='month', y=[col for col in ['수입', '지출'] if col in monthly_sum.columns], barmode='group', color_discrete_map={'수입': '#3182f6', '지출': '#f04452'})
        fig_bar.update_layout(margin=dict(t=10, b=0, l=0, r=0), xaxis_title="월", yaxis_title="금액(원)", legend_title="구분")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("#### 지난달 대비 소비 분석")
    months = sorted(df_all['month'].unique())
    if len(months) >= 2:
        last_m, curr_m = months[-2], months[-1]
        last_exp = df_all[(df_all['month'] == last_m) & (df_all['type'] == '지출')]['amount'].sum()
        curr_exp = df_all[(df_all['month'] == curr_m) & (df_all['type'] == '지출')]['amount'].sum()
        diff = curr_exp - last_exp
        status_text = f"{utils.format_currency(abs(diff))} 증가했습니다." if diff > 0 else f"{utils.format_currency(abs(diff))} 감소했습니다."
        st.info(f"지난달({last_m}) 대비 이번 달({curr_m}) 지출이 **{status_text}**")
    else:
        st.write("데이터가 2개월 이상 쌓이면 지난달과 비교할 수 있습니다.")

def render_settings():
    st.markdown("### 자산 및 환경 설정")
    
    st.markdown("#### 1. 자산 관리")
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
        new_a_name = st.text_input("새 자산 이름")
        new_a_type = st.selectbox("자산 종류", ["현금", "은행", "카드", "적금", "투자", "대출"])
        new_a_bal = st.number_input("초기 잔액", value=0, step=10000)
        if st.form_submit_button("자산 추가") and new_a_name:
            db.add_asset(new_a_name, new_a_type, new_a_bal)
            st.rerun()
            
    st.markdown("#### 2. 카테고리 관리")
    with st.form("add_cat_form", clear_on_submit=True):
        c_type = st.selectbox("구분", ["지출", "수입"])
        c_major = st.text_input("대분류")
        c_minor = st.text_input("소분류")
        if st.form_submit_button("카테고리 추가") and c_major and c_minor:
            db.add_category(c_type, c_major, c_minor)
            st.rerun()
            
    cats_df = db.get_categories()
    if not cats_df.empty:
        for _, row in cats_df.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"[{row['type']}] {row['major']} > {row['minor']}")
            with col2:
                if st.button("삭제", key=f"del_cat_{row['id']}"):
                    db.delete_category(row['id'])
                    st.rerun()
                    
    st.markdown("#### 3. 결제 수단 관리")
    with st.form("add_pay_form", clear_on_submit=True):
        p_name = st.text_input("결제 수단 이름")
        if st.form_submit_button("결제 수단 추가") and p_name:
            db.add_payment_method(p_name)
            st.rerun()
            
    pay_df = db.get_payment_methods()
    for _, row in pay_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(row['name'])
        with col2:
            if st.button("삭제", key=f"del_pay_{row['id']}"):
                db.delete_payment_method(row['id'])
                st.rerun()

    st.markdown("#### 4. 예산 설정")
    now_ym = datetime.now().strftime("%Y-%m")
    with st.form("add_budget_form", clear_on_submit=True):
        b_cat = st.selectbox("예산 설정할 대분류", db.get_categories('지출')['major'].unique())
        b_amount = st.number_input("이번 달 예산 금액(원)", min_value=0, step=10000)
        if st.form_submit_button("예산 저장") and b_cat:
            db.set_budget(now_ym, b_cat, b_amount)
            st.rerun()

    st.markdown("#### 5. 데이터 백업 및 엑셀 내보내기")
    df_all = db.get_transactions()
    if not df_all.empty:
        csv_data = df_all.to_csv(index=False).encode('utf-8-sig')
        st.download_button("CSV 파일로 내보내기", data=csv_data, file_name="moneybook_backup.csv", mime="text/csv")
        
        with open(db.DB_PATH, "rb") as f:
            st.download_button("SQLite DB 파일 백업", data=f, file_name="moneybook.db", mime="application/x-sqlite3")
