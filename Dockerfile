FROM        tiangolo/uwsgi-nginx-flask:python3.8

LABEL       Name="Mock Up API Endpoint" \
            Author="Brad Frank" \
            Maintainer="bradfrank@fastmail.com" \
            Description="Brad's mock up O'Reilly API endpoint assignment."

COPY        app/ /app/

RUN         python3 -m pip install --upgrade pip && \
            python3 -m pip install -r /app/requirements.txt
