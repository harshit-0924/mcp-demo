FROM python:3.13-rc-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python packages with verbose output
RUN pip install --no-cache-dir -r requirements.txt -v

# Copy the server code
COPY server.py .
COPY .env .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the server in stdio mode
CMD ["python", "server.py"] 