Installation on Ubuntu Server (16.04)
-------------------------------------

The following instructions are for setting up the patch server application on an
Ubuntu 16.04 system using ``gunicorn`` and ``systemd``.

.. warning::

    These instructions do not cover securing your patch server with a TLS
    certificate for HTTPS connections.

Install ``git``, ``python``, and ``virtualenv`` on the system:

.. code-block:: bash

    /usr/bin/apt-get update -q
    /usr/bin/apt-get install -qqy git virtualenv python-minimal

Clone the project repository to a temporary directory. ``cd`` into the
``installation/ubuntu`` directory.

.. code-block:: bash

    /usr/bin/git clone https://github.com/brysontyrrell/PatchServer.git /tmp/patchserver
    cd /tmp/patchserver/installation/ubuntu

Run the ``quick_install.sh``.

.. code-block:: bash

    sudo quick_install.sh


Once the script has completed you should be able to access the application using
the IP address of the system at port ``5000``.

Contents of ``quick_install.sh``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../../installation/ubuntu/quick_install.sh
    :code: bash
