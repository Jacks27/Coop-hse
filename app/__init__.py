"app/__init__.py"
from flask  import Flask, url_for
from app.v1.db_setup import SetUpDb
from instance.config import configs, Config
from flask_mail import Mail, Message
from app.v1 import my_v1
from itsdangerous import URLSafeTimedSerializer

app=Flask(__name__)
def create_app(config="development"):
    
    app.config.from_object(configs[config])
    db = SetUpDb(config)
    with app.app_context():
        db.create_tables()
    app.register_blueprint(my_v1, url_prefix='/app/v1')
    app.secret_key= Config.SECRET_KEY

    return app


def send_email(email):
    """this method is used to send email in all class and functions
    Arguments:
    email= email=[{list}] - alist of emails that will be sent to
    message = msg[{dict}] - a dict with link and a messae
    """
    s = URLSafeTimedSerializer(Config.SECRET_KEY)
    mail_token=s.dumps(email, salt='confirm_email')

    mail=Mail(app)
    msg=Message('Thank you for joining us', sender= Config.MAIL_USERNAME, recipients=[email])
    link = url_for('confirm_email', token=mail_token, _external= True )
    msg.body = "Click this link to confirm your account{}, please ignore if this is not intenede  for you".format(link)
    mail.send(msg)