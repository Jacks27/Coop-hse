import os

class Config:
    os.environ["FLASK_ENV"] = 'production'

    DEBUG = False
    FLASK_DEBUG = 0
    SECRET_KEY = "somethig acient, wide , deep and loooong"
    JWT_ALGORITHM = 'HS256'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    CONNECTION_STRING = os.environ["CONNECTION_STRING"]
    MAIL_SERVER=os.environ["MAIL_SERVER"]
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
class DevelopmentConfig(Config):
    os.environ["FLASK_ENV"] = 'development'

    FLASK_DEBUG = 1
    DEBUG = True
class TestConfig(Config):
    os.environ["FLASK_ENV"] = 'testing'
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    CONNECTION_STRING = os.environ["TEST_CONNECTION_STRING"]


configs = dict(
    testing=TestConfig,
    production=Config,
    development=DevelopmentConfig
)
