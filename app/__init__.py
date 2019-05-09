"app/__init__.py"
import os
from flask  import Flask, url_for
from app.v1.db_setup import SetUpDb
from instance.config import configs, Config
from flask_mail import Mail, Message
from app.v1 import my_v1
from app.v1.models.auth_login import UserLogin
from app.v1.models.auth_model import UsersModel
from itsdangerous import URLSafeTimedSerializer
from app.v1.views.auth import hash_password


def create_app(config="development"):
    app=Flask(__name__)
    app.config.from_object(configs[config])
    db = SetUpDb(config)
    with app.app_context():
        db.create_tables()
        create_default_admin()
        
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
    msg.body = "Click this link {}, please ignore you did not request this service".format(link)
    mail.send(msg)

def create_default_admin():
    """ Create a default admin for the app"""
  
    firstname = os.getenv('ADMIN_FIRST_NAME')
    lastname = os.getenv('ADMIN_LAST_NAME')
    othername = os.getenv('ADMIN_OTHERNAME')
    email = os.getenv('ADMIN_EMAIL')
    phonenumber = os.getenv('ADMIN_PHONENUMBER')
    psnumber = os.getenv('ADMIN_PSNUMBER')
    password = os.getenv('ADMIN_PASSWORD')
    Error=()
    lm=UserLogin()
    lm.where(dict(email=email))
    if lm.check_exist() is True and psnumber is not None:
        Error+=("Account with the following {}number exists".format(email),)
    else:
        UM=UsersModel(firstname, lastname, othername,\
        email, phonenumber, psnumber, password)
        hashedpass=hash_password(password)
        UM.insert_data(UM.firstname, UM.lastname, UM.othername,\
        UM.email, UM.phonenumber,UM.psnumber , hashedpass)
        