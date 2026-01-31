FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose ports
EXPOSE 8000 3000

# Make shell scripts executable
RUN chmod +x /app/shell/start_services.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the startup script
CMD ["/app/shell/start.sh"]
