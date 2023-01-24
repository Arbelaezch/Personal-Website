FROM python:3.10.9-slim

ARG SECRET_KEY
ARG SUPABASE_URL
ARG SUPABASE_KEY
ARG DB_HOST
ARG DB_NAME
ARG DB_USER
ARG DB_PORT
ARG DB_PASSWORD
ARG FB_BUCKET_URL
ARG FB_BUCKET_NAME

ENV SECRET_KEY=${SECRET_KEY}
ENV SUPABASE_URL=${SUPABASE_URL}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV DB_HOST=${DB_HOST}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PORT=${DB_PORT}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV FB_BUCKET_URL=${FB_BUCKET_URL}
ENV FB_BUCKET_NAME=${FB_BUCKET_NAME}

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./website /app

WORKDIR /app

ENV PORT 8080

CMD gunicorn --bind :$PORT --workers 3 website.wsgi:application