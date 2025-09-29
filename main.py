import os#for environment variables 
import psycopg2#for PostgreSQL connection
from googleapiclient.discovery import build#for YouTube API
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
HASHTAG = "HijackYSWS"
DB_CONN = os.getenv("DATABASE_URL")

youtube = build("youtube", "v3", developerKey=API_KEY)

def fetch_videos(query, max_results=10):
    request = youtube.search().list(
        part="id,snippet",
        q=f"#{query}",
        type="video",
        order="date",
        maxResults=max_results
    )
    response = request.execute()
    return response.get("items", [])

def save_to_db(videos):
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    for v in videos:
        video_id = v["id"]["videoId"]
        title = v["snippet"]["title"]
        published = v["snippet"]["publishedAt"]
        channel = v["snippet"]["channelTitle"]

        cur.execute("""
            INSERT INTO youtube_videos (video_id, title, channel, published_at, raw_json)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING;
        """, (video_id, title, channel, published, str(v)))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    videos = fetch_videos(HASHTAG, max_results=5)
    save_to_db(videos)
    print(f"Inserted {len(videos)} videos into DB.")
