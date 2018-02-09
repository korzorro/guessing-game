import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'guessing_game.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = 'korzon.ninja'


class TestConfig(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    FIXTURES_DIRS = [basedir + '/test/fixtures']
