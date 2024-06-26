FROM python:3.11-slim-buster as base
RUN apt-get update && apt-get install curl -y
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /opt/todo_app
COPY poetry.toml pyproject.toml poetry.lock ./
RUN poetry install

FROM base as production
WORKDIR /opt/todo_app
ENV FLASK_DEBUG="false"
COPY todo_app ./todo_app/
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as development
WORKDIR /opt/todo_app
ENV FLASK_DEBUG="true"
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as test
WORKDIR /opt/todo_app
ENV PYTHONPATH="/opt/todo_app"
COPY todo_app ./todo_app/
COPY tests ./tests/
ENTRYPOINT poetry run pytest
