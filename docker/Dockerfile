FROM python:3.8-slim-buster

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get -y upgrade

COPY /Pipfile* /opt/ps/
COPY /patchserver /opt/ps/patchserver
COPY /docker/wsgi.py /opt/ps/
COPY /docker/config.py /opt/ps/

RUN pip install pipenv gunicorn && \
    cd /opt/ps && \
    pipenv install --deploy --system

ENV DATABASE_DIR=/var/lib/patchserver

WORKDIR /opt/ps

EXPOSE 5000

CMD ["gunicorn", "--config", "/opt/ps/config.py", "wsgi"]
