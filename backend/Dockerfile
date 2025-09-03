FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create requirements.txt if it doesn't exist
RUN echo "fastapi==0.104.1" > requirements.txt && \
    echo "uvicorn[standard]==0.24.0" >> requirements.txt && \
    echo "requests==2.31.0" >> requirements.txt && \
    echo "python-dotenv==1.0.0" >> requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]