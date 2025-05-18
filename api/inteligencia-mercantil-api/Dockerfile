FROM python:3.11.6-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy dependency files
COPY Pipfile* ./

# Install dependencies
RUN pipenv install --deploy --system

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Command to start with gunicorn, using Flask app factory style import
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.main:create_app()"]