FROM python:3.11

ENV PYTHONUNBUFFERED True \
    POETRY_VIRTUALENVS_CREATE false

ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -  && poetry config virtualenvs.create false

COPY pyproject.toml ./

#RUN poetry install --without dev
RUN poetry install --no-root

COPY ./api ./api

CMD exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT} --workers 1
