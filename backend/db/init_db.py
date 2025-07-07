from .db import get_conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER,
            sentence TEXT,
            answer TEXT,
            user_answer TEXT,
            correct INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # Insert topics if empty
    cur.execute("SELECT COUNT(*) as c FROM topics;")
    if cur.fetchone()["c"] == 0:
        cur.executemany(
            "INSERT INTO topics (name) VALUES (?)",
            [("Science",), ("Technology",), ("History",)]
        )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
