import os
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = None
if DATABASE_URL:
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print('Connected to PostgreSQL')
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    components JSONB,
                    documents JSONB,
                    user_prompt TEXT
                );
            ''')
            conn.commit()
    except Exception as e:
        print(f'PostgreSQL connection failed: {e}')
else:
    print('DATABASE_URL not set. PostgreSQL will not be used.')

def get_db_conn():
    return conn

def save_project_db(name, description, components=None, documents=None, user_prompt=None):
    if components is None:
        components = []
    if documents is None:
        documents = []
    connection = get_db_conn()
    try:
        with connection.cursor() as cur:
            cur.execute(
                "INSERT INTO projects (name, description, components, documents, user_prompt) VALUES (%s, %s, %s, %s, %s)",
                (name, description, Json(components), Json(documents), user_prompt)
            )
            connection.commit()
        return True
    except Exception as e:
        print(f"Error saving project to DB: {e}")
        return False
