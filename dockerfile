FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -qy

COPY ./MorphViewBlog ./MorphView

RUN pip install gunicorn

COPY requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /MorphView
