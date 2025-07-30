import streamlit as st
import sqlite3
import pandas as pd
import datetime
import bcrypt

DB_NAME = "oil_flow.db"

@st.cache_resource
def get_db_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

def setup_database():
    """Initializes the database for the OilFlow Logistics App."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL, role TEXT NOT NULL)''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            description TEXT,
            density_tonne_per_m3 REAL NOT NULL)''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            supplier_name TEXT,
            quantity_tonnes REAL,
            purchase_price_per_tonne REAL,
            purchase_date TIMESTAMP,
            eta_date TIMESTAMP,
            status TEXT,
            FOREIGN KEY (product_id) REFERENCES products (id))''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER,
            product_id INTEGER,
            quantity_tonnes REAL,
            status TEXT, -- 'Raw', 'Refining', 'Refined'
            last_updated TIMESTAMP,
            FOREIGN KEY (purchase_id) REFERENCES purchases (id),
            FOREIGN KEY (product_id) REFERENCES products (id))''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS sales_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inventory_id INTEGER,
            vendor_name TEXT,
            quantity_tonnes REAL,
            sale_price_per_tonne REAL,
            order_date TIMESTAMP,
            status TEXT, -- 'Booked', 'Dispatched', 'Delivered'
            FOREIGN KEY (inventory_id) REFERENCES inventory (id))''')

    # Seed initial product data if empty
    c.execute("SELECT count(*) FROM products")
    if c.fetchone()[0] == 0:
        products_data = [
            ('Crude Degummed Soyabean Oil', 'Raw soyabean oil, requires refining.', 0.92),
            ('Crude Palm Oil', 'Raw palm oil from fruit bunches.', 0.90),
            ('Crude Degummed Palm Oil', 'Palm oil that has undergone degumming.', 0.91),
            ('Crude Sunflower Oil', 'Raw oil extracted from sunflower seeds.', 0.92)
        ]
        c.executemany("INSERT INTO products (name, description, density_tonne_per_m3) VALUES (?, ?, ?)", products_data)

    # Seed admin user if not exists
    c.execute("SELECT count(*) FROM users WHERE username = 'admin'")
    if c.fetchone()[0] == 0:
        admin_pass = "admin123"
        hashed_password = bcrypt.hashpw(admin_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", ('admin', hashed_password, 'admin'))

    conn.commit()

# --- DATA ACCESS FUNCTIONS ---

def get_all_products():
    conn = get_db_connection()
    return pd.read_sql_query("SELECT * FROM products", conn)

def log_new_purchase(product_id, supplier, quantity, price, eta):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO purchases (product_id, supplier_name, quantity_tonnes, purchase_price_per_tonne, purchase_date, eta_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (product_id, supplier, quantity, price, datetime.datetime.now(), eta, 'Ordered'))
    conn.commit()

def get_all_purchases():
    conn = get_db_connection()
    query = """
        SELECT p.id, pr.name as product_name, p.supplier_name, p.quantity_tonnes,
               p.purchase_price_per_tonne, p.purchase_date, p.eta_date, p.status
        FROM purchases p JOIN products pr ON p.product_id = pr.id
        ORDER BY p.purchase_date DESC
    """
    return pd.read_sql_query(query, conn)

# (You would continue to add functions for inventory and sales here)
# def get_inventory_summary(): ...
# def create_sale_order(): ...
