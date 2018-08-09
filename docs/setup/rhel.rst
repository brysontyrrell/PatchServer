Installation on RHEL Server (7.3)
-------------------------------------

The following instructions are for setting up the patch server application on an
RHEL 7.5 system using ``gunicorn`` and ``systemd``.

.. warning::

    These instructions do not cover securing your patch server with a TLS
    certificate for HTTPS connections.

Enable EPEL repository if needed:

.. code-block:: bash

    wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    sudo rpm -ivh epel-release-latest-7.noarch.rpm

Install ``git``, ``httpd``, and ``pip`` on the system:

.. code-block:: bash

    sudo /bin/yum update -q
    sudo /bin/yum install -y git httpd python-pip python-wheel python-virtualenv

Clone the project repository to a temporary directory. ``cd`` into the
``installation/rhel`` directory.

.. code-block:: bash

    /usr/bin/git clone https://github.com/brysontyrrell/PatchServer.git /tmp/patchserver
    cd /tmp/patchserver/installation/rhel

Run the ``quick_install.sh``.

.. code-block:: bash

    sudo bash quick_install.sh


Once the script has completed you should be able to access the application using
the IP address of the system at port ``5000``. You may have to allow TCP port 5000 through the firewall:

.. code-block:: bash

    sudo firewall-cmd --zone=public --add-port=5000/tcp

Contents of ``quick_install.sh``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../../installation/rhel/quick_install.sh
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

    sudo /bin/yum update -q
    sudo /bin/yum install -qqy nginx

Remove the default Nginx site:

.. code-block:: bash

    sudo rm /etc/nginx/sites-enabled/default

Modify the `bind` value of ``/opt/patchserver/config.py`` to have ``gunicorn``
bind the application to localhost at port ``5000``:

.. code-block:: python

    bind = "127.0.0.1:5000"

Write the following to a new file called ``/etc/nginx/conf.d/patchserver.conf``:

.. note::

    This file can be found in the repository at ``installation/rhel/``

.. include:: ../../installation/rhel/patchserver.conf
    :code: python

Restart ``nginx`` for the changes to take effect:

.. code-block:: bash

    sudo service nginx restart

You should now be able to access the application using the IP address of the
system at port ``80`` (this is the default HTTP port and you do not need to
include it with the URL).
