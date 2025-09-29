import os
from flask import Flask, render_template_string
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_CONN = os.getenv("DATABASE_URL")

TEMPLATE = """
<!doctype html>
<html>
<h1>CONSUME</h1>
<h1>CONSUME</h1>
<h1>CONSUME</h1>

Everyone is pushing you to
<marquee>
consume
doomscroll
tune in
watch live
swipe
</marquee>

For the next 2 weeks, hijack your algorithem and flip the script...

- instead of consuming, build something yourself
- post YT shorts of your progress as you track your time working
- earn prizes once you ship your project

<a href="SLACK_CHANNEL">Join now</a>


<h3>The shop</h3>

TBD (this will be pre-authed card grants. not sure what the bounds of these should be)

<h3>What to build</h3>

Build whatever you want. Feeling uninspired? scroll through some of these ideas

- a vtuber!
- some tool to make your videos better
- slack bot to share your most recent videos
- a website that streams to YT for you with your own interface
- build a hackatime extension with the bounty program

Ask our humble content creator...
<div class="idea-generator"></div>

And check out what others are building:
<ul>
{% for v in videos %}
  <li><a href="https://www.youtube.com/watch?v={{ v.video_id }}">{{ v.title }} by {{ v.channel }}</a></li>
{% endfor %}
</html>
"""


def get_videos():
    if not DB_CONN:
        return []

    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    cur.execute("SELECT video_id, title, channel FROM youtube_videos ORDER BY created_at DESC LIMIT 100;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    videos = []
    for r in rows:
        videos.append({"video_id": r[0], "title": r[1], "channel": r[2]})
    return videos


@app.route("/")
def index():
    videos = get_videos()
    return render_template_string(TEMPLATE, videos=videos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
