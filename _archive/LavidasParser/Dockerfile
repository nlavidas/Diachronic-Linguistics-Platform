# Use stable Python 3.10 (compatible with TensorFlow)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first (Docker caching optimization)
COPY requirements.txt /app/

# Install dependencies separately
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app

# Expose the correct port
EXPOSE 8000

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "greek_parser:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
