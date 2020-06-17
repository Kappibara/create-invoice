import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'postgres://postgres:postgres@localhost:5432/piastrix_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
