
import datetime
import hashlib
from flask import make_response, abort, jsonify, request, abort, session, url_for
from app.v1.models.auth_model import UsersModel
from app.v1.models.auth_login import UserLogin
from app.v1.views.validate import Validate
from app.v1.views import BaseView
from instance.config import Config
from app.v1.models import BaseModel
import jwt
from functools import wraps, partial
from flask_mail import Message
from app import send_email



def auth_admin(func):
    """Auth  checking Jwt token in the request for admin routes

    Arguments:
        func {[type]} -- The function to authenticate

    Returns:
        [error] -- [Incase token is invalid]
        returns the function for success
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        request.user = None

        token = request.headers.get('authorization', None)

        if token:
            if token.startswith('Bearer '):
                token = token.replace('Bearer ', '')
            secret = Config.SECRET_KEY
            algo = Config.JWT_ALGORITHM
            try:
                payload = jwt.decode(token, secret, algo)
                isadmin = payload.get('isadmin', False)
                if isadmin is True:
                    request.user = payload
                    return func(*args, **kwargs)
            except (jwt.DecodeError):
                pass
        return abort(make_response(jsonify(
            {"status": 400,
                'error': "You are not authorized to perform this action"}),
            400))

    return func_wrapper
"""@auth_admin"""
def signup():
    """create useer account  """
    datadict = BaseView.get_jsondata()
    fields=["firstname", "lastname", "othername", "email","phonenumber"\
        , "passporturlstring", "password"]
    Error= ()
    BaseView.required_fields_check(fields, datadict)
    lm=UserLogin()  
    firstname, lastname, othername, phonenumber, email, passporturlstring, password =\
    [val for val in datadict.values()]

    
    UM=UsersModel(firstname, lastname, othername,\
        phonenumber, email, passporturlstring, password)
    lm.where(dict(email=datadict['email']))
    if lm.check_exist() is True:
        Error+=("Account with the following {} email exists".format(datadict['email']),)
    
    lm.where(dict(phonenumber=datadict['phonenumber']))
    if lm.check_exist() is True:
        Error+=("Account with the following {} phone number exists".format(datadict['phonenumber']),)
    
    
    
    
    if len(Error)> 0:
        res = jsonify({'error': ",".join(Error), 'status': 400})
        return abort(make_response(res, 400))

    hashedpass=hash_password(password)
    UM.insert_data(UM.firstname, UM.lastname, UM.othername,\
    UM.email, UM.phonenumber, UM.passporturlstring, hashedpass)
    userdetails=UM.sub_set()
    token=''
    if UM.id is not None:
        token=jwt_encode(userdetails)
        session['email']=email
        send_email(email)#send confirmation link
        data = {'user': userdetails, 'token': token}
        res  = jsonify({"status": 201, 'data': data})
        return make_response(res, 201)
    return  make_response(jsonify({"Errro": 'Oops somthing went wrong'}), 500)

def hash_password(password):
    """ password hashing

    Arguments:dd
        password {[str]} -- [the string to Hash]

    Returns:
        [str] -- [the hashed password]
    """

    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest() 

def login():
    datadict = BaseView.get_jsondata()
    fields =["email", "password"]
    lm=UserLogin()
    BaseView.required_fields_check(fields, datadict)
    lm.where(dict(email=datadict['email']))
    if lm.check_exist() is True and lm.id is not None:
        hashpassword= hash_password(datadict['password'])
        if lm.password==hashpassword:
            payload = lm.sub_set()
            payload.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)})
            token = jwt_encode(payload)
            session['email']= datadict['email']
            res = {'data': {'token': token, 'user': payload
                            },
                   'status': 200}
        else:
            res = res = {
                'error': "Wrong emai/password combination. Please try again",
                'status': 400
            }
        return make_response(jsonify(res), res['status'])
    res = {
        'error': "Could not find a account with that email. Pleas sign up",
        'status': 400
    }
    return make_response(jsonify(res), res['status'])

def jwt_encode(payload):
    """For creating Jwt Tokens

    Arguments:
        payload {[dict]} -- [key:value]

    """

    secret = Config.SECRET_KEY
    algo = Config.JWT_ALGORITHM
    token = jwt.encode(payload, secret, algo)
    return token.decode('UTF-8')

def make_SU(user_id):
    
    lm=UserLogin()
    if lm.where(dict(id=user_id)) is True and lm.id is not None:
        lm.update(dict(isAdmin=True), user_id)
        res = {'status': 202, 'data':lm.sub_set}
    else:
        msg = "User not found"
        res={"status": 404, 'error':msg}
    return make_response(jsonify({res}, res['status']))

def get_users():
    lm=UserLogin()
    select_cols= lm.tbl_colomns
    lm.select(select_cols)
    Users=lm.get(False)
    res = jsonify({"status": 200,
                   'data': Users
                   })
    return make_response(res, 200)

def change_password():
    datadict=BaseView.get_jsondata()
    lm=UserLogin()
    fields=['password', 'confirmpassword','newpassword']
    BaseView.required_fields_check(fields, datadict)
    email = session['email']
    hashedpas=hash_password(datadict['password'])
    if lm.where(dict(email=email))is True and lm.id is not None:
        if lm.password==hashedpas:
            newpass=hash_password(datadict['newpassword'])
            lm.update(dict(password=newpass), lm.id)
        res = {'status': 202, 'data':lm.sub_set}
    else:
        msg = "wrong password try again"
        res={"status": 404, 'error':msg}
    return make_response(jsonify({res}, res['status']))
def recover_password():
    pass

def confirm_email(token):
   pass
