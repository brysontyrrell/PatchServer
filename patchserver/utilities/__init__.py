import os

from flask import current_app

from patchserver.database import db
from patchserver.models import ApiToken


def reset_api_token():
    """Deletes the API token in the Patch Server database.

    This function is invoked on startup if the ``reset_api_token`` file has been
    written to the application directory.

    The file is removed when this function is invoked.
    """
    token = ApiToken.query.first()
    if token:
        current_app.logger.info("Resetting API Token")
        db.session.delete(token)
        db.session.commit()

    current_app.config.pop('RESET_API_TOKEN')
    current_app.logger.info("Removing 'reset_api_token' stub")
    os.remove(os.path.join(
        current_app.config['APP_DIR'], 'reset_api_token'))
