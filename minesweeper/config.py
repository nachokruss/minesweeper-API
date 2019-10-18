import os
import sys


class Config(object):
    DEBUG = False
    PORT = 8080


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


def get_config():
    """
    Get the correct config class based on the ENVIRONMENT system env variable
    :return: The config class.
    """
    environment = os.environ.get('ENVIRONMENT', 'development')
    capitalized_env_value = environment[:1].upper() + environment[1:].lower()
    env_config_class_name = '{}Config'.format(capitalized_env_value)

    current_module = sys.modules[__name__]
    config_class = getattr(current_module, env_config_class_name)

    return config_class
