FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install requirements and MCP
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "mcp[cli]>=0.1.0"

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8000"] 