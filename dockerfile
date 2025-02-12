# Use a lightweight Python image
FROM python:3.9-slim  

# Set environment variables to prevent interactive prompts and enable unbuffered logs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install system dependencies (Tesseract OCR and required libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libjpeg-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    tesseract-ocr-eng \
    tesseract-ocr-tir \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Verify Tesseract installation
RUN tesseract --version

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (to leverage Docker caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8080

# Use ENTRYPOINT for flexibility in production
ENTRYPOINT ["python", "app.py"]
