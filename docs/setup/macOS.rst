Installation on macOS
---------------------

The following instructions are for setting up the patch server application on a
macOS system using ``mod_wsgi-express``.

.. warning::

    These instructions do not cover securing your patch server with a TLS
    certificate for HTTPS connections.

.. note::

    You will need to have the ``pip`` and ``virtualenv`` commands installed to
    follow these instructions.

Create a new directory in your ``/Library`` named ``PatchServer``. Clone the
project repository to this directory.

Write the following into a new file called ``patch_server.wsgi``:

.. note::

    Grant execute permissions on this file (mode ``755``).
    This file can be found in the repository at ``installation/macOS/``

.. code-block:: python

    import sys
    sys.path.insert(0, '/Library/PatchServer/')

    from patchserver.factory import create_app

    application = create_app()

In the Terminal, create a virtual environment within this directory called
``venv`` and install the project requirements.

.. code-block:: bash

    $ cd /Library/PatchServer
    $ virtualenv ./venv
    $ source ./venv/bin/activate
    (venv) $ pip install -r ./requirements.txt

Now install ``mod_wsgi`` into the environment (this process may take several
minutes):

.. code-block:: bash

    (venv) $ pip install mod_wsgi

Change the ownership of the ``/Library/PatchServer`` directory to the ``_www``
user and group (the server will be run as this user and **must** have read/write
access to this directory):

.. code-block:: bash

    $ sudo chown -R _www:_www /Library/PatchServer

Now, in a new Terminal window in ``/Library/PatchServer``, create a command line
utility to run and manage the apache server with:

.. code-block:: bash

    $ sudo venv/bin/mod_wsgi-express setup-server patch_server.wsgi --port=5000 --user _www --group _www --server-root=/usr/local/bin/patchserver

You can now launch the application using the following command:

.. code-block:: bash

    $ sudo /usr/local/bin/patchserver/apachectl start

To launch the patch server automatically when the system boots, write the
following launch daemon to ``/Library/LaunchDaemons/com.patchserver.daemon.plist``.

.. note::

    This launch daemon should be owned by ``root:wheel`` with mode ``644``.
    This file can be found in the repository at ``installation/macOS/``

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.patchserver.daemon</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/local/bin/patchserver/apachectl</string>
                <string>start</string>
            </array>
            <key>RunAtLoad</key>
            <true/>
            <key>KeepAlive</key>
            <true/>
        </dict>
    </plist>

The following file tree shows the locations of all the **required** files and
resources copied or created during these steps::

    /
    ├── Library/
    │   ├── PatchServer/                         <-- Owned by _www:_www
    │   │   ├── venv/                            <-- Python virtual environment
    │   │   ├── patchserver/                     <-- Application dir from GitHub
    │   │   ├── patch_server.wsgi
    │   │   └── requirements.txt
    │   └── LaunchDaemons/
    │       └── com.patchserver.daemon.plist
    └── usr/
        └── local/
            └── bin/
                └── patchserver/                 <-- Apache server utilities


You will be able to access the application using ``localhost`` or your
computer's IP address at port ``5000``.
