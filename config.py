class BaseConfig:
    """ Base Configuration """
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    DEBUG = True

class TestingConfig(BaseConfig):
    """ Testing configuration """
    DEBUG = False
    TESTING = False

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False


