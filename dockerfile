FROM python:3.11.4

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

RUN apt-get update -qy

COPY . ./MorphView

RUN pip install gunicorn

RUN pip install -r ./MorphView/requirements.txt

WORKDIR MorphView/MorphViewBlog


