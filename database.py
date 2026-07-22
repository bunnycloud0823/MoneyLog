# database.py
import sqlite3
from datetime import datetime

DB_NAME = "moneylog.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
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
    conn.commit()
    conn.close()

def add_transaction(name, category, sub_category, tx_date, amount, tx_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (name, category, sub_category, tx_date, amount, tx_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, sub_category, tx_date, amount, tx_type))
    conn.commit()
    conn.close()

def get_all_transactions(limit=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM transactions ORDER BY tx_date DESC, id DESC"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_transactions_by_date(date_str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM transactions 
        WHERE tx_date = ? 
        ORDER BY id DESC
    """, (date_str,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_month_summary(year, month):
    conn = get_connection()
    cursor = conn.cursor()
    month_prefix = f"{year:04d}-{month:02d}%"
    
    cursor.execute("""
        SELECT tx_type, SUM(amount) as total 
        FROM transactions 
        WHERE tx_date LIKE ? 
        GROUP BY tx_type
    """, (month_prefix,))
    
    summary = {"수입": 0, "지출": 0, "잔액": 0}
    for row in cursor.fetchall():
        summary[row["tx_type"]] = row["total"] if row["total"] else 0
        
    summary["잔액"] = summary["수입"] - summary["지출"]
    conn.close()
    return summary

def get_category_expenses(year, month):
    conn = get_connection()
    cursor = conn.cursor()
    month_prefix = f"{year:04d}-{month:02d}%"
    
    cursor.execute("""
        SELECT category, SUM(amount) as total 
        FROM transactions 
        WHERE tx_date LIKE ? AND tx_type = '지출'
        GROUP BY category 
        ORDER BY total DESC
    """, (month_prefix,))
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_monthly_trend(year):
    conn = get_connection()
    cursor = conn.cursor()
    year_prefix = f"{year:04d}%"
    
    cursor.execute("""
        SELECT substr(tx_date, 6, 2) as month, tx_type, SUM(amount) as total
        FROM transactions
        WHERE tx_date LIKE ?
        GROUP BY month, tx_type
    """, (year_prefix,))
    
    trend = {}
    for i in range(1, 13):
        m_str = f"{i:02d}"
        trend[m_str] = {"수입": 0, "지출": 0}
        
    for row in cursor.fetchall():
        m = row["month"]
        if m in trend:
            trend[m][row["tx_type"]] = row["total"]
            
    conn.close()
    return trend
