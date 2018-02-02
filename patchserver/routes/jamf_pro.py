from flask import blueprints, jsonify, request
import sqlalchemy

from .api_operations import lookup_software_title
from ..exc import SoftwareTitleNotFound
from ..models import SoftwareTitle

blueprint = blueprints.Blueprint('jamf_pro', __name__, url_prefix='/jamf/v1')


@blueprint.route('/software', methods=['GET', 'POST'])
def software_titles():
    """Endpoint for Jamf Pro"""
    if request.method == 'GET':
        titles = SoftwareTitle.query.all()
        return jsonify([title.serialize_short for title in titles]), 200


@blueprint.route('/software/<name_ids>')
def software_titles_select(name_ids):
    """Endpoint for Jamf Pro"""
    # Comma separated list of name IDs
    name_id_list = name_ids.split(',')
    title_list = SoftwareTitle.query.filter(
        sqlalchemy.or_(SoftwareTitle.id_name.in_(name_id_list))).all()

    not_found = [name for name in name_id_list
                 if name not in
                 [title.id_name for title in title_list]]
    if not_found:
        raise SoftwareTitleNotFound(not_found)
    else:
        return jsonify(
            [title.serialize_short for title in title_list]), 200


@blueprint.route('/patch/<name_id>')
def patch_by_name_id(name_id):
    """Endpoint for Jamf Pro"""
    return jsonify(lookup_software_title(name_id).serialize), 200
