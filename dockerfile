FROM python:3.11.4

RUN apt-get update -qy

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

COPY ./MorphViewBlog ./MorphView

RUN poetry install

WORKDIR /MorphView

ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "MorphViewBlog.wsgi"]

# ENTRYPOINT ["poetry", "run", "python3", "manage.py", "runserver"]
