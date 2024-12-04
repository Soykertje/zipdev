FROM python:3.11.8

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Requirements are installed here to ensure they will be cached.
COPY /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY /requirements.extra.txt /requirements.extra.txt
RUN pip install -r /requirements.extra.txt

COPY /compose/dev/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY . /app

EXPOSE 8000

WORKDIR /app
