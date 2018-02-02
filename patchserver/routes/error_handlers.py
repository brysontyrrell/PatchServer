from flask import blueprints, current_app, flash, jsonify
from sqlalchemy.exc import IntegrityError

from ..exc import InvalidPatchDefinitionError, SoftwareTitleNotFound

blueprint = blueprints.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(InvalidPatchDefinitionError)
def error_invalid_patch_definition(err):
    current_app.logger.error(err.message)
    flash(err.message)
    return jsonify({'invalid_json': err.message}), 400


@blueprint.app_errorhandler(SoftwareTitleNotFound)
def error_title_not_found(err):
    current_app.logger.error(err)
    return jsonify({'title_not_found': err.message}), 404


@blueprint.app_errorhandler(IntegrityError)
def database_integrity_error(err):
    if 'software_titles.id_name' in err.message:
        message = 'A software title of the provided name already exists.'
    else:
        message = err.message

    return jsonify({'database_conflict': message}), 409
