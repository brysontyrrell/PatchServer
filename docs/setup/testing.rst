Testing the Patch Server
------------------------

.. warning::

    Using the included ``run.py`` script is not recommended for a production
    environment. See the other options below depending upon your platform.

Clone the project repository to the system that will run the application.

Change into the directory for the project, create a Python virtual environment,
and install the project requirements to it.

.. code-block:: bash

    $ cd /path/to/PatchServer
    $ virtualenv ./venv
    $ source ./venv/bin/activate
    (venv) $ pip install -r ./requirements.txt

Run the application.

.. code-block:: bash

    python run.py


You will be able to access the application using ``localhost`` or your
computer's IP address at port ``5000``.
