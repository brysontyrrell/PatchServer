FROM ubuntu:16.04

RUN /usr/bin/apt-get update -q && \
    /usr/bin/apt-get install -qqy python-pip gunicorn && \
    /usr/bin/apt-get clean && \
    /bin/rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY /requirements.txt /opt/ps/
COPY /patchserver /opt/ps/patchserver
COPY /installation/docker/wsgi.py /opt/ps/
COPY /installation/docker/config.py /opt/ps/

RUN pip install -r /opt/ps/requirements.txt && \
    pip install futures

ENV DATABASE_DIR=/var/lib/patchserver

WORKDIR /opt/ps

EXPOSE 5000

CMD ["/usr/bin/gunicorn", "--config", "/opt/ps/config.py", "wsgi"]
