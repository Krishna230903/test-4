import bcrypt
import sqlite3
from database import get_db_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def register_user(username, password, role='manager'):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        hashed_pw = hash_password(password).decode('utf-8')
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Username already exists

def validate_login(username, password):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user and check_password(user['password_hash'].encode('utf-8'), password):
        return {'id': user['id'], 'username': user['username'], 'role': user['role']}
    return None
