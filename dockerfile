# Use slim Python base (this just makes a smaller image with only the essentials)
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system deps for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy all the python code in
COPY *.py /app/

# Add entrypoint script that will run DB init then start the web server
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose default web port
EXPOSE 5000

# Entrypoint runs DB init (idempotent) and then starts the Flask app
ENTRYPOINT ["/app/entrypoint.sh"]
