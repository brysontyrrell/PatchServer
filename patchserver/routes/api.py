import json
from urlparse import urlparse

from flask import (
    blueprints,
    flash,
    g,
    jsonify,
    redirect,
    request,
    send_file,
    url_for
)

from patchserver.database import db
from patchserver.exc import InvalidPatchDefinitionError, InvalidWebhook
from patchserver.models import ApiToken, SoftwareTitle, WebhookUrls
from patchserver.routes.api_operations import (
    create_criteria_objects,
    create_extension_attributes,
    create_patch_objects,
    lookup_software_title,
    create_backup_archive,
    restore_backup_archive
)
from patchserver.routes.auth import api_auth
from patchserver.routes.validator import validate_json
from patchserver.routes.webhooks import webhook_event

blueprint = blueprints.Blueprint('api', __name__, url_prefix='/api/v1')


@blueprint.route('/token', methods=['POST'])
def token_create():
    """Create an API token for the server.

    .. :quickref: Token; Create the API token.

    **Example Request:**

    .. sourcecode:: http

        POST /api/v1/token HTTP/1.1

    **Example Response:**

    A successful response will return a ``201`` status with the API token.

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        {
            "token_created": "94631ec5c65e4dd19fb81479abdd2929"
        }

    **Error Responses**

    A ``403`` status is returned if an API token already exists.

    .. sourcecode:: http

        HTTP/1.1 403 Forbidden
        Content-Type: application/json

        {
            "forbidden": "A token already exists for this server"
        }

    :return:
    """
    if ApiToken.query.first():
        return jsonify(
            {'forbidden': 'A token already exists for this server'}), 403

    new_token = ApiToken()
    db.session.add(new_token)
    db.session.commit()

    return jsonify({'token_created': new_token.token}), 201


@blueprint.route('/title', methods=['POST'])
@api_auth
@webhook_event
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

    g.event_type = 'new_title'
    g.event = new_title.serialize

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
@api_auth
@webhook_event
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

    g.event_type = 'title_deleted'
    g.event = title.serialize

    db.session.delete(title)
    db.session.commit()

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Software title deleted',
                'message': name_id
            },
            'success')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({}), 204


@blueprint.route('/title/<name_id>/version', methods=['POST'])
@api_auth
def title_versions(name_id):
    """Create a new patch version for an existing patch definition.

    .. :quickref: Software Title; Create a patch version.

    **Example Request:**

    .. sourcecode:: http

        POST /api/v1/title/Composer/version HTTP/1.1
        Content-Type: application/json

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

    .. note::

        The JSON schema for a patch definition can be found in the project
        repository at:
        ``patchserver/routes/validator/schema_version.json``

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
    data = request.get_json()
    if not data:
        try:
            data = json.load(request.files['file'])
        except ValueError:
            raise InvalidPatchDefinitionError('No JSON data could be found.')

    validate_json(data, 'version')

    title = lookup_software_title(name_id)
    if data['version'] in [patch.version for patch in title.patches]:
        return jsonify(
            {'database_conflict': 'The provided version already exists '
                                  'for this software title.'}
        ), 409

    create_patch_objects([data], software_title=title)
    db.session.commit()

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Software title version updated',
                'message': 'View at <a href="{0}">{0}</a>'.format(
                    url_for('jamf_pro.patch_by_name_id', name_id=name_id))
            },
            'success')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({}), 201


@blueprint.route('/backup')
def backup_titles():
    """Download a zipped archive of all patch definitions.

    .. :quickref: Backup; Downloadable archive of all software titles.

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


@blueprint.route('/restore', methods=['POST'])
def restore_titles():
    """Restore a zipped archive of definitions to the server. This endpoint
    may only be used when no definitions exist. If definitions have been created
    the restore request will be rejected.

    .. :quickref: Backup; Restore definitions from a zipped archive of software titles.

    **Example Request:**

    .. sourcecode:: http

        POST /api/v1/restore HTTP/1.1
        Content-Type: application/zip

        <patch_archive.zip>

    **Example Response:**

    A successful response will return a ``201`` status and a JSON object
    containing the software title IDs and their database IDs.

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "database_id": 1,
                "id": "Composer"
            },
            {
                "database_id": 2,
                "id": "JamfImaging"
            }
        ]

    **Error Responses**

    A ``400`` status can be returned if a file other than a zip archive is
    submitted, if a validation error occurs when processing the unzipped
    definitions, or if the request was made after definitions have been already
    created.

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Content-Type: application/json

        {
            "restore_failure": "The submitted file is not a .zip archive"
        }

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Content-Type: application/json

        {
            "restore_failure": "A definition in the archive failed validation"
        }

    .. sourcecode:: http

        HTTP/1.1 400 Bad Request
        Content-Type: application/json

        {
            "restore_failure": "Definitions already exist on this server"
        }

    """
    uploaded_file = request.files['file']
    restored_definitions = restore_backup_archive(uploaded_file)
    return jsonify(restored_definitions), 201


@blueprint.route('/webhooks', methods=['GET', 'POST'])
@api_auth
def webhooks():
    if request.method == 'GET':
        results = list()
        for webhook in WebhookUrls.query.all():
            results.append(webhook.serialize)

        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            data = {
                'url': request.form.get('url', ''),
                'enabled': bool(request.form.get('enabled')),
                'send_definition': bool(request.form.get('send_definition'))
            }

        def validate_url(url):
            parsed = urlparse(url)
            if parsed.scheme and parsed.netloc:
                return True
            else:
                return False

        if not validate_url(data['url']):
            raise InvalidWebhook('The provided URL is invalid')

        new_webhook = WebhookUrls(
            url=data['url'],
            enabled=data['enabled'],
            send_definition=data['send_definition']
        )
        db.session.add(new_webhook)
        db.session.commit()

        if request.args.get('redirect'):
            flash(
                {
                    'title': 'Webhook saved',
                    'message': 'The new webhook has been saved.'
                },
                'success')
            return redirect(url_for('web_ui.index'))
        else:
            return jsonify({'id': new_webhook.id}), 201


@blueprint.route('/webhooks/<webhook_id>', methods=['DELETE'])
@api_auth
def webhooks_delete(webhook_id):
    """Delete a configured webhook from the server by ID.

    .. :quickref: Webhooks; Delete a webhook.

    **Example Request:**

    .. sourcecode:: http

        DELETE /api/v1/webhooks/1 HTTP/1.1

    **Example Response:**

    A successful response will return a ``204`` status.

    .. sourcecode:: http

        HTTP/1.1 204 No Content

    **Error Responses**

    A ``404`` status is returned if the specified webhook does not exist.

    .. sourcecode:: http

        HTTP/1.1 404 Not Found
        Content-Type: application/json

        {
            "webhook_id_not_found": 1
        }

    """
    webhook = WebhookUrls.query.filter_by(id=webhook_id).first()
    if not webhook:
        flash({'title': 'Not found!', 'message': ''}, 'error')
        return redirect(url_for('web_ui.index'))

    webhook_url = webhook.url

    db.session.delete(webhook)
    db.session.commit()

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Webhook deleted',
                'message': webhook_url
            },
            'success')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({}), 204
