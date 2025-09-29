import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DB_CONN = os.getenv("DATABASE_URL")
print(f"DATABASE_URL configured: {bool(DB_CONN)}")

if DB_CONN:
    try:
        print("Attempting database connection...")
        conn = psycopg2.connect(DB_CONN)
        cur = conn.cursor()
        
        # Check if table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'youtube_videos'
            );
        """)
        table_exists = cur.fetchone()[0]
        print(f"Table 'youtube_videos' exists: {table_exists}")
        
        if table_exists:
            # Count rows
            cur.execute("SELECT COUNT(*) FROM youtube_videos;")
            count = cur.fetchone()[0]
            print(f"Number of videos in database: {count}")
            
            # Show sample data if any
            if count > 0:
                cur.execute("SELECT video_id, title, channel, created_at FROM youtube_videos ORDER BY created_at DESC LIMIT 3;")
                rows = cur.fetchall()
                print("Sample videos:")
                for row in rows:
                    print(f"  - {row[1]} by {row[2]} (ID: {row[0]}, Created: {row[3]})")
            else:
                print("No videos found in database")
        else:
            print("Table does not exist - need to run init_db.py")
        
        cur.close()
        conn.close()
        print("Database connection successful!")
        
    except Exception as e:
        print(f"Database connection error: {e}")
else:
    print("DATABASE_URL not set in environment")