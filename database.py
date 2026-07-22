import sqlite3
import os
import shutil
import pandas as pd
from datetime import datetime

DB_PATH = "moneybook.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        type TEXT,
        balance INTEGER DEFAULT 0
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        major TEXT,
        minor TEXT,
        icon TEXT DEFAULT '🍔',
        UNIQUE(type, major, minor)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        type TEXT,
        amount INTEGER,
        merchant TEXT,
        major_cat TEXT,
        minor_cat TEXT,
        pay_method TEXT,
        asset_name TEXT,
        memo TEXT,
        installment_months INTEGER DEFAULT 1,
        installment_current INTEGER DEFAULT 1
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year_month TEXT,
        major_cat TEXT,
        amount INTEGER,
        UNIQUE(year_month, major_cat)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merchant_history (
        merchant TEXT PRIMARY KEY,
        type TEXT,
        major_cat TEXT,
        minor_cat TEXT,
        pay_method TEXT
    )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_cats = [
            ('지출', '식비', '외식', '🍔'), ('지출', '식비', '배달', '🥡'), ('지출', '식비', '카페', '☕'), ('지출', '식비', '장보기', '🛒'),
            ('지출', '교통', '대중교통', '🚌'), ('지출', '교통', '택시', '🚕'), ('지출', '교통', '주유', '⛽'),
            ('지출', '쇼핑', '의류', '🛍️'), ('지출', '쇼핑', '생필품', '🧻'), ('지출', '의료', '병원', '🏥'), ('지출', '의료', '약국', '💊'),
            ('지출', '여가', '영화/문화', '🎮'), ('지출', '여가', '여행', '✈️'), ('지출', '주거', '월세', '🏠'), ('지출', '주거', '공과금', '💡'),
            ('수입', '급여', '월급', '💰'), ('수입', '부수입', '이자/투자', '📈'), ('수입', '용돈', '기타수입', '🎁'),
            ('이체', '이체', '계좌이체', '🔄')
        ]
        cursor.executemany("INSERT OR IGNORE INTO categories (type, major, minor, icon) VALUES (?, ?, ?, ?)", default_cats)
        
    cursor.execute("SELECT COUNT(*) FROM payment_methods")
    if cursor.fetchone()[0] == 0:
        default_methods = [('현금',), ('체크카드',), ('신용카드',), ('토스',), ('카카오페이',)]
        cursor.executemany("INSERT OR IGNORE INTO payment_methods (name) VALUES (?)", default_methods)
        
    cursor.execute("SELECT COUNT(*) FROM assets")
    if cursor.fetchone()[0] == 0:
        default_assets = [('현금', '현금', 0), ('신한은행', '은행', 0), ('국민은행', '은행', 0), ('삼성카드', '카드', 0)]
        cursor.executemany("INSERT OR IGNORE INTO assets (name, type, balance) VALUES (?, ?, ?)", default_assets)
        
    conn.commit()
    conn.close()

def add_transaction(date, trans_type, amount, merchant, major, minor, pay_method, asset_name, memo, install_months=1):
    conn = get_connection()
    cursor = conn.cursor()
    
    if install_months > 1 and trans_type == '지출':
        monthly_amount = int(amount / install_months)
        base_date = datetime.strptime(date, "%Y-%m-%d")
        for i in range(install_months):
            m = (base_date.month + i - 1) % 12 + 1
            y = base_date.year + (base_date.month + i - 1) // 12
            target_date = f"{y:04d}-{m:02d}-{base_date.day:02d}"
            inst_memo = f"{memo} ({i+1}/{install_months}개월 할부)" if memo else f"{i+1}/{install_months}개월 할부"
            cursor.execute("""
                INSERT INTO transactions (date, type, amount, merchant, major_cat, minor_cat, pay_method, asset_name, memo, installment_months, installment_current)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (target_date, trans_type, monthly_amount, merchant, major, minor, pay_method, asset_name, inst_memo, install_months, i+1))
    else:
        cursor.execute("""
            INSERT INTO transactions (date, type, amount, merchant, major_cat, minor_cat, pay_method, asset_name, memo, installment_months, installment_current)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
        """, (date, trans_type, amount, merchant, major, minor, pay_method, asset_name, memo))
    
    if trans_type == '수입':
        cursor.execute("UPDATE assets SET balance = balance + ? WHERE name = ?", (amount, asset_name))
    elif trans_type == '지출' and install_months == 1:
        cursor.execute("UPDATE assets SET balance = balance - ? WHERE name = ?", (amount, asset_name))
    elif trans_type == '지출' and install_months > 1:
        cursor.execute("UPDATE assets SET balance = balance - ? WHERE name = ?", (int(amount / install_months), asset_name))
        
    if merchant and trans_type in ['수입', '지출']:
        cursor.execute("""
            INSERT OR REPLACE INTO merchant_history (merchant, type, major_cat, minor_cat, pay_method)
            VALUES (?, ?, ?, ?, ?)
        """, (merchant, trans_type, major, minor, pay_method))
        
    conn.commit()
    conn.close()

def delete_transaction(trans_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, amount, asset_name FROM transactions WHERE id = ?", (trans_id,))
    row = cursor.fetchone()
    if row:
        t_type, amount, asset_name = row
        if t_type == '수입':
            cursor.execute("UPDATE assets SET balance = balance - ? WHERE name = ?", (amount, asset_name))
        elif t_type == '지출':
            cursor.execute("UPDATE assets SET balance = balance + ? WHERE name = ?", (amount, asset_name))
        cursor.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
    conn.commit()
    conn.close()

def get_transactions(start_date=None, end_date=None, trans_type=None, keyword=None):
    conn = get_connection()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if trans_type and trans_type != "전체":
        query += " AND type = ?"
        params.append(trans_type)
    if keyword:
        query += " AND (merchant LIKE ? OR memo LIKE ? OR major_cat LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
    query += " ORDER BY date DESC, id DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_merchant_history(merchant):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, major_cat, minor_cat, pay_method FROM merchant_history WHERE merchant = ?", (merchant,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_assets():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM assets ORDER BY id", conn)
    conn.close()
    return df

def update_asset_balance(asset_id, new_balance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE assets SET balance = ? WHERE id = ?", (new_balance, asset_id))
    conn.commit()
    conn.close()

def add_asset(name, asset_type, balance=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO assets (name, type, balance) VALUES (?, ?, ?)", (name, asset_type, balance))
    conn.commit()
    conn.close()

def delete_asset(asset_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    conn.commit()
    conn.close()

def get_categories(trans_type=None):
    conn = get_connection()
    query = "SELECT * FROM categories"
    params = []
    if trans_type:
        query += " WHERE type = ?"
        params.append(trans_type)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_category_icon(major, minor=None):
    conn = get_connection()
    cursor = conn.cursor()
    if minor:
        cursor.execute("SELECT icon FROM categories WHERE major = ? AND minor = ?", (major, minor))
    else:
        cursor.execute("SELECT icon FROM categories WHERE major = ? LIMIT 1", (major,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] else "🏷️"

def add_category(trans_type, major, minor, icon="🍔"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO categories (type, major, minor, icon) VALUES (?, ?, ?, ?)", (trans_type, major, minor, icon))
    conn.commit()
    conn.close()

def delete_category(cat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
    conn.commit()
    conn.close()

def get_payment_methods():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM payment_methods ORDER BY id", conn)
    conn.close()
    return df

def add_payment_method(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO payment_methods (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def delete_payment_method(method_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payment_methods WHERE id = ?", (method_id,))
    conn.commit()
    conn.close()

def get_budgets(year_month):
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM budgets WHERE year_month = ?", conn, params=[year_month])
    conn.close()
    return df

def set_budget(year_month, major_cat, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (year_month, major_cat, amount)
        VALUES (?, ?, ?)
        ON CONFLICT(year_month, major_cat) DO UPDATE SET amount = excluded.amount
    """, (year_month, major_cat, amount))
    conn.commit()
    conn.close()

def backup_db(target_path):
    shutil.copyfile(DB_PATH, target_path)

def restore_db(source_path):
    shutil.copyfile(source_path, DB_PATH)
