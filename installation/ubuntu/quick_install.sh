#!/usr/bin/env bash

# Create application directory
/bin/mkdir /opt/ps

# Move required application files
/bin/mv ../../{requirements.txt,patchserver} /opt/patchserver
/bin/mv ./{config.py,wsgi.py} /opt/patchserver

/bin/chown -R www-data:www-data /opt/patchserver

/bin/mv ./patchserver.service /etc/systemd/system
/bin/chmod 755 /etc/systemd/system/patchserver.service


# Create application virtual environment
/usr/bin/virutalenv -p python2.7 /usr/local/patchserver-venv

# Install Python dependencies
/usr/local/patchserver-venv/bin/pip install futures gunicorn -r /opt/patchserver/requirements.txt

# Enable and start the service
/bin/systemctl enable gunicorn.service
/bin/systemctl start gunicorn.service

# Verify the service has started
/bin/systemctl status gunicorn.service
