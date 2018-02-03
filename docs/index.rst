.. Jamf Pro Community Patch Server documentation master file, created by
   sphinx-quickstart on Fri Feb  2 12:00:28 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Jamf Pro Community Patch Server
================================

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

.. note::

   More documentation on the UI coming soon. Refer to the
   :doc:`Setup <setup/server>` for details on accessing your patch server after
   you have installed it.

Change History
--------------

0.5.0 (2018-02-02)
^^^^^^^^^^^^^^^^^^

Organized code.

JSON validation for API.

Really big documentation update (now hosted on Read the Docs).

Installation instructions for macOS and Docker.

Added ``GET /api/v1/backup``. Download a zipped archive of all patch definitions
on the server.

Version history notes.

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

Moved javascript out of the HTML and into static.

Database moved to application directory.

Patch title deletion.

Bug fixes.

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

Database improvements.

Proper deletion of all objects linked to a patch.

0.1.1 (2017-08-10)
^^^^^^^^^^^^^^^^^^

Initial GUI.

Deduplication of criteria entries.

Extension attribute objects.

0.1.0 (2017-08-09)
^^^^^^^^^^^^^^^^^^

Initial commit.
