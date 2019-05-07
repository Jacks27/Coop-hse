import os

class Config:
    os.environ["FLASK_ENV"] = 'production'

    DEBUG = False
    FLASK_DEBUG = 0
    SECRET_KEY = "somethig acient, wide , deep and loooong"
    JWT_ALGORITHM = 'HS256'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    CONNECTION_STRING = ENV["CONNECTION_STRING"]
    MAIL_SERVER=ENV["MAIL_SERVER"]
    MAIL_USERNAME = ENV["MAIL_USERNAME"]
    MAIL_PASSWORD = ENV["MAIL_PASSWORD"]
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
class DevelopmentConfig(Config):
    ENV["FLASK_ENV"] = 'development'

    FLASK_DEBUG = 1
    DEBUG = True
class TestConfig(Config):
    ENV["FLASK_ENV"] = 'testing'
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    CONNECTION_STRING = ENV["TEST_CONNECTION_STRING"]


configs = dict(
    testing=TestConfig,
    production=Config,
    development=DevelopmentConfig
)
