#initialise the database and create tables if they don't exist

import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_CONN = os.getenv("DATABASE_URL")


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS youtube_videos (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    channel TEXT,
    published_at TIMESTAMPTZ,
    raw_json JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);
"""


def init_db(conn_str: str):
    if not conn_str:
        print("DATABASE_URL is not set. Set the DATABASE_URL environment variable and try again.")
        sys.exit(2)

    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
        cur.close()
        conn.close()
        print("Table 'youtube_videos' created or already exists.")
    except Exception as e:
        print("Error creating table:", e)
        sys.exit(1)


if __name__ == "__main__":
    init_db(DB_CONN)
