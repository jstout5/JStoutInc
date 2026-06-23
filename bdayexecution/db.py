import sqlite3
from contextlib import contextmanager
from pathlib import Path

import os
DB_PATH = Path(os.getenv("DB_PATH", str(Path(__file__).parent / "bday.db")))

def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                shipping_name TEXT NOT NULL,
                shipping_address TEXT NOT NULL,
                stripe_customer_id TEXT,
                active INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS recipients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL REFERENCES subscribers(id),
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                birthday TEXT NOT NULL,
                gift_budget TEXT NOT NULL,
                UNIQUE(subscriber_id, name, birthday)
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER NOT NULL REFERENCES recipients(id),
                year INTEGER NOT NULL,
                product_name TEXT,
                product_url TEXT,
                product_price REAL,
                walmart_order_id TEXT,
                status TEXT DEFAULT 'pending',
                approved INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                purchased_at TIMESTAMP,
                UNIQUE(recipient_id, year)
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_b64 TEXT,
                paypal_link TEXT,
                stripe_link TEXT,
                in_stock INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def add_subscriber(email, shipping_name, shipping_address):
    with get_conn() as conn:
        # check if subscriber already exists
        existing = conn.execute(
            "SELECT id FROM subscribers WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            return existing["id"]
        cur = conn.execute(
            "INSERT INTO subscribers (email, shipping_name, shipping_address) VALUES (?,?,?)",
            (email, shipping_name, shipping_address)
        )
        return cur.lastrowid

def add_recipient(subscriber_id, name, gender, birthday, gift_budget):
    """Returns (id, is_duplicate)."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM recipients WHERE subscriber_id=? AND name=? AND birthday=?",
            (subscriber_id, name.strip().title(), birthday)
        ).fetchone()
        if existing:
            return existing["id"], True
        cur = conn.execute(
            "INSERT INTO recipients (subscriber_id, name, gender, birthday, gift_budget) VALUES (?,?,?,?,?)",
            (subscriber_id, name.strip().title(), gender, birthday, gift_budget)
        )
        return cur.lastrowid, False

def activate_subscriber(email):
    with get_conn() as conn:
        conn.execute("UPDATE subscribers SET active=1 WHERE email=?", (email,))

def get_upcoming_birthdays(days_ahead=9):
    """Returns recipients whose birthday month/day matches today + days_ahead."""
    from datetime import date, timedelta
    target = date.today() + timedelta(days=days_ahead)
    month_day = f"{target.month:02d}-{target.day:02d}"
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT r.*, s.shipping_name, s.shipping_address, s.email as sub_email
            FROM recipients r
            JOIN subscribers s ON s.id = r.subscriber_id
            WHERE s.active = 1
              AND substr(r.birthday, 6, 5) = ?
              AND NOT EXISTS (
                SELECT 1 FROM orders o
                WHERE o.recipient_id = r.id AND o.year = ?
              )
        """, (month_day, target.year)).fetchall()
        return [dict(r) for r in rows]

def create_order(recipient_id, year, product_name, product_url, product_price):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT OR IGNORE INTO orders (recipient_id, year, product_name, product_url, product_price) VALUES (?,?,?,?,?)",
            (recipient_id, year, product_name, product_url, product_price)
        )
        return cur.lastrowid

def approve_order(order_id):
    with get_conn() as conn:
        conn.execute("UPDATE orders SET approved=1 WHERE id=?", (order_id,))

def mark_purchased(order_id, walmart_order_id):
    with get_conn() as conn:
        conn.execute(
            "UPDATE orders SET status='purchased', walmart_order_id=?, purchased_at=CURRENT_TIMESTAMP WHERE id=?",
            (walmart_order_id, order_id)
        )

def get_order(order_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT o.*, r.name, r.gender, r.gift_budget, s.shipping_name, s.shipping_address "
            "FROM orders o JOIN recipients r ON r.id=o.recipient_id "
            "JOIN subscribers s ON s.id=r.subscriber_id WHERE o.id=?",
            (order_id,)
        ).fetchone()
        return dict(row) if row else None

def get_products():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM products ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

def add_product(name, description, price, image_b64, paypal_link, stripe_link):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO products (name, description, price, image_b64, paypal_link, stripe_link) VALUES (?,?,?,?,?,?)",
            (name, description, price, image_b64, paypal_link, stripe_link)
        )
        return cur.lastrowid

def delete_product(product_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM products WHERE id=?", (product_id,))

def toggle_product_stock(product_id):
    with get_conn() as conn:
        conn.execute("UPDATE products SET in_stock = 1 - in_stock WHERE id=?", (product_id,))
