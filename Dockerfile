FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    curl \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Create a marker file to prove this Dockerfile is used
RUN echo "This container was built using the main Dockerfile" > /app/dockerfile-source.txt

# Expose API port
EXPOSE 8000

# Start FastAPI
CMD ["bash", "-c", "python app/db/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]