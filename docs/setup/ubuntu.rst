Installation on Ubuntu Server (16.04)
-------------------------------------

The following instructions are for setting up the patch server application on an
Ubuntu 16.04 system using ``gunicorn`` and ``systemd``.

.. warning::

    These instructions do not cover securing your patch server with a TLS
    certificate for HTTPS connections.

Install ``git``, ``python``, and ``virtualenv`` on the system:

.. code-block:: bash

    sudo /usr/bin/apt-get update -q
    sudo /usr/bin/apt-get install -qqy git virtualenv python-minimal

Clone the project repository to a temporary directory. ``cd`` into the
``installation/ubuntu`` directory.

.. code-block:: bash

    /usr/bin/git clone https://github.com/brysontyrrell/PatchServer.git /tmp/patchserver
    cd /tmp/patchserver/installation/ubuntu

Run the ``quick_install.sh``.

.. code-block:: bash

    sudo bash quick_install.sh


Once the script has completed you should be able to access the application using
the IP address of the system at port ``5000``.

Contents of ``quick_install.sh``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../../installation/ubuntu/quick_install.sh
    :code: bash

Use Nginx as a Reverse Proxy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    Running the patch server behind Nginx will allow you to configure the web
    server for HTTPS.

    To configure TLS, refer to the Nginx documentation available
    `here <http://nginx.org/en/docs/http/configuring_https_servers.html>`_.

Install Nginx on the system:

.. code-block:: bash

    sudo /usr/bin/apt-get update -q
    sudo /usr/bin/apt-get install -qqy nginx

Remove the default Nginx site:

.. code-block:: bash

    sudo rm /etc/nginx/sites-enabled/default

Modify the `bind` value of ``/opt/patchserver/config.py`` to have ``gunicorn``
bind the application to localhost at port ``5000``:

.. code-block:: python

    bind = "127.0.0.1:5000"

Write the following to a new file called ``/etc/nginx/conf.d/patchserver.conf``:

.. note::

    This file can be found in the repository at ``installation/ubuntu/``

.. include:: ../../installation/ubuntu/patchserver.conf
    :code: python

Restart ``nginx`` for the changes to take effect:

.. code-block:: bash

    sudo service nginx restart

You should now be able to access the application using the IP address of the
system at port ``80`` (this is the default HTTP port and you do not need to
include it with the URL).
