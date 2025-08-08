# Use Python 3.9 slim image for better compatibility with Whisper
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for audio processing and Whisper
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set environment variables for Hugging Face Spaces and Whisper cache
ENV PYTHONUNBUFFERED=1
ENV WHISPER_MODEL=base
ENV WHISPER_DEVICE=cpu
ENV XDG_CACHE_HOME=/home/user/.cache

# Create cache directory with proper permissions
RUN mkdir -p /home/user/.cache

# Copy requirements first to leverage Docker cache
COPY --chown=user:user requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY --chown=user:user . .

# Create a directory for temporary files
RUN mkdir -p /tmp/audio

# Expose port 7860 (Hugging Face Spaces standard)
EXPOSE 7860

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
