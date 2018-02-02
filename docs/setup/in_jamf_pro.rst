Add Your Patch Server to Jamf Pro
=================================

Configure the patch server as an External Patch Source in Jamf Pro.

.. note::

    "External Patch Sources" is a feature of Jamf Pro v10.2+.

To add your Patch Server as a ``Patch External Source`` in Jamf Pro, go to:

**Settings > Computer Management > Patch Management**

1. Click the ``+ New`` button next to ``Patch External Source``.
2. Give the Patch Server a name.
3. Enter the URL without the schema (i.e. ``https://``) in the ``SERVER AND PORT`` field (e.g. ``<API-GATEWAY-ID>.execute-api.<REGION>.amazonaws.com/Prod/``) and 443 for the ``PORT``.
4. Check the ``Use SSL`` box.

The Patch Server will now be available to subscribe to when adding new titles under ``Patch Management``:

**Computers > Patch Management**
