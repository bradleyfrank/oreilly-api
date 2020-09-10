FROM        tiangolo/uwsgi-nginx-flask:python3.8-alpine as base

LABEL       Name="Mock Up API Endpoint" \
            Author="Brad Frank" \
            Maintainer="bradfrank@fastmail.com" \
            Description="Brad's mock up O'Reilly API endpoint assignment."

RUN         apk update && apk --no-cache add postgresql-dev gcc python3-dev musl-dev

COPY        app/requirements.txt /app

RUN         python3 -m pip install --upgrade pip && \
            python3 -m pip install -r /app/requirements.txt && \
            rm -rf /root/.cache/pip

COPY        app/ /app/
