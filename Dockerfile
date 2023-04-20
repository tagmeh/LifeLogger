FROM python:3.11-slim-buster

# Update and upgrade the linux environment
RUN apt-get -y update && apt-get install -y git

# Install gcc, which is required for python-levenshtein
RUN apt-get install gcc -y

# Install psycopg2 dependencies for Linux.
RUN apt-get install python3-dev libpq-dev -y

# Install pipenv.
# -U upgrades the specified package(s)
RUN pip install -U poetry

# Create and cd to the working directory
WORKDIR /LifeLogger

# Copy the source code in last to optimize rebuilding the image
COPY .env .
COPY ./lifelogger ./lifelogger

# Install project dependencies
COPY poetry.lock .
COPY pyproject.toml .
# --system installs to the parent system. Removed until the below is solved. Not transferring the lock file over to the
#  container breaks this flag.
# --deploy enforces that that pipfile is up to date, or fails. Removed until a way is discovered to have a windows
#  and linux pipfile at the same time. The lock file will always be wrong when install on the other platform.
RUN poetry install




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