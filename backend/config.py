# Configuration settings for the backend application

import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    # Add other configuration variables as needed
    DRONE_DATA_PATH = os.environ.get('DRONE_DATA_PATH', 'backend/data/droneType002.csv')
    PORT_DATA_PATH = os.environ.get('PORT_DATA_PATH', 'backend/data/merged_ports_data.csv')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
