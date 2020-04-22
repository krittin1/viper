"""Flask config class."""
import os


# class Config:
#     """Set Flask configuration vars."""

    # General Config
TESTING = True
DEBUG = True
SECRET_KEY = '68Fnw8J3DLdMFjkH9jCdZP'
SESSION_COOKIE_NAME = 'my_cookie'


# class ProductionConfig(Config):
#     """
#     This class will inherit any attributes from the parent Config class.
#     Use this class to define production configuration atrributes, such
#     as database usernames, passwords, server specific files & directories etc.
#     """
#     pass


# class DevelopmentConfig(Config):
#     """
#     This class will inherit any attributes from the parent Config class.
#     Use this class to define development configuration atrributes, such
#     as local database usernames, passwords, local specific files & directories etc.
#     """
#     DEBUG = True