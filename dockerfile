# Use a base Python image
FROM python:3.8-slim

# Set environment variables to ensure non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (Tesseract and other libraries)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libjpeg-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Check the installation path of Tesseract
RUN which tesseract  # This should print the location of tesseract

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 8080

# Command to run the Flask app
CMD ["python", "app.py"]
