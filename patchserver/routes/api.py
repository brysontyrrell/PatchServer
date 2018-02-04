import json

from flask import (
    blueprints,
    flash,
    jsonify,
    redirect,
    request,
    send_file,
    url_for
)

from .api_operations import (
    create_criteria_objects,
    create_extension_attributes,
    create_patch_objects,
    lookup_software_title,
    create_backup_archive
)
from .validator import validate_json
from ..database import db
from ..exc import InvalidPatchDefinitionError
from ..models import SoftwareTitle

blueprint = blueprints.Blueprint('api', __name__, url_prefix='/api/v1')


@blueprint.route('/title', methods=['POST'])
def title_create():
    """Create a new patch definition on the server.

    .. :quickref: Software Title; Create a patch definition.

    **Example Request:**

    .. sourcecode:: http

        POST /api/v1/title HTTP/1.1
        Content-Type: application/json

        {
            "id": "Composer",
            "name": "Composer",
            "publisher": "Jamf",
            "appName": "Composer.app",
            "bundleId": "com.jamfsoftware.Composer",
            "requirements": ["requirementObjects"],
            "patches": ["versionObjects"],
            "extensionAttributes": ["extensionAttributeObjects"]
        }

    .. note::

        The JSON schema for a patch definition can be found in the project
        repository at:
        ``patchserver/routes/validator/schema_full_definition.json``

    **Example Response:**

    A successful response will return a ``201`` status with the numerical
    database ID as well as the definition's ID.

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        {
            "database_id": 1,
            "id": "Composer"
        }

    **Error Responses**

    A ``409`` status is returned if you attempt to create a patch definition
    using an ID that already exists in the database.

    .. sourcecode:: http

        HTTP/1.1 409 Conflict
        Content-Type: application/json

        {
            "database_conflict": "A software title of the provided name already exists."
        }

    A ``400`` status can be returned if your patch definition fails a
    validation check against the JSON schema. If this occurs, a reason will
    be provided in the JSON response.

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Content-Type: application/json

        {
            "invalid_json": "Validation error encountered with submitted JSON for item: /u'true' is not of type u'boolean'"
        }

    A ``400`` status can be returned if your patch definition fails a
    validation check against the JSON schema. If this occurs, a reason will
    be provided in the JSON response.

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Content-Type: application/json

        {
            "invalid_json": "Validation error encountered with submitted JSON: u'true' is not of type u'boolean' for item: /patches/0/components/0/criteria/0/and"
        }

    """
    data = request.get_json()
    if not data:
        try:
            data = json.load(request.files['file'])
        except ValueError:
            raise InvalidPatchDefinitionError('No JSON data could be found.')

    validate_json(data, 'patch')

    new_title = SoftwareTitle(
        id_name=data['id'],
        name=data['name'],
        publisher=data['publisher'],
        app_name=data['appName'],
        bundle_id=data['bundleId']
    )
    db.session.add(new_title)

    if data.get('requirements'):
        create_criteria_objects(
            data['requirements'], software_title=new_title)

    if data.get('patches'):
        create_patch_objects(
            list(reversed(data['patches'])), software_title=new_title)

    if data.get('extensionAttributes'):
        create_extension_attributes(
            data['extensionAttributes'], new_title)

    db.session.commit()

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Software title created',
                'message': 'View at <a href="{0}">{0}</a>'.format(
                    url_for('jamf_pro.patch_by_name_id',
                            name_id=new_title.id_name))
            },
            'success')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify(
            {'id': new_title.id_name, 'database_id': new_title.id}), 201


@blueprint.route('/title/<name_id>', methods=['DELETE'])
def title_delete(name_id):
    """Delete a patch definition on the server.

    .. :quickref: Software Title; Delete a patch definition.

    **Example Request:**

    .. sourcecode:: http

        DELETE /api/v1/title/Composer HTTP/1.1

    **Example Response:**

    A successful response will return a ``204`` status.

    .. sourcecode:: http

        HTTP/1.1 204 No Content

    **Error Responses**

    A ``404`` status is returned if the specified patch definition does
    not exist.

    .. sourcecode:: http

        HTTP/1.1 404 Not Found
        Content-Type: application/json

        {
            "title_not_found": "Composer"
        }

    """
    title = lookup_software_title(name_id)
    db.session.delete(title)
    db.session.commit()

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Software title deleted:',
                'message': name_id
            },
            'success')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({}), 204


@blueprint.route('/title/<name_id>/version', methods=['POST'])
def title_versions(name_id):
    """Create a new patch version for an existing patch definition.

    .. :quickref: Patch Version; Create a patch version.

    **Example Request:**

    .. sourcecode:: http

        POST /api/v1/title/Composer/version HTTP/1.1
        Content-Type: application/json

        {
            "items": [
                {
                    "version": "10.1.1",
                    "releaseDate": "2017-12-20T10:08:38.270Z",
                    "standalone": true,
                    "minimumOperatingSystem": "10.9",
                    "reboot": false,
                    "killApps": [
                        {
                            "bundleId": "com.jamfsoftware.Composer",
                            "appName": "Composer.app"
                        }
                    ],
                    "components": [
                        {
                            "name": "Composer",
                            "version": "10.1.1",
                            "criteria": ["requirementsObjects"]
                        }
                    ],
                    "capabilities": ["requirementsObjects"],
                    "dependencies": []
                }
            ]
        }

    .. note::

        The JSON schema for a patch definition can be found in the project
        repository at:
        ``patchserver/routes/validator/schema_version.json``

    .. warning::

        You may pass multiple version objects in the ``items`` array to this
        endpoint. You must arrange these objects in descending order of the
        version to be written to the patch definition correctly!

    **Example Response:**

    A successful response will return a ``201`` status.

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        {}

    **Error Responses**

    A ``400`` status can be returned if your patch version fails a validation
    check against the JSON schema. If this occurs, a reason will be provided in
    the JSON response.

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Content-Type: application/json

        {
            "invalid_json": "Validation error encountered with submitted JSON: u'true' is not of type u'boolean' for item: /patches/0/components/0/criteria/0/and"
        }

    """
    title = lookup_software_title(name_id)
    data = request.get_json()

    for version in data['items']:
        validate_json(version, 'version')
        if version['version'] in [patch.version for patch in title.patches]:
            return jsonify(
                {'database_conflict': 'The provided version already exists '
                                      'for this software title.'}
            ), 409

    create_patch_objects(data['items'], software_title=title)
    db.session.commit()

    return jsonify({}), 201


@blueprint.route('/backup')
def backup_titles():
    """Download a zipped archive of all patch definitions.

    .. :quickref: Software Title; Downloadable archive of all software titles.

    **Example Request:**

    .. sourcecode:: http

        GET /api/v1/backup HTTP/1.1

    **Example Response:**

    A successful response will return a ``200`` status and a zipped archive
    containing the patch definitions.

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/zip

        <patch_archive.zip>

    """
    archive = create_backup_archive()
    return send_file(
        archive, as_attachment=True, attachment_filename='patch_archive.zip'
    ), 200
