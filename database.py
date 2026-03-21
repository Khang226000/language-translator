import sqlite3
import os
import hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.abspath(os.path.join(BASE_DIR, "translator.db"))

print("📌 DB PATH:", DB_NAME)

def connect():
    return sqlite3.connect(DB_NAME)


# tạo bảng
def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # ===== ROLES =====
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    # ===== USERS =====
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT,
        role_id INTEGER,
        login_from TEXT DEFAULT 'system',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(role_id) REFERENCES roles(id)
    )
    """)

    # ===== HISTORY =====
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        source_text TEXT,
        translated_text TEXT,
        from_lang TEXT,
        to_lang TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ===== SOCIAL LOGIN =====
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS social_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        provider TEXT,
        provider_id TEXT,
        UNIQUE(provider, provider_id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ===== INSERT DEFAULT ROLES =====
    cursor.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (1, 'admin')")
    cursor.execute("INSERT OR IGNORE INTO roles (id, name) VALUES (2, 'user')")

    conn.commit()
    conn.close()


# lưu lịch sử
def save_history(user_id, source, translated, from_lang, to_lang):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history (user_id, source_text, translated_text, from_lang, to_lang)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, source, translated, from_lang, to_lang))

    conn.commit()
    conn.close()


# đăng ký
def register_user(name, email, phone, password, login_from="system"):
    conn = connect()
    cursor = conn.cursor()

    try:
        hashed = hash_password(password)    

        cursor.execute("""
        INSERT INTO users (name, email, phone, password, role_id, login_from)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, phone, hashed, 2, login_from))  # role_id = 2 (user)

        conn.commit()
        return True

    except Exception as e:
        print("REGISTER ERROR:", e)
        return False

    finally:
        conn.close()

def add_login_from_column():
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN login_from TEXT DEFAULT 'system'")
        print("Đã thêm cột login_from")
    except Exception as e:
        print("Có thể cột đã tồn tại:", e)

    conn.commit()
    conn.close()
# đăng nhập
def login_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute("""
    SELECT id, name
    FROM users
    WHERE (email=? OR phone=? OR name=?)
    AND password=?
    AND login_from='system'
    """, (username, username, username, hashed))

    user = cursor.fetchone()
    conn.close()

    return user
def get_history(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT source_text, translated_text, from_lang, to_lang, created_at, id
        FROM history
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 10
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows
def delete_history_item(history_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history WHERE id = ?",
    (history_id,))

    conn.commit()
    conn.close()
def get_user_info(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.name, users.email, users.phone, roles.name, users.login_from
        FROM users
        LEFT JOIN roles ON users.role_id = roles.id
        WHERE users.id = ?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()

    return user


def debug_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    print("===== USERS =====")
    for r in rows:
        print(r)

    conn.close()
if __name__ == "__main__":
    create_tables()
    print("✅ Tables created")
def check_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables:", cursor.fetchall())

    conn.close()
def check_user_exists(name, email, phone):
    conn = connect()   
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users 
        WHERE name = ? OR email = ? OR phone = ?
    """, (name, email, phone))

    user = cursor.fetchone()
    conn.close()

    return user
def login_social(provider, provider_id, name, email):
    conn = connect()
    cursor = conn.cursor()

    # kiểm tra đã tồn tại chưa
    cursor.execute("""
    SELECT user_id FROM social_accounts
    WHERE provider=? AND provider_id=?
    """, (provider, provider_id))

    row = cursor.fetchone()

    if row:
        return row[0]

    # tạo user mới
    cursor.execute("""
    INSERT INTO users (name, email, role_id, login_from)
    VALUES (?, ?, ?, ?)
    """, (name, email, 2, provider))

    user_id = cursor.lastrowid

    # lưu social account
    cursor.execute("""
    INSERT INTO social_accounts (user_id, provider, provider_id)
    VALUES (?, ?, ?)
    """, (user_id, provider, provider_id))

    conn.commit()
    conn.close()

    return user_id
def count_translations(user_id=None):
    conn = connect()
    cursor = conn.cursor()

    if user_id:
        cursor.execute("SELECT COUNT(*) FROM history WHERE user_id=?", (user_id,))
    else:
        cursor.execute("SELECT COUNT(*) FROM history")

    result = cursor.fetchone()[0]
    conn.close()
    return result
def make_admin(email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET role_id = 1
    WHERE email = ?
    """, (email,))

    conn.commit()
    conn.close()

    print(f"✅ Đã cấp quyền admin cho {email}")
def get_user_role(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT roles.name
    FROM users
    LEFT JOIN roles ON users.role_id = roles.id
    WHERE users.id = ?
    """, (user_id,))

    role = cursor.fetchone()
    conn.close()

    return role[0] if role else "user"
def save_feedback(user_id, content):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    INSERT INTO feedback (user_id, content)
    VALUES (?, ?)
    """, (user_id, content))

    conn.commit()
    conn.close()

def save_rating(user_id, rating, comment):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        history_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    INSERT INTO ratings (user_id, rating, comment)
    VALUES (?, ?, ?)
    """, (user_id, rating, comment))

    conn.commit()
    conn.close()