import os


class Config(object):
    TEST_CONFIG = os.getenv('TEST_CONFIG', '')
