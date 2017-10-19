"""
/ - Welcome message

--- Jamf Pro Endpoints ---

/jamf/v1/software - GET Returns patch software titles
/jamf/v1/software/<Name> - GET Returns subset of named titles
/jamf/v1/patch/<Name> - GET Returns full patch definition of a title

--- Patch Server API ---

/api/v1/title/create - POST Create a new patch software title

/api/v1/title/<Name>/requirements - GET Returns all requirements of a title
/api/v1/title/<Name>/requirements/add - POST Add requirements onto a title

/api/v1/title/<Name>/patches - GET Returns all patch versions of a title
/api/v1/title/<Name>/patches/add - POST Add patch versions onto a title
"""

import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

__title__ = 'PatchServer'
__version__ = '1.3.0'
__author__ = 'Bryson Tyrrell'

app = Flask(__name__)

app.config.from_object(config)

db = SQLAlchemy(app)

if app.config.get('DEBUG'):
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.DEBUG)

    for handler in app.logger.handlers:
        sql_logger.addHandler(handler)

import models
import routes
