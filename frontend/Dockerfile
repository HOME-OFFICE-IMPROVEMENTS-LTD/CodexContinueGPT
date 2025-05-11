FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit configuration
RUN mkdir -p /root/.streamlit
RUN echo '\
[theme]\n\
primaryColor="#4f46e5"\n\
backgroundColor="#ffffff"\n\
secondaryBackgroundColor="#f8f9fa"\n\
textColor="#111827"\n\
font="sans serif"\n\
[server]\n\
enableCORS=true\n\
enableXsrfProtection=true\n\
' > /root/.streamlit/config.toml

# Copy application
COPY . .

# Make run script executable
RUN chmod +x /app/run_fixed_app.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Set the command
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]
