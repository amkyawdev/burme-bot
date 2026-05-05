FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir gradio requests

# Copy app files
COPY . .

# Expose port
EXPOSE 7860

# Set environment
ENV PYTHONUNBUFFERED=1

# Run the app (uses Inference API - no model download needed)
CMD ["python", "app_api.py"]