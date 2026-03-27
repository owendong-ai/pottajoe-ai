import json
import os
import psycopg2

FILE_NAME = "preferences.json"

DEFAULT_PREFERENCES = {
    "濃郁": 0,
    "果香": 0,
    "堅果": 0,
    "花香": 0,
    "淺焙": 0,
    "中焙": 0,
    "深焙": 0
}

def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return None
    return psycopg2.connect(database_url)

def init_db():
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    flavor VARCHAR(50) PRIMARY KEY,
                    score INTEGER DEFAULT 0
                )
            """)
            for flavor, score in DEFAULT_PREFERENCES.items():
                cur.execute("""
                    INSERT INTO preferences (flavor, score)
                    VALUES (%s, %s)
                    ON CONFLICT (flavor) DO NOTHING
                """, (flavor, score))
        conn.commit()
    finally:
        conn.close()

def load_preferences():
    conn = get_db_connection()
    if conn:
        try:
            init_db()
            with conn.cursor() as cur:
                cur.execute("SELECT flavor, score FROM preferences")
                rows = cur.fetchall()
                return {row[0]: row[1] for row in rows} if rows else dict(DEFAULT_PREFERENCES)
        finally:
            conn.close()

    # 本機開發用 JSON 檔
    if not os.path.exists(FILE_NAME):
        return dict(DEFAULT_PREFERENCES)
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return dict(DEFAULT_PREFERENCES)

def save_preferences(preferences):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                for flavor, score in preferences.items():
                    cur.execute("""
                        INSERT INTO preferences (flavor, score)
                        VALUES (%s, %s)
                        ON CONFLICT (flavor) DO UPDATE SET score = EXCLUDED.score
                    """, (flavor, score))
            conn.commit()
        finally:
            conn.close()
        return

    # 本機開發用 JSON 檔
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(preferences, file, ensure_ascii=False, indent=4)
