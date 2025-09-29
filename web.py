import os
from flask import Flask, render_template
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

DB_CONN = os.getenv("DATABASE_URL")


def get_videos():
    if not DB_CONN:
        return []
    try:
        conn = psycopg2.connect(DB_CONN)
        cur = conn.cursor()
        cur.execute("SELECT video_id, title, channel FROM youtube_videos ORDER BY created_at DESC LIMIT 100;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        return []

    return [
        {"video_id": r[0], "title": r[1], "channel": r[2]}
        for r in rows
    ]


@app.route("/")
def index():
    videos = get_videos()
    # Pass datetime so template can render generation timestamp
    return render_template("index.html", videos=videos, datetime=datetime)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
