FROM python:3.7-alpine
WORKDIR /usr/src/app
COPY webserver.py .
CMD [ "python", "webserver.py"]
