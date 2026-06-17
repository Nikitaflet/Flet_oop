import sqlite3
import os
import shutil
from datetime import datetime


def get_db_path():
    app_data = os.getenv("FLET_APP_STORAGE_DATA")
    if app_data:
        return os.path.join(app_data, "data.db")
    return "data.db"


def ensure_db_exists(db_path):
    if not os.path.exists(db_path):
        source = "data.db"
        if os.path.exists(source):
            shutil.copy(source, db_path)


def init_db(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        size TEXT,
        material TEXT,
        price REAL,
        sold REAL,
        made REAL,
        total REAL,
        materials_cost REAL,
        prod_cost REAL,
        time REAL,
        series TEXT,
        date TEXT,
        remainder REAL,
        remainder_rub REAL,
        markup REAL
    )
    """)
    cursor.connection.commit()


def connect_db(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    init_db(cursor)
    return conn, cursor


def to_float(v):
    try:
        return float(v)
    except:
        return 0


def get_year_from_date(date_str):
    if not date_str:
        return None
    parts = date_str.split('.')
    if len(parts) >= 3:
        try:
            return int(parts[2])
        except:
            return None
    return None


def calc_values(price, sold, made, mat_cost, time):
    p = to_float(price)
    s = to_float(sold)
    m = to_float(made)
    mat = to_float(mat_cost)
    t = to_float(time)

    work = t * 500
    cost = mat + work
    remainder = m - s
    profit = p - cost
    markup = (p / cost * 100) if cost != 0 else 0

    return cost, work, remainder, profit, markup
