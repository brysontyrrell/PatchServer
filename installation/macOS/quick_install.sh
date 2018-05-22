#!/usr/bin/env bash

#!/bin/bash

if [[ ! -e /Applications/Xcode.app ]]; then
    echo "Xcode.app is required to install Patch Server"
    exit 1
fi

if [[ -z $(which pip) ]]; then
    echo "'pip' not found, installing..."
    /usr/bin/easy_install pip
fi

if [[ -z $(pip freeze | grep virtualenv) ]]; then
    echo "'virtualenv' not found, installing..."
    pip install virtualenv
fi

APP_DIR=/Library/PatchServer

echo "Creating application directory at ${APP_DIR}"
mkdir ${APP_DIR}
virtualenv ${APP_DIR}/venv

echo "Installing required packages..."
cp ../../requirements.txt ${APP_DIR}
${APP_DIR}/venv/bin/pip install mod_wsgi -r ${APP_DIR}/requirements.txt

echo "Copying application files and setting permissions..."
cp -r  ../../patchserver ${APP_DIR}
cp ./patch_server.wsgi ${APP_DIR}

chmod 755 ${APP_DIR}/patch_server.wsgi
chown -R _www:_www ${APP_DIR}

echo "Creating Apache scripts in '/usr/local/bin/patchserver'..."
${APP_DIR}/venv/bin/mod_wsgi-express \
    setup-server ${APP_DIR}/patch_server.wsgi \
    --port=5000 \
    --user _www \
    --group _www \
    --server-root=/usr/local/bin/patchserver

echo "Copying LaunchDaemon..."
cp ./com.patchserver.daemon.plist /Library/LaunchDaemons/
chown root:wheel /Library/LaunchDaemons/com.patchserver.daemon.plist
chmod 644 /Library/LaunchDaemons/com.patchserver.daemon.plist

echo "Starting the Patch Server..."
/usr/local/bin/patchserver/apachectl start

echo "Quick install finished"
