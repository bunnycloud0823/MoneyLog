import streamlit as st
import calendar
from datetime import datetime, date
from style import apply_mobile_app_style
import database as db

st.set_page_config(page_title="Moneylog", layout="centered", initial_sidebar_state="collapsed")
db.init_db()
apply_mobile_app_style()

# ---------------- 상태 초기화 ----------------
today = date.today()
defaults = {
    "current_tab": "캘린더",
    "cal_year": today.year,
    "cal_month": today.month,
    "selected_date": today,
    "show_modal": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

now = datetime.now()
curr_year, curr_month = now.year, now.month

# ---------------- 상단 고정 헤더 ----------------
now_str = now.strftime("%p %I:%M").replace("AM", "오전").replace("PM", "오후")
st.markdown(f"""
<div class="sticky-header">
    <span class="header-time">{now_str}</span>
    <span class="header-title">🧡 Moneylog · {st.session_state['current_tab']}</span>
</div>
""", unsafe_allow_html=True)


# ---------------- 내역 추가 모달 ----------------
def render_add_modal():
    st.markdown("""
    <div class="card" style="border:1.5px solid #FFD4CB;">
        <div style="font-size:17px; font-weight:900; color:#2B2320;">✏️ 새 내역 추가</div>
    </div>
    """, unsafe_allow_html=True)

    tx_type = st.radio("유형", ["지출", "수입"], horizontal=True, label_visibility="collapsed")
    cat_options = db.EXPENSE_CATEGORIES if tx_type == "지출" else db.INCOME_CATEGORIES

    c1, c2 = st.columns(2)
    with c1:
        tx_cat = st.selectbox("카테고리", cat_options, format_func=lambda c: f"{db.CATEGORY_ICONS.get(c,'📦')} {c}")
    with c2:
        tx_date = st.date_input("날짜", st.session_state["selected_date"])

    tx_amt = st.number_input("금액 (원)", min_value=0, step=1000, value=10000)
    tx_sub = st.text_input("세부 항목", placeholder="예: 외식, 지하철")
    tx_memo = st.text_input("상세 내용", placeholder="예: 점심 식사, 스타벅스")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("취소", use_container_width=True):
            st.session_state["show_modal"] = False
            st.rerun()
    with col_m2:
        if st.button("저장하기 💾", type="primary", use_container_width=True):
            name = tx_memo.strip() or tx_sub.strip() or tx_cat
            db.add_transaction(name, tx_cat, tx_sub, tx_date.strftime("%Y-%m-%d"), int(tx_amt), tx_type)
            st.session_state["show_modal"] = False
            st.session_state["selected_date"] = tx_date
            st.toast("저장했어요! 🎉")
            st.rerun()
    st.write("")


if st.session_state["show_modal"]:
    render_add_modal()


def tx_row_html(tx, show_date=False):
    icon = db.CATEGORY_ICONS.get(tx["category"], "📦")
    amt_str = f"+{tx['amount']:,}원" if tx["tx_type"] == "수입" else f"-{tx['amount']:,}원"
    color_cls = "tx-plus" if tx["tx_type"] == "수입" else "tx-minus"
    date_part = f" · {tx['tx_date'][5:].replace('-', '/')}" if show_date else ""
    sub = tx["sub_category"] or tx["category"]
    return f"""
    <div class="tx-row">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:20px; background:#FFF3EF; width:40px; height:40px; border-radius:12px;
                        display:flex; align-items:center; justify-content:center;">{icon}</div>
            <div>
                <div class="tx-title">{tx['name']}</div>
                <div class="tx-sub">{tx['category']} · {sub}{date_part}</div>
            </div>
        </div>
        <div class="{color_cls}">{amt_str}</div>
    </div>
    """


# ================= 1. 캘린더 화면 =================
if st.session_state["current_tab"] == "캘린더":
    cy, cm = st.session_state["cal_year"], st.session_state["cal_month"]

    nav1, nav2, nav3 = st.columns([1, 3, 1])
    with nav1:
        if st.button("‹", use_container_width=True):
            cm -= 1
            if cm == 0:
                cm, cy = 12, cy - 1
            st.session_state["cal_year"], st.session_state["cal_month"] = cy, cm
            st.rerun()
    with nav2:
        st.markdown(f"<div style='text-align:center; font-size:18px; font-weight:900; padding-top:6px;'>{cy}년 {cm}월</div>", unsafe_allow_html=True)
    with nav3:
        if st.button("›", use_container_width=True):
            cm += 1
            if cm == 13:
                cm, cy = 1, cy + 1
            st.session_state["cal_year"], st.session_state["cal_month"] = cy, cm
            st.rerun()

    month_txs = db.get_transactions_by_month(cy, cm)
    day_summary = {}
    for tx in month_txs:
        d = int(tx["tx_date"].split("-")[2])
        day_summary.setdefault(d, {"수입": 0, "지출": 0})
        day_summary[d][tx["tx_type"]] += tx["amount"]

    days_kr = ["일", "월", "화", "수", "목", "금", "토"]
    header_cols = st.columns(7)
    for i, d in enumerate(days_kr):
        cls = "sun" if i == 0 else ("sat" if i == 6 else "weekday")
        header_cols[i].markdown(f"<div style='text-align:center; font-size:12px; font-weight:800;' class='{cls}'>{d}</div>", unsafe_allow_html=True)

    cal_matrix = calendar.monthcalendar(cy, cm)
    for week in cal_matrix:
        cols = st.columns(7)
        for i, day_num in enumerate(week):
            with cols[i]:
                if day_num == 0:
                    st.markdown("<div style='height:70px;'></div>", unsafe_allow_html=True)
                    continue
                this_date = date(cy, cm, day_num)
                is_selected = st.session_state["selected_date"] == this_date
                btn_type = "primary" if is_selected else "secondary"
                if st.button(str(day_num), key=f"day_{cy}_{cm}_{day_num}", type=btn_type):
                    st.session_state["selected_date"] = this_date
                    st.rerun()
                info = day_summary.get(day_num, {"수입": 0, "지출": 0})
                pills = ""
                if info["수입"] > 0:
                    pills += f"<div class='cal-pill income'>+{info['수입']//1000}k</div>"
                if info["지출"] > 0:
                    pills += f"<div class='cal-pill expense'>-{info['지출']//1000}k</div>"
                dot = "today-dot" if this_date == today else ""
                st.markdown(f"<div class='cal-day-summary {dot}'>{pills}</div>", unsafe_allow_html=True)

    sel = st.session_state["selected_date"]
    target_date_str = sel.strftime("%Y-%m-%d")
    daily_txs = db.get_transactions_by_date(target_date_str)

    st.markdown(f"""<div class="card"><div style="font-size:15px; font-weight:800; margin-bottom:8px;">
        📅 {sel.month}월 {sel.day}일 내역</div>""", unsafe_allow_html=True)
    if not daily_txs:
        st.markdown('<div class="empty-state">🍃 등록된 내역이 없어요</div>', unsafe_allow_html=True)
    else:
        for tx in daily_txs:
            st.markdown(tx_row_html(tx), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= 2. 홈 화면 =================
elif st.session_state["current_tab"] == "홈":
    summary = db.get_month_summary(curr_year, curr_month)
    bal_str = f"+{summary['잔액']:,}원" if summary["잔액"] >= 0 else f"{summary['잔액']:,}원"
    total_assets = db.get_total_assets()

    st.markdown(f"""
    <div class="card" style="display:flex; justify-content:space-between; align-items:center; padding:16px 20px;">
        <div style="font-size:13.5px; font-weight:700; color:#A79E95;">🐷 총 자산</div>
        <div style="font-size:17px; font-weight:900; color:#2B2320;">{total_assets:,}원</div>
    </div>
    <div class="gradient-card">
        <div class="gradient-title">{curr_month}월 잔액</div>
        <div class="gradient-balance">{bal_str}</div>
        <div class="gradient-sub-row">
            <div class="gradient-sub-item">
                <div class="gradient-sub-label">💰 수입</div>
                <div class="gradient-sub-val">+{summary['수입']:,}원</div>
            </div>
            <div class="gradient-sub-item">
                <div class="gradient-sub-label">💸 지출</div>
                <div class="gradient-sub-val">-{summary['지출']:,}원</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ 지출 추가", use_container_width=True):
            st.session_state["show_modal"] = True
            st.rerun()
    with col_btn2:
        if st.button("➕ 수입 추가", use_container_width=True):
            st.session_state["show_modal"] = True
            st.rerun()

    cat_expenses = db.get_category_expenses(curr_year, curr_month)
    st.markdown("""
    <div style="margin:22px 0 10px 0; font-size:15.5px; font-weight:800; color:#2B2320;">🏷️ 카테고리별 지출</div>
    <div class="cat-grid">
    """, unsafe_allow_html=True)
    if not cat_expenses:
        st.markdown('<div class="empty-state">지출 내역이 없어요</div>', unsafe_allow_html=True)
    else:
        boxes = "".join(f"""
            <div class="cat-box">
                <div class="cat-icon">{db.CATEGORY_ICONS.get(cat['category'], '📦')}</div>
                <div class="cat-name">{cat['category']}</div>
                <div class="cat-amt">{cat['total']:,}원</div>
            </div>""" for cat in cat_expenses)
        st.markdown(boxes, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    ym = f"{curr_year:04d}-{curr_month:02d}"
    budgets = db.get_budgets(ym)
    st.markdown('<div style="margin:22px 0 10px 0; font-size:15.5px; font-weight:800; color:#2B2320;">🎯 예산 진행률</div>', unsafe_allow_html=True)
    if not budgets:
        st.markdown('<div class="card"><div class="empty-state">설정에서 이번 달 예산을 등록해보세요</div></div>', unsafe_allow_html=True)
    else:
        used_map = {c["category"]: c["total"] for c in cat_expenses}
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for b in budgets:
            used = used_map.get(b["category"], 0)
            rate = min(int((used / b["amount"]) * 100), 100) if b["amount"] > 0 else 0
            icon = db.CATEGORY_ICONS.get(b["category"], "📦")
            over = used > b["amount"]
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px; color:{'#FF5E62' if over else '#2B2320'};">
                    <span>{icon} {b['category']}</span>
                    <span>{used:,} / {b['amount']:,}원</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(rate / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    recent_txs = db.get_all_transactions(limit=5)
    st.markdown('<div style="margin:22px 0 10px 0; font-size:15.5px; font-weight:800; color:#2B2320;">🧾 최근 내역</div><div class="card">', unsafe_allow_html=True)
    if not recent_txs:
        st.markdown('<div class="empty-state">거래 내역이 없어요</div>', unsafe_allow_html=True)
    else:
        for tx in recent_txs:
            st.markdown(tx_row_html(tx, show_date=True), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= 3. 내역 화면 =================
elif st.session_state["current_tab"] == "내역":
    all_txs = db.get_all_transactions()
    st.markdown(f'<div class="card"><div style="font-size:16px; font-weight:800; margin-bottom:6px;">전체 거래 내역 ({len(all_txs)}건)</div>', unsafe_allow_html=True)
    if not all_txs:
        st.markdown('<div class="empty-state">기록된 거래 내역이 없어요</div>', unsafe_allow_html=True)
    else:
        for tx in all_txs:
            st.markdown(tx_row_html(tx, show_date=True), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if all_txs:
        with st.expander("🗑️ 내역 삭제하기"):
            options = {f"{t['tx_date']} · {t['name']} · {t['amount']:,}원": t["id"] for t in all_txs}
            pick = st.selectbox("삭제할 항목 선택", list(options.keys()))
            if st.button("선택 항목 삭제", type="primary", use_container_width=True):
                db.delete_transaction(options[pick])
                st.rerun()

# ================= 4. 통계 화면 =================
elif st.session_state["current_tab"] == "통계":
    summary = db.get_month_summary(curr_year, curr_month)
    cat_expenses = db.get_category_expenses(curr_year, curr_month)
    trend = db.get_monthly_trend(curr_year)

    months_to_show = [f"{m:02d}" for m in range(max(1, curr_month - 2), curr_month + 1)]
    max_val = max([trend[m]["지출"] for m in months_to_show] + [1])
    bars = "".join(f"""
        <div class="bar-group">
            <div class="bar-fill" style="height:{max(int((trend[m]['지출']/max_val)*120), 4)}px;"></div>
            <div class="bar-label">{int(m)}월</div>
        </div>""" for m in months_to_show)

    st.markdown(f"""
    <div class="card">
        <div style="font-size:16px; font-weight:800; margin-bottom:6px;">📈 월별 지출 추이 ({curr_year}년)</div>
        <div class="bar-container">{bars}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="font-size:16px; font-weight:800; margin-bottom:4px;">🧡 이번 달 지출 분석</div>
        <div style="font-size:12.5px; color:#A79E95; margin-bottom:14px;">총 {summary['지출']:,}원</div>
    """, unsafe_allow_html=True)
    if not cat_expenses or summary["지출"] == 0:
        st.markdown('<div class="empty-state">지출 내역이 없어요</div>', unsafe_allow_html=True)
    else:
        rows = ""
        for cat in cat_expenses:
            ratio = int((cat["total"] / summary["지출"]) * 100)
            icon = db.CATEGORY_ICONS.get(cat["category"], "📦")
            rows += f"""
            <div style="display:flex; align-items:center; justify-content:space-between; padding:10px 0; border-bottom:1px solid #F7F0EE;">
                <div style="font-size:13.5px; font-weight:700; color:#2B2320;">{icon} {cat['category']} · {ratio}%</div>
                <div style="font-size:13.5px; font-weight:800; color:#FF5E62;">{cat['total']:,}원</div>
            </div>"""
        st.markdown(rows, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= 5. 설정 화면 (자산 · 예산 · 백업) =================
elif st.session_state["current_tab"] == "설정":
    st.markdown('<div style="font-size:16px; font-weight:800; margin-bottom:10px;">🐷 자산 계좌</div>', unsafe_allow_html=True)
    assets = db.get_assets()
    if not assets:
        st.markdown('<div class="card"><div class="empty-state">등록된 자산이 없어요</div></div>', unsafe_allow_html=True)
    else:
        for a in assets:
            st.markdown(f"""
            <div class="card" style="padding:14px 18px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:14px; font-weight:800;">{db.ASSET_ICONS.get(a['asset_type'],'💼')} {a['name']}
                        <span style="font-size:11px; color:#A79E95; font-weight:600;">({a['asset_type']})</span></div>
                    <div style="font-size:14.5px; font-weight:900; color:#2B2320;">{a['balance']:,}원</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            ac1, ac2 = st.columns([3, 1])
            with ac1:
                new_bal = st.number_input("잔액 수정", value=int(a["balance"]), step=1000, key=f"bal_{a['id']}", label_visibility="collapsed")
                if new_bal != a["balance"]:
                    db.update_asset_balance(a["id"], new_bal)
                    st.rerun()
            with ac2:
                if st.button("삭제", key=f"del_asset_{a['id']}", use_container_width=True):
                    db.delete_asset(a["id"])
                    st.rerun()

    with st.expander("➕ 자산 계좌 추가"):
        a_name = st.text_input("계좌 이름", placeholder="예: 카카오뱅크")
        a_type = st.selectbox("종류", db.ASSET_TYPES, format_func=lambda t: f"{db.ASSET_ICONS.get(t,'💼')} {t}")
        a_bal = st.number_input("초기 잔액", value=0, step=10000)
        if st.button("계좌 추가하기", type="primary", use_container_width=True) and a_name.strip():
            db.add_asset(a_name.strip(), a_type, a_bal)
            st.rerun()

    st.markdown('<div style="font-size:16px; font-weight:800; margin:22px 0 10px 0;">🎯 이번 달 예산</div>', unsafe_allow_html=True)
    ym = f"{curr_year:04d}-{curr_month:02d}"
    budgets = db.get_budgets(ym)
    if budgets:
        for b in budgets:
            bc1, bc2 = st.columns([4, 1])
            with bc1:
                st.markdown(f"<div style='padding-top:8px; font-size:13.5px; font-weight:700;'>{db.CATEGORY_ICONS.get(b['category'],'📦')} {b['category']} · {b['amount']:,}원</div>", unsafe_allow_html=True)
            with bc2:
                if st.button("삭제", key=f"del_budget_{b['id']}", use_container_width=True):
                    db.delete_budget(b["id"])
                    st.rerun()

    with st.expander("➕ 예산 설정하기"):
        b_cat = st.selectbox("카테고리", db.EXPENSE_CATEGORIES, format_func=lambda c: f"{db.CATEGORY_ICONS.get(c,'📦')} {c}")
        b_amt = st.number_input("이번 달 예산 (원)", min_value=0, step=10000, value=100000)
        if st.button("예산 저장", type="primary", use_container_width=True):
            db.set_budget(ym, b_cat, b_amt)
            st.rerun()

    st.markdown('<div style="font-size:16px; font-weight:800; margin:22px 0 10px 0;">💾 데이터 백업</div>', unsafe_allow_html=True)
    all_txs = db.get_all_transactions()
    if all_txs:
        import csv, io
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(all_txs[0].keys()))
        writer.writeheader()
        writer.writerows(all_txs)
        st.download_button("📥 CSV로 내보내기", data=buf.getvalue().encode("utf-8-sig"),
                            file_name="moneylog_backup.csv", mime="text/csv", use_container_width=True)
    else:
        st.markdown('<div class="card"><div class="empty-state">내보낼 거래 내역이 없어요</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:44px;'></div>", unsafe_allow_html=True)

# ---------------- 하단 고정 네비게이션 ----------------
col_nav1, col_nav2, col_nav3, col_nav4, col_nav5, col_fab = st.columns(6)
nav_map = [
    (col_nav1, "🏠", "홈"),
    (col_nav2, "📅", "캘린더"),
    (col_nav3, "🧾", "내역"),
    (col_nav4, "📊", "통계"),
    (col_nav5, "⚙️", "설정"),
]
for col, icon, label in nav_map:
    with col:
        active = st.session_state["current_tab"] == label
        if st.button(f"{icon}\n{label}" if active else f"{icon} {label}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state["current_tab"] = label
            st.rerun()
with col_fab:
    if st.button("➕", type="primary", use_container_width=True):
        st.session_state["show_modal"] = not st.session_state["show_modal"]
        st.rerun()
