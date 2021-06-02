FROM python:3.9-alpine
MAINTAINER Pedro Rodriguez

ENV PYTHONUNBUFFED 1

# Install required packages
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Directory to store the App sourcecode
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create user to run the app
# This is for security reasons, so that the container does not run our app with root privilegies
RUN adduser -D docker_user
RUN chown docker_user:docker_user -R /app/
USER docker_user
