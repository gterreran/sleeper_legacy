# pull official base image
FROM python:3.10.15-alpine3.20

# set work directory
RUN mkdir /fantasy
WORKDIR /fantasy

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk update && apk add gcc
RUN apk add --update make automake gcc g++ subversion python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /fantasy/

# copy entrypoint.sh
RUN sed -i 's/\r$//g' /fantasy/entrypoint.sh
RUN chmod +x /fantasy/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/fantasy/entrypoint.sh"]