# -*- coding: utf-8 -*-
import os
from authomatic.providers import oauth2

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env.get('SGANNOTATE_SECRET', 'secret-key')  # TODO: Change me
    AUTHOMATIC = {

        'google': {

            'class_': oauth2.Google,

            # Facebook is an AuthorizationProvider too.
            'consumer_key': '69252368211-1b4usgu3ds5tiqdhu052rfcm0d5p56qv.apps.googleusercontent.com',
            'consumer_secret': '12jnj-Q0Pd7gIZxeAuebXza-',

            # But it is also an OAuth 2.0 provider and it needs scope.
            'scope': ['https://www.googleapis.com/auth/userinfo.email'],
        }
    }
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DB_NAME = 'prod.db'
    # Put the db file in project root
    DB_PATH = os.path.join('/db/', DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

