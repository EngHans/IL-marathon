# Use a base image with Python pre-installed
FROM python:3.10.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH"

# Update system and install necessary tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

# Set the working directory
WORKDIR /app

ENV DISPLAY=host.docker.internal:0.0

# Copy the project files (e.g., `pyproject.toml` and source code)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY /app /app

# Expose application port (if needed)
EXPOSE 8000
