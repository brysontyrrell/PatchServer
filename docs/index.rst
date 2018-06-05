.. Patch Server for Jamf Pro documentation master file, created by
   sphinx-quickstart on Fri Feb  2 12:00:28 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Patch Server for Jamf Pro
=========================

An open-source implementation of an external patch source for use with Jamf Pro
(version 10.2+).

.. contents::
   :depth: 2
   :local:

.. toctree::
   :maxdepth: 1

   change_history

.. toctree::
   :maxdepth: 1
   :caption: Managing Your Patch Server

   managing/patch_starter
   managing/troubleshooting

.. toctree::
   :maxdepth: 1
   :caption: Setup Instructions

   setup/testing
   setup/docker
   setup/macOS
   setup/ubuntu
   setup/in_jamf_pro

.. toctree::
   :maxdepth: 1
   :caption: API Documentation

   apis/auth
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

.. image:: _static/gui_02_new_title.png
   :align: center

You will recieve a confirmation of a successful upload.

.. image:: _static/gui_03_title_created.png
   :align: center

Upload Errors
^^^^^^^^^^^^^

If the patch server rejects your upload of a patch definition, it will provide
a notification with the reason so you can correct the cause and retry.

There is a conflict with an existing software title.

.. image:: _static/gui_04_title_conflict.png
   :align: center

The patch definition failed validation, but the cause is displayed.

.. image:: _static/gui_05_title_error.png
   :align: center

Update a Title's Version
^^^^^^^^^^^^^^^^^^^^^^^^

Click the green **Up** icon for a title to display a file prompt. Select the
JSON file containing the new version data and submit it.

.. image:: _static/gui_06_title_update.png
   :align: center

You will receive a confirmation of a successful upload.

.. image:: _static/gui_07_title_updated.png
   :align: center

You will also receive similar feedback for errors as with creating new titles.

Other Title Actions
^^^^^^^^^^^^^^^^^^^

There are additional actions available for each software title.

- The blue **View** icon will take you to the URL of the patch definition JSON.
- The red **X** icon will delete the title from the server.

.. image:: _static/gui_08_actions.png
   :align: center

.. warning::

   The delete action cannot be undone.

Backup Patch Definitions
^^^^^^^^^^^^^^^^^^^^^^^^

Click the **Backup** button and you will download a zipped archive of all patch
definitions for all your software titles.

.. note::

   This is a feature of the API that you can use with automation for scheduled
   backups of the server.

.. image:: _static/gui_09_backups.png
   :align: center

Webhooks
^^^^^^^^

The patch server can send notifications on changes to software titles on the
server to remote servers via *HTTP POST*. To configure a webhook, click the
**New Webhook** button to bring up the configuration screen. Enter the remote
**URL** and select from the available options:

- **Enabled:** Enable or disable this webhook.
- **Verify SSL:** Enable or disable SSL verification (HTTPS).
- **Send Definition:** When an event is sent, include a fully copy of the entire patch definition for the software title.
