"app/__init__.py"
from flask  import Flask, url_for
from app.v1.db_setup import SetUpDb
from instance.config import configs, Config
from flask_mail import Mail, Message
from app.v1 import my_v1
from itsdangerous import URLSafeTimedSerializer


def create_app(config="development"):
    app=Flask(__name__)
    app.config.from_object(configs[config])
    db = SetUpDb(config)
    with app.app_context():
        db.create_tables()
    app.register_blueprint(my_v1, url_prefix='/app/v1')
    app.secret_key= Config.SECRET_KEY

    return app


def send_email(email_dict={}):
    """this method is used to send email in all class and functions
    Arguments:
   email_dict [{ dictionary with email message ,route}]
    """
    
    s = URLSafeTimedSerializer(Config.SECRET_KEY)
    
    token=s.dumps(email_dict['email'], salt='confirm_email')
    app = create_app()
    mail=Mail(app)
    msg=Message('Hey ,{}'.format(email_dict['msg']), sender= Config.MAIL_USERNAME, recipients=[email_dict['email']])
    link = url_for('my_v1.{}'.format(email_dict['route']), token=token, email= email_dict['email'], _external= True)
    msg.body = "Click this link {}, please ignore if this is not intended for you".format(link)
    mail.send(msg)