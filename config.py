import os


class Config(object):
    pass


class ProdConfig(object):
    pass


class DevConfig(object):
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': 'mongodb',
        'port': 27017,
        'db': 'dev'
    }

class TestConfig(object):
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': 'mongodb',
        'port': 27017,
        'db': 'test'
    }
