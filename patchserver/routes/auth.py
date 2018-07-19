import functools

from flask import current_app, request

from patchserver.exc import Unauthorized
from patchserver.models import ApiToken


def api_auth(func):
    """A decorator for routes that requires token authentication on a request if
    the API token exists in the database.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        api_token = ApiToken.query.first()
        if api_token:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise Unauthorized('Authentication required')

            schema, auth_token = auth_header.split()
            current_app.logger.debug(schema)
            current_app.logger.debug(auth_token)

            if schema != 'Bearer' or api_token.token != auth_token:
                raise Unauthorized('Invalid token provided')

            current_app.logger.debug('Auth successful')
        return func(*args, **kwargs)
    return wrapped
