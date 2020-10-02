Docker
------

Build Image
^^^^^^^^^^^

In the ``docker`` directory of the project repository is a ``Dockerfile`` that can be
used to launch the patch server as a container.

Clone the project repository to your computer. Create the Docker image with:

.. code-block:: bash

    $ cd /path/to/PatchServer
    $ docker build --tag patchserver:latest -f installation/docker/Dockerfile .

Run Container
^^^^^^^^^^^^^

Run a container with the following command:

.. code-block:: bash

    $ docker run -v /<patchserver-data>:/var/lib/patchserver -p 5000:5000 patchserver

.. note::

    Use the ``-d`` option to run the container in the background.

.. note::

    The ``-v /<patchserver-data>:/var/lib/patchserver`` option is to mount a
    local directory to the path in the running container where the persistent
    data for the patch server is stored (i.e. the database).

.. warning::

    If you do not attach a volume to ``/var/lib/patchserver`` the database will
    be erased when the container is stopped and removed.

You will be able to access the application using the IP address of the host
(your computer's IP address when running Docker locally) at port ``5000``.

Performance
^^^^^^^^^^^

The application, by default, runs 2 worker per available CPU plus 1 (a 2 CPU host will
produce 5 workers) with 1 thread per worker. 

Advanced Usage
^^^^^^^^^^^^^^

Coming soon.
