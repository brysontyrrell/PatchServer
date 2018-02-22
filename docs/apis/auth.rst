API Authentication
==================

You may optionally generate an API token that will be required for all requests
made to the following ``/api/v1/title*`` endpoints to prevent unauthenticated
requests to create, update, or delete software titles.

.. note::

    The ``/jamf/v1`` and ``/api/v1/backup`` endpoints remain open and will not
    use the API token for authentication.

.. warning::

    THe UI does not yet support API authentication. You will receive a
    **"Unauthorized: Authentication required"** message if you attempt to use
    the **New Title +** or **X (delete)** options.

See the :doc:`Patch Server API documentation <./ps_api>` for how to create an
API token.

Authenticating Requests
-----------------------

If you have created an API token, you must include it with your requests in the
``Authorization`` header and the ``Bearer`` type::

    Authorization: Bearer 94631ec5c65e4dd19fb81479abdd2929

Requests without this header will be rejected with a ``401`` status.

Retrieve/Reset the API Token
----------------------------

In the event you lose your API token, you can use a command line utillity such
as ``sqlite3`` to retrieve the existing token:

.. code-block:: bash

    $ sqlite3 patch_server.db "SELECT * FROM api_token;"

If you wish to reset the token, write a stub file into the ``patchserver``
application directory named ``reset_api_token`` and restart the server. The API
token will be deleted from the database and the stub file cleared. You will then
be allowed to create a new API token using ``/api/v1/token``.
