FROM python:3.10-slim-buster
# Working directory inside Docker container
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_NO_INTERACTION=1

# Placeholder variables to run collectstatic
ENV DEPLOYMENT_ENVIRONMENT="DOCKER"
ENV SECRET_KEY="Placeholder"
ENV DEBUG="True"
ENV OPENAI_API_KEY="Placeholder"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y curl netcat \
    && apt-get clean

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root

# Our project code:
#copy everything in side aibou/ folder to /app
COPY flashmonster/ /app

# Expose the port the app runs in
EXPOSE $PORT

RUN python manage.py collectstatic --noinput

# Specify the command to run
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 flashmonster.wsgi:application
