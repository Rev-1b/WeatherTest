FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /temp/requirements.txt

COPY . /backend
WORKDIR /backend
EXPOSE 8000

#RUN apt-get update
#RUN apt-get install postgresql-client build-base postgresql-dev

RUN pip install --no-cache -r /temp/requirements.txt
