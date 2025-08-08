# Use Python 3.9 slim image for better compatibility with Whisper
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for audio processing and Whisper
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a directory for temporary files
RUN mkdir -p /tmp/audio

# Expose port 7860 (Hugging Face Spaces standard)
EXPOSE 7860

# Set environment variables for Hugging Face Spaces
ENV PYTHONUNBUFFERED=1
ENV WHISPER_MODEL=base
ENV WHISPER_DEVICE=cpu

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
