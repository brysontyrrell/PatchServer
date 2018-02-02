Jamf Pro Community Patch Server
===============================

An implementation of an external patch source for Jamf Pro. The Patch Server
provides the endpoints for Jamf Pro to read and subscribe to your custom
software title definitions and a API for managing those definitions.

Read the full documentation on [Read the Docs](http://patchserver.readthedocs.io/en/latest/)!

Setup
-----

Create a Python virtual environment and install the project requirements to it.

.. code-block:: bash

    cd /path/to/PatchServer
    virtualenv ./venv
    source ./venv/bin/activate
    pip install -r ./requirements.txt

Run the application.

.. code-block:: bash

    python run.py


You will be able to access the application using ``localhost`` or your
computer's IP address.


User Interface
--------------

Go to ``http://localhost/`` in a browser to view all titles that are available
on the Patch Server.

Jamf Pro Endpoints
------------------

``http://localhost/jamf/v1/software``

Lists all available titles for Jamf Pro.

``http://localhost/jamf/v1/software/<Title>,<Title>``

Lists a subset of titles, separated by comma, for Jamf Pro.

``http://localhost/jamf/v1/patch/<Title>``

Returns the full definition of a title.

API Endpoints
-------------

``http://localhost/api/v1/title``

``POST``: Create a new title. You may optionally send a full patch definition
from another source to this endpoint.

    .. code-block:: json

        {
            "id": "",
            "name": "",
            "publisher": "",
            "appName": "",
            "bundleId": ""
        }

        - Or full definition -

        {
            "id": "",
            "name": "",
            "publisher": "",
            "appName": "",
            "bundleId": "",
            "requirements": [...],
            "patches": [...],
            "extensionAttributes": [...]
        }

``http://localhost/api/v1/title/<Title>``

``DELETE``: Delete a title.

``PUT``: Update a title. You cannot change the ``id`` of a title. Additional
objects included will be ignored with this operation.

    .. code-block:: json

        {
            "name": "",
            "publisher": "",
            "appName": "",
            "bundleId": ""
        }

``http://localhost/api/v1/title/<Title>/requirements``

``POST``: Add requirements to a title. These requirements must be within an
array under an ``items`` key.

    .. code-block:: json

        {
            "name": "",
            "operator": "",
            "value": "",
            "type": "",
            "and": ""
        }

``http://localhost/api/v1/title/<Title>/patches``

``GET``: Returns all patch versions of a title.

``POST``: Add patch versions to a title.

    .. code-block:: json

        {
            "version": "",
            "releaseDate": "",
            "standalone": true,
            "minimumOperatingSystem": "",
            "reboot": false,
            "capabilities": [...],
            "components": [...],
            "killApps": [...]
        }
