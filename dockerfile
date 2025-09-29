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
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY main.py .

# Run script the main script using python (obvs)
CMD ["python", "main.py"]
