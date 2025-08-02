# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt -i https://pypi.org/simple

# Copy the app code
COPY . .

# Expose the app port
EXPOSE 8080

# Start the Flask app
CMD ["python", "main.py"]
