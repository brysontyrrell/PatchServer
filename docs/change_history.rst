Change History
--------------

0.7.0 (2018-04-16)
^^^^^^^^^^^^^^^^^^

New webhook feature to allow the patch server to notify remote servers of
changes to software titles via HTTP POSTs.

0.6.0 (2018-02-14)
^^^^^^^^^^^^^^^^^^

You can secure the API with token authentication (if you really want to).

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
