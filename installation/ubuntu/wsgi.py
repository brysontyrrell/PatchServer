import logging

from patchserver.factory import create_app

application = create_app()

gunicorn_logger = logging.getLogger('gunicorn.error')

for handler in gunicorn_logger.handlers:
    application.logger.addHandler(handler)

application.logger.setLevel(gunicorn_logger.level)
