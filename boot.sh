#!/bin/bash
source venv/bin/activate
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app
# using gunicorn to serve this web app as docker image as flask
# doesn't provide a production server on it's own.