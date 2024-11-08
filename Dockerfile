FROM python:3.8.19-alpine3.20

ENV PYTHONUNBUFFERED=1
ENV PORT 8080
RUN mkdir /fantasy
WORKDIR /fantasy
COPY . /fantasy/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Run app with gunicorn command
CMD gunicorn fantasy.wsgi:application --bind 0.0.0.0:"${PORT}"

# Open port 8080 on container
EXPOSE ${PORT}                          