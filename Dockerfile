FROM python:3.11-slim-buster

# Install dependencies for building native extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install -U poetry

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY poetry.lock pyproject.toml ./

# Install the project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the project code to the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=myproject.settings.production

# Expose port 8001 for the Django application
EXPOSE 8001

# Start the Django application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8001"]



#FROM python:3.11-slim-buster
#
## Update and upgrade the linux environment
#RUN apt-get -y update && apt-get install -y git
#
## Install gcc, which is required for python-levenshtein
#RUN apt-get install gcc -y
#
## Install psycopg2 dependencies for Linux.
#RUN apt-get install python3-dev libpq-dev -y
#
## Install pipenv.
## -U upgrades the specified package(s)
#RUN pip install -U poetry
#
#RUN ls -al
## Create and cd to the working directory
#WORKDIR /LifeLogger
#RUN ls -al
## Copy the source code in last to optimize rebuilding the image
#COPY .env .
#COPY ./lifelogger .
#
## Install project dependencies
#COPY pyproject.toml .
#
#RUN poetry install




#
## Use an official Python runtime as a parent image
#FROM python:3.11-slim-buster
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy the requirements file into the container
#COPY pyproject.toml. .
#
## Install any dependencies for the app
#RUN poetry install --no-cache-dir -r requirements.txt
#
## Copy the rest of the application code into the container
#COPY . .
#
## Set environment variables for the database
#COPY .env .
#ENV POSTGRES_USER postgres
#ENV POSTGRES_PASSWORD postgres
#ENV POSTGRES_DB lifelogger
#
## Install Postgres and set up the database
#RUN apt-get update && apt-get install -y postgresql-client && \
#    psql -c 'create database lifelogger;' && \
#    rm -rf /var/lib/apt/lists/*
#
## Expose the port on which the Django app will run
##EXPOSE 8000
#
## Start the Django app
##CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]