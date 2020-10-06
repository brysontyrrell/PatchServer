from flask import blueprints, jsonify
import sqlalchemy

from patchserver.models import SoftwareTitle
from patchserver.routes.api_operations import lookup_software_title

blueprint = blueprints.Blueprint("jamf_pro", __name__, url_prefix="/jamf/v1")


@blueprint.route("/software", methods=["GET"])
def software_titles():
    """Returns all available software titles on server.

    .. :quickref: Software Title; List all software titles.

    **Example Request:**

    .. sourcecode:: http

        GET /jamf/v1/software HTTP/1.1
        Accept: application/json

    **Example Response:**

    A successful response will return a ``200`` status and an array of software
    title summaries.

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "currentVersion": "10.1.1",
                "id": "Composer",
                "lastModified": "2018-02-02T17:39:58Z",
                "name": "Composer",
                "publisher": "Jamf"
            },
            {
                "currentVersion": "10.1.1",
                "id": "JamfAdmin",
                "lastModified": "2018-02-02T17:39:51Z",
                "name": "Jamf Admin",
                "publisher": "Jamf"
            },
            {
                "currentVersion": "10.1.1",
                "id": "JamfImaging",
                "lastModified": "2018-02-02T17:39:53Z",
                "name": "Jamf Imaging",
                "publisher": "Jamf"
            },
            {
                "currentVersion": "10.1.1",
                "id": "JamfRemote",
                "lastModified": "2018-02-02T17:39:56Z",
                "name": "Jamf Remote",
                "publisher": "Jamf"
            }
        ]

    """
    titles = SoftwareTitle.query.all()
    return jsonify([title.serialize_short for title in titles]), 200


@blueprint.route("/software/<name_ids>")
def software_titles_select(name_ids):
    """Returns a selection of software titles on server. The software title IDs
    must be passed as a comma separated string.

    .. :quickref: Software Title; List selected software titles.

    **Example Request:**

    .. sourcecode:: http

        GET /jamf/v1/software/Composer,JamfImaging HTTP/1.1
        Accept: application/json

    **Example Response:**

    A successful response will return a ``200`` status and an array of software
    title summaries.

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "currentVersion": "10.1.1",
                "id": "Composer",
                "lastModified": "2018-02-02T17:39:58Z",
                "name": "Composer",
                "publisher": "Jamf"
            },
            {
                "currentVersion": "10.1.1",
                "id": "JamfImaging",
                "lastModified": "2018-02-02T17:39:53Z",
                "name": "Jamf Imaging",
                "publisher": "Jamf"
            }
        ]

    **Error Responses**

    .. sourcecode:: http

        GET /jamf/v1/software/Composers,JamfImager HTTP/1.1
        Accept: application/json

    A ``404`` status is returned if any of the specified software titles do not
    exist.

    .. sourcecode:: http

        HTTP/1.1 404 Not Found
        Content-Type: application/json

        {
            "title_not_found": [
                "Composers",
                "JamfImager"
            ]
        }

    """
    # Comma separated list of name IDs
    name_id_list = name_ids.split(",")
    title_list = SoftwareTitle.query.filter(
        sqlalchemy.or_(SoftwareTitle.id_name.in_(name_id_list))
    ).all()

    return jsonify([title.serialize_short for title in title_list]), 200


@blueprint.route("/patch/<name_id>")
def patch_by_name_id(name_id):
    """Returns a selection of software titles on server. The software title IDs
    must be passed as a comma separated string.

    .. :quickref: Software Title; Return a patch definition.

    **Example Request:**

    .. sourcecode:: http

        GET /jamf/v1/patch/Composer HTTP/1.1
        Accept: application/json

    **Example Response:**

    A successful response will return a ``200`` status and the full patch
    definition for the specified software title.

    .. sourcecode:: http

        HTTP/1.1 200 OK
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

    **Error Responses**

    .. sourcecode:: http

        GET /jamf/v1/software/Composers HTTP/1.1
        Accept: application/json

    A ``404`` status is returned if any of the specified software title does not
    exist.

    .. sourcecode:: http

        HTTP/1.1 404 Not Found
        Content-Type: application/json

        {
            "title_not_found": "Composers"
        }

    """
    return jsonify(lookup_software_title(name_id).serialize), 200
