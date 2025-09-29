import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("YOUTUBE_API_KEY")
HASHTAG = "programming"  # Using programming for testing since HijackYSWS has no content yet

print(f"API Key configured: {bool(API_KEY)}")
print(f"Testing hashtag: #{HASHTAG}")

if API_KEY:
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
        
        print("Fetching videos from YouTube API...")
        request = youtube.search().list(
            part="id,snippet",
            q=f"#{HASHTAG}",
            type="video",
            order="date",
            maxResults=5
        )
        response = request.execute()
        videos = response.get("items", [])
        
        print(f"Found {len(videos)} videos for #{HASHTAG}")
        
        if videos:
            print("Sample videos found:")
            for i, video in enumerate(videos[:3], 1):
                video_id = video["id"]["videoId"]
                title = video["snippet"]["title"]
                channel = video["snippet"]["channelTitle"]
                published = video["snippet"]["publishedAt"]
                
                print(f"{i}. {title}")
                print(f"   Channel: {channel}")
                print(f"   Published: {published}")
                print(f"   URL: https://www.youtube.com/watch?v={video_id}")
                print()
        else:
            print("No videos found for this hashtag")
            
    except Exception as e:
        print(f"YouTube API error: {e}")
else:
    print("YOUTUBE_API_KEY not set")