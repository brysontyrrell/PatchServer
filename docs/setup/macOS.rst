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

    .. code-block:: bash

        $ sudo easy_install pip
        $ sudo pip install virtualenv

.. note::

    You will need the full Xcode application on the host Mac in order to install
    ``mod_wsgi``. You can download Xcode from the Mac App Store.

Clone the project repository to a temporary directory. ``cd`` into the
``installation/macOS`` directory.

.. code-block:: bash

    git clone https://github.com/brysontyrrell/PatchServer.git /tmp/patchserver
    cd /tmp/patchserver/installation/macOS

Run the ``quick_install.sh``.

Once the script has successfully completed, you will be able to access the
application using ``localhost`` or the system's IP address at port ``5000``.

.. note::

    The LaunchDaemon provided will start the patch server on boot.

Contents of ``quick_install.sh``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../../installation/macOS/quick_install.sh
    :code: shell

Managing the Apache Server
^^^^^^^^^^^^^^^^^^^^^^^^^^

Start the server:

.. code-block:: bash

    $ sudo /usr/local/bin/patchserver/apachectl start

Stop the server:

.. code-block:: bash

    $ sudo /usr/local/bin/patchserver/apachectl stop

If the server does not start, check the ``/usr/local/bin/patchserver/error_log``
file for error messages.
