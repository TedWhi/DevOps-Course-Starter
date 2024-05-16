FROM python:3.11-buster
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /opt/todo_app
COPY poetry.toml pyproject.toml poetry.lock ./
RUN poetry install
COPY todo_app ./todo_app/
ENTRYPOINT poetry run flask run --host=0.0.0.0
