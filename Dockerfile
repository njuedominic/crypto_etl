# lightweight Python runtime image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed to build packages like psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to take advantage of Docker layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the default command to execute the pipeline orchestrator
CMD ["python", "main.py"]