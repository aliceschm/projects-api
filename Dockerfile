FROM python:3.12-slim

# Disable output buffering
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y git curl build-essential libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Make them executable
RUN chmod +x wait-for-it.sh entrypoint.sh

# Create non-root user
RUN groupadd -r appuser \
 && useradd -r -g appuser -d /app appuser \
 && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run the application (will be executed by entrypoint)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
