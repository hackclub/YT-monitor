Database setup instructions

This project uses PostgreSQL. The scraper expects a table named `youtube_videos` with the columns:

- video_id (primary key)
- title
- channel
- published_at (timestamp with timezone)
- raw_json (jsonb)
- created_at (timestamp with timezone)

You can create the table manually or run the included script `init_db.py` which will create it if missing.

Local (docker-compose) quick setup

1. Start services:

    docker-compose up -d db

2. Run the init script inside a Python container that has the project and dependencies installed. One way:

    # build the image (if using the project's Dockerfile)
    docker-compose build scraper

    # run a one-off command in the scraper service with the same environment
    docker-compose run --rm --service-ports scraper python init_db.py

If you prefer to run locally, ensure `DATABASE_URL` points at your DB and run:

    # from project root
    python -m pip install -r requirements.txt
    python init_db.py

Coolify deployment hints

- Coolify provides hooks / release commands you can run after deployment. Add a release or post-deploy command to run the init script so the table exists before the app starts.
- Example Coolify post-deploy command (in Coolify UI):

    # ensure virtualenv is set up or use system python
    python -m pip install -r requirements.txt; python init_db.py

Or, if your deployed container already has the app and Python packages installed, simply run:

    python init_db.py

Notes

- `init_db.py` is idempotent (uses CREATE TABLE IF NOT EXISTS).
- If your `DATABASE_URL` uses the deprecated `postgres://` scheme, psycopg2 still accepts it, but some ORMs may warn. You can convert to `postgresql://` if desired.
