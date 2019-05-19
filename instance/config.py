import os

class Config:
    os.environ["FLASK_ENV"] = 'production'

    DEBUG = False
    FLASK_DEBUG = 0
    SECRET_KEY = "somethig acient, wide , deep and loooong"
    JWT_ALGORITHM = 'HS256'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    CONNECTION_STRING = os.environ['DATABASE_URL']
    MAIL_SERVER=os.environ["MAIL_SERVER"]
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
    UPLOADS_DEFAULT_URL= os.environ["UPLOADS_DEFAULT_URL"]
    UPLOADED_IMAGES_DEST=os.environ["UPLOADS_DEFAULT_DEST"]
   
class DevelopmentConfig(Config):
    os.environ["FLASK_ENV"] = 'development'

    FLASK_DEBUG = 1
    DEBUG = True
class TestConfig(Config):
    os.environ["FLASK_ENV"] = 'testing'
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    CONNECTION_STRING = os.environ["TEST_DATABASE_URL"]


configs = dict(
    testing=TestConfig,
    production=Config,
    development=DevelopmentConfig
)
