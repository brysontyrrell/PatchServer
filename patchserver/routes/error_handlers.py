from flask import blueprints, current_app, flash, jsonify, redirect, request, url_for
from sqlalchemy.exc import IntegrityError

from ..exc import InvalidPatchDefinitionError, SoftwareTitleNotFound

blueprint = blueprints.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(InvalidPatchDefinitionError)
def error_invalid_patch_definition(err):
    current_app.logger.error(err.message)

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Invalid Patch Definition JSON',
                'message': err.message
            },
            'warning')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'invalid_json': err.message}), 400


@blueprint.app_errorhandler(SoftwareTitleNotFound)
def error_title_not_found(err):
    current_app.logger.error(err)
    if request.args.get('redirect'):
        flash(
            {
                'title': 'Software title not found',
                'message': err.message
            },
            'warning')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'title_not_found': err.message}), 404


@blueprint.app_errorhandler(IntegrityError)
def database_integrity_error(err):
    if 'software_titles.id_name' in err.message:
        message = 'A software title of the given name already exists.'
    else:
        message = err.message

    if request.args.get('redirect'):
        flash(
            {
                'title': 'There was a conflict',
                'message': message
            },
            'danger')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'database_conflict': message}), 409
