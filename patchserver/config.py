import os

APP_DIR = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
SQL_LOGGING = False

SQLALCHEMY_DATABASE_URI = 'sqlite:////{}' .format(
    os.path.join(APP_DIR, 'patch_server.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False
