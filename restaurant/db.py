import os
import sqlite3

STATUSES = ('yeni', 'hazır', 'teslim')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'orders.db')


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_number TEXT,
                items TEXT,
                total_price INTEGER,
                status TEXT DEFAULT 'yeni'
            )
        """)
        columns = {row[1] for row in conn.execute('PRAGMA table_info(orders)')}
        if 'status' not in columns:
            conn.execute("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'yeni'")


def next_status(current):
    try:
        index = STATUSES.index(current)
    except ValueError:
        return STATUSES[0]
    return STATUSES[(index + 1) % len(STATUSES)]


def insert_order(table_number, items, total_price):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO orders (table_number, items, total_price, status)
            VALUES (?, ?, ?, ?)
            """,
            (table_number, items, total_price, 'yeni'),
        )


def list_orders():
    with connect() as conn:
        return conn.execute('SELECT * FROM orders ORDER BY id DESC').fetchall()


def advance_status(order_id):
    with connect() as conn:
        row = conn.execute('SELECT status FROM orders WHERE id = ?', (order_id,)).fetchone()
        if row is None:
            return False
        conn.execute(
            'UPDATE orders SET status = ? WHERE id = ?',
            (next_status(row['status']), order_id),
        )
    return True


def delete_order(order_id):
    with connect() as conn:
        deleted = conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        return deleted.rowcount > 0
