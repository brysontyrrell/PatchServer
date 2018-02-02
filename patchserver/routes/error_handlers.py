from flask import blueprints, jsonify
from sqlalchemy.exc import IntegrityError

from ..exc import SoftwareTitleNotFound

blueprint = blueprints.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(SoftwareTitleNotFound)
def error_title_not_found(err):
    app.logger.error(err)
    return jsonify({'title_not_found': err.message}), 404


@blueprint.app_errorhandler(IntegrityError)
def database_integrity_error(err):
    if 'software_titles.id_name' in err.message:
        message = 'A software title of the provided name already exists.'
    else:
        message = err.message

    return jsonify({'database_conflict': message}), 409
