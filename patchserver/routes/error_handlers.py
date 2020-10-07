from flask import blueprints, current_app, flash, jsonify, redirect, request, url_for
from sqlalchemy.exc import IntegrityError

from patchserver.exc import (
    InvalidPatchDefinitionError,
    InvalidWebhook,
    PatchArchiveRestoreFailure,
    SoftwareTitleNotFound,
    Unauthorized,
)

blueprint = blueprints.Blueprint("error_handlers", __name__)


@blueprint.app_errorhandler(Unauthorized)
def unauthorized(err):
    current_app.logger.error(err.message)

    if request.user_agent.browser:
        flash({"title": "Unauthorized", "message": err.message}, "warning")
        return redirect(url_for("web_ui.index"))
    else:
        return jsonify({"unauthorized": err.message}), 401


@blueprint.app_errorhandler(InvalidPatchDefinitionError)
def error_invalid_patch_definition(err):
    current_app.logger.error(err.message)

    if request.user_agent.browser:
        flash(
            {"title": "Invalid Patch Definition JSON", "message": err.message},
            "warning",
        )
        return redirect(url_for("web_ui.index"))
    else:
        return jsonify({"invalid_json": err.message}), 400


@blueprint.app_errorhandler(InvalidWebhook)
def error_invalid_webhook(err):
    current_app.logger.error(err.message)

    if request.user_agent.browser:
        flash({"title": "Invalid Webhook", "message": err.message}, "warning")
        return redirect(url_for("web_ui.index"))
    else:
        return jsonify({"invalid_json": err.message}), 400


@blueprint.app_errorhandler(SoftwareTitleNotFound)
def error_title_not_found(err):
    current_app.logger.error(err)
    if request.user_agent.browser:
        flash({"title": "Software title not found", "message": err.message}, "warning")
        return redirect(url_for("web_ui.index"))
    else:
        return jsonify({"title_not_found": err.message}), 404


@blueprint.app_errorhandler(IntegrityError)
def database_integrity_error(err):
    current_app.logger.exception(str(err.__dict__))
    message = (
        "Unable to write title to the database. A title of the given name may already."
    )

    if request.user_agent.browser:
        flash({"title": "There was a conflict", "message": message}, "danger")
        return redirect(url_for("web_ui.index"))
    else:
        return jsonify({"message": message}), 409


@blueprint.app_errorhandler(PatchArchiveRestoreFailure)
def archive_restore_failure(err):
    current_app.logger.error(err.message)

    if request.user_agent.browser:
        flash(
            {"title": "Unable to Restore Patch Archive", "message": err.message},
            "warning",
        )
        return redirect(url_for("web_ui.index"))
    else:
        return jsonify({"restore_failure": err.message}), 400
