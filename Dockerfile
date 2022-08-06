# [base] image
FROM python:3.8.13-slim as base

EXPOSE 8000
WORKDIR /backend

ENV PYTHONUNBUFFERED 1

# [production] image
FROM base as prod

# copy all files to container
COPY . /backend/
