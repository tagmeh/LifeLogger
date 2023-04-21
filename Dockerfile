# Image
FROM python:3.11-slim-buster

# Install dependencies for building native extensions
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip

# Install Poetry
RUN pip install -U poetry
RUN python -m pip install gunicorn

# Set the working directory
RUN mkdir -p /app
WORKDIR /app

# Copy the project files to the container
COPY pyproject.toml .

# Copy the project code to the container
COPY /lifelogger .

# Set environment variables
COPY .env .

# Install the project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi