FROM python:3.8-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev gcc \
                            libffi-dev openssl-dev
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV DATABASE_URL postgres://postgres:postgres@database:5432/piastrix_db
EXPOSE 5000