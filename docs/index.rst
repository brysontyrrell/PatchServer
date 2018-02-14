.. Patch Server for Jamf Pro documentation master file, created by
   sphinx-quickstart on Fri Feb  2 12:00:28 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Patch Server for Jamf Pro
=========================

An open-source implementation of an external patch source for use with Jamf Pro
(version 10.2+).

.. contents::
   :depth: 1
   :local:

.. toctree::
   :maxdepth: 1
   :caption: Setup Instructions

   setup/server
   setup/in_jamf_pro

.. toctree::
   :maxdepth: 1
   :caption: API Documentation

   apis/ps_api
   apis/jamf_pro

User Interface
--------------

.. image:: _static/gui_01_index.png
   :align: center

In a browser, the root of the patch server will take you to the main page where
you can view and manage the available software titles.

Upload a New Software Title
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click the **New Title** button to bring up the file selector. Browse for the
JSON file of the patch definition and then click **Upload**.

.. image:: _static/gui_02_upload.png
   :align: center

You will recieve a confirmation of a successful upload.

.. image:: _static/gui_03_created.png
   :align: center

Upload Errors
^^^^^^^^^^^^^

If the patch server rejects your upload of a patch definition, it will provide
a notification with the reason so you can correct the cause and retry.

There is a conflict with an existing software title.

.. image:: _static/gui_04_conflict.png
   :align: center

The patch definition failed validation, but the cause is displayed.

.. image:: _static/gui_05_validation.png
   :align: center

View a Patch Definition
^^^^^^^^^^^^^^^^^^^^^^^

Click the blue **View** icon for a software title to be taken to the URL of the
patch definition JSON.

.. image:: _static/gui_10_view.png
   :align: center

Delete a Software Title
^^^^^^^^^^^^^^^^^^^^^^^

Click the red **X** button for a software title to delete it.

.. warning::

   This action cannot be undone.

.. image:: _static/gui_08_delete.png
   :align: center

.. image:: _static/gui_09_deleted.png
   :align: center

Backup Your Patch Definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Click the **Backup** button and you will download a zipped archive of all patch
definitions for all your software titles.

.. note::

   This is a feature of the API that you can use with automation for scheduled
   backups of the server.

.. image:: _static/gui_06_backup.png
   :align: center

.. image:: _static/gui_07_archive.png
   :align: center

Change History
--------------

0.5.3 (2018-02-13)
^^^^^^^^^^^^^^^^^^

Because accurate and easy to read instructions are important.

0.5.2 (2018-02-08)
^^^^^^^^^^^^^^^^^^

A minor renaming.

0.5.1 (2018-02-03)
^^^^^^^^^^^^^^^^^^

Make the GUI great(ish) again. The **New Title** button has been updated. It now
prompts you to select a JSON file (the patch definition) and performs the
upload. Validation is still performed on the uploaded file as with the API.

The new ``/api/v1/backup`` feature is available in the GUI. Click the **Backup**
button to trigger.

The **View** button for a software title has been moved to the right and will
take the user to the ``/jamf/v1/patch/{title}`` endpoint to view the JSON.

All GUI actions now provide feeback on success or error.

0.5.0 (2018-02-02)
^^^^^^^^^^^^^^^^^^

Organized code. JSON validation for API. Really big documentation update (now
hosted on Read the Docs). Installation instructions for macOS and Docker.

Added ``GET /api/v1/backup``. Download a zipped archive of all patch definitions
on the server. Version history notes.

.. note::

   Removed most of the UI and some API endpoints no longer required without the
   associated UI views.

0.4.3 (2018-02-01)
^^^^^^^^^^^^^^^^^^

The non-existent requirements file now exists.

0.4.2 (2018-01-09)
^^^^^^^^^^^^^^^^^^

Patch eligibility criteria added to software title view.

0.4.1 (2018-01-08)
^^^^^^^^^^^^^^^^^^

Fixed UI redirects.

0.4.0 (2018-01-07)
^^^^^^^^^^^^^^^^^^

Switched to Pipenv for development.

0.3.3 (2018-01-05)
^^^^^^^^^^^^^^^^^^

Typos and such.

0.3.2 (2017-10-25)
^^^^^^^^^^^^^^^^^^

Editing software title in the UI view.

0.3.1 (2017-10-20)
^^^^^^^^^^^^^^^^^^

Moved javascript out of the HTML and into static. Database moved to application
directory. Patch title deletion. Bug fixes.

0.3.0 (2017-10-19)
^^^^^^^^^^^^^^^^^^

UI view for individual software titles.


0.2.1 (2017-10-12)
^^^^^^^^^^^^^^^^^^

Bug fix for software title creation.

0.2.0 (2017-08-23)
^^^^^^^^^^^^^^^^^^

Added RSS feed.

0.1.2 (2017-08-11)
^^^^^^^^^^^^^^^^^^

Database improvements. Proper deletion of all objects linked to a patch.

0.1.1 (2017-08-10)
^^^^^^^^^^^^^^^^^^

Initial GUI. Deduplication of criteria entries. Extension attribute objects.

0.1.0 (2017-08-09)
^^^^^^^^^^^^^^^^^^

Initial commit.
