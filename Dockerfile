FROM python:3.7-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev gcc \
                            libffi-dev openssl-dev
RUN pip install --upgrade pip
COPY . /app
RUN pip install -r app/requirements.txt
EXPOSE 5000