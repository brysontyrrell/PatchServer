from flask import blueprints, jsonify, request

from .api_operations import (
    create_criteria_objects,
    create_extension_attributes,
    create_patch_objects,
    lookup_software_title
)
from .validator import validate_json
from ..database import db
from ..models import SoftwareTitle

blueprint = blueprints.Blueprint('api', __name__, url_prefix='/api/v1')


@blueprint.route('/title', methods=['POST'])
def title_create():
    """Create a new Patch Software Title"""
    data = request.get_json()
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

    return jsonify(
        {'id': new_title.id_name, 'database_id': new_title.id}), 201


@blueprint.route('/title/<name_id>', methods=['PUT', 'DELETE'])
def title_update_delete(name_id):
    """Update or Delete a Patch Software Title"""
    title = lookup_software_title(name_id)
    data = request.get_json()

    if request.method == 'PUT':
        validate_json(data, 'patch')
        
        if 'id' in data:
            data.pop('id')

        title.name = data['name']
        title.publisher = data['publisher']
        title.app_name = data['appName']
        title.bundle_id = data['bundleId']

        db.session.commit()
        return '', 204

    elif request.method == 'DELETE':
        db.session.delete(title)
        db.session.commit()
        return jsonify({}), 204


@blueprint.route('/title/<name_id>/versions', methods=['GET', 'POST'])
def title_versions(name_id):
    """
    POST Accepts:
        {
            "items": [
                <patch_object>
            ]
        }
        """
    title = lookup_software_title(name_id)

    if request.method == 'GET':
        return jsonify(
            {
                'id': title.id_name,
                'versions': [patch.serialize for patch in title.patches]
            }
        ), 200

    elif request.method == 'POST':
        data = request.get_json()
        validate_json(data, 'version')

        create_patch_objects(data['items'], software_title=title)
        db.session.commit()

        return jsonify({}), 201
