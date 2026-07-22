import sqlite3
from contextlib import contextmanager

DB_NAME = "moneylog.db"

EXPENSE_CATEGORIES = ["식비", "교통", "쇼핑", "의료", "여가", "주거", "기타"]
INCOME_CATEGORIES = ["급여", "보너스", "용돈", "기타"]

CATEGORY_ICONS = {
    "식비": "🍔", "교통": "🚗", "쇼핑": "🛍️", "의료": "💊",
    "여가": "🎮", "주거": "🏠", "급여": "💰", "보너스": "🎁",
    "용돈": "💵", "기타": "📦",
}


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                sub_category TEXT,
                tx_date TEXT NOT NULL,
                amount INTEGER NOT NULL,
                tx_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_transaction(name, category, sub_category, tx_date, amount, tx_type):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO transactions (name, category, sub_category, tx_date, amount, tx_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, category, sub_category, tx_date, amount, tx_type))


def delete_transaction(tx_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))


def get_all_transactions(limit=None):
    with get_connection() as conn:
        query = "SELECT * FROM transactions ORDER BY tx_date DESC, id DESC"
        if limit:
            query += f" LIMIT {int(limit)}"
        rows = conn.execute(query).fetchall()
    return [dict(row) for row in rows]


def get_transactions_by_date(date_str):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM transactions WHERE tx_date = ? ORDER BY id DESC",
            (date_str,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_transactions_by_month(year, month):
    month_prefix = f"{year:04d}-{month:02d}%"
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM transactions WHERE tx_date LIKE ? ORDER BY tx_date ASC, id ASC",
            (month_prefix,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_month_summary(year, month):
    month_prefix = f"{year:04d}-{month:02d}%"
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT tx_type, SUM(amount) as total
            FROM transactions
            WHERE tx_date LIKE ?
            GROUP BY tx_type
        """, (month_prefix,)).fetchall()

    summary = {"수입": 0, "지출": 0, "잔액": 0}
    for row in rows:
        summary[row["tx_type"]] = row["total"] or 0
    summary["잔액"] = summary["수입"] - summary["지출"]
    return summary


def get_category_expenses(year, month):
    month_prefix = f"{year:04d}-{month:02d}%"
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE tx_date LIKE ? AND tx_type = '지출'
            GROUP BY category
            ORDER BY total DESC
        """, (month_prefix,)).fetchall()
    return [dict(row) for row in rows]


def get_monthly_trend(year):
    year_prefix = f"{year:04d}%"
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT substr(tx_date, 6, 2) as month, tx_type, SUM(amount) as total
            FROM transactions
            WHERE tx_date LIKE ?
            GROUP BY month, tx_type
        """, (year_prefix,)).fetchall()

    trend = {f"{i:02d}": {"수입": 0, "지출": 0} for i in range(1, 13)}
    for row in rows:
        m = row["month"]
        if m in trend:
            trend[m][row["tx_type"]] = row["total"] or 0
    return trend
