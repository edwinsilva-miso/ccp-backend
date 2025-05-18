FROM python:3.11.6-slim

WORKDIR /app

# Install system dependencies first
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy dependency files
COPY Pipfile ./
FROM python:3.9-slim

WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile* ./

# Install dependencies
RUN pipenv install --deploy --system

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.main:create_app()"]
# Install dependencies
RUN pipenv install --deploy --ignore-pipfile --dev

# Copy application code
COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=src/main.py

# Expose port
EXPOSE 5000

# Run the application
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]