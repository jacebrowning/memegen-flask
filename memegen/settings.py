import os
import logging


class Config:

    ENV = None

    PATH = os.path.abspath(os.path.dirname(__file__))
    ROOT = os.path.dirname(PATH)
    DEBUG = False
    THREADED = False

    # Constants
    GITHUB_SLUG = "jacebrowning/memegen-flask"
    GITHUB_URL = "https://github.com/{}".format(GITHUB_SLUG)
    GITHUB_BASE = "https://raw.githubusercontent.com/{}/main/".format(GITHUB_SLUG)
    CHANGES_URL = GITHUB_BASE + "CHANGELOG.md"
    CONTRIBUTING_URL = GITHUB_BASE + "CONTRIBUTING.md"

    # Variables
    BUGSNAG_API_KEY = os.getenv('BUGSNAG_API_KEY')
    FACEBOOK_APP_ID = 'localhost'
    FACEBOOK_IMAGE_HEIGHT = 492
    FACEBOOK_IMAGE_WIDTH = 940
    GOOGLE_ANALYTICS_TID = 'localhost'
    GOOGLE_ANALYTICS_URL = "http://www.google-analytics.com/collect"
    LOG_LEVEL = getattr(logging, os.getenv('LOG_LEVEL', 'INFO'))
    REGENERATE_IMAGES = os.getenv('REGENERATE_IMAGES')
    REMOTE_TRACKING_URL = os.getenv('REMOTE_TRACKING_URL')
    TWITTER_IMAGE_HEIGHT = 440
    TWITTER_IMAGE_WIDTH = 880
    WATERMARK_OPTIONS = os.getenv('WATERMARK_OPTIONS', "").split(',')


class ProductionConfig(Config):

    ENV = 'production'

    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    GOOGLE_ANALYTICS_TID = os.getenv('GOOGLE_ANALYTICS_TID')
    SLACK_APP_ID = os.getenv('SLACK_APP_ID')


class StagingCongif(ProductionConfig):

    ENV = 'staging'


class LocalConfig(Config):

    ENV = 'local'

    DEBUG = True

    LOG_LEVEL = logging.DEBUG
    WATERMARK_OPTIONS = ['localhost'] + Config.WATERMARK_OPTIONS


class TestConfig(LocalConfig):

    ENV = 'test'

    TESTING = True

    WATERMARK_OPTIONS = ['test', 'memegen.test', 'werkzeug']


def get_config(name):
    assert name, "No configuration specified"

    for config in _subclasses(Config):
        if config.ENV == name:
            return config

    assert False, "No matching configuration"
    return None


def _subclasses(cls):
    yield from cls.__subclasses__()
    yield from (g for s in cls.__subclasses__() for g in _subclasses(s))
