
import datetime
import hashlib
from flask import make_response, abort, jsonify, request, session
from app.v1.models.auth_model import UsersModel
from app.v1.models.auth_login import UserLogin,ForgotPass
from app.v1.views.validate import CheckEmail, CheckInteger
from app.v1.views import BaseView
import jwt
from instance.config import Config
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import app




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
                payload = jwt.decode(token, secret, algorithms=algo)
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

def signup():
    """create useer account  """
    datadict = BaseView.get_jsondata()
    fields=["firstname", "lastname", "othername", "email","phonenumber"\
        , "psnumber", "password"]
    Error= ()
    BaseView.required_fields_check(fields, datadict)
    lm=UserLogin()
    firstname, lastname, othername, phonenumber, email, psnumber, password =\
    [val for val in datadict.values()]

    
    UM=UsersModel(firstname, lastname, othername,\
        phonenumber, email, psnumber, password)
    lm.where(dict(email=datadict['email']))
    if lm.check_exist() is True:
        Error+=("Account with the following {} email exists".format(datadict['email']),)
    
    lm.where(dict(phonenumber=datadict['phonenumber']))
    if lm.check_exist() is True:
        Error+=("Account with the following {} phone number exists".format(datadict['phonenumber']),)
    
    lm.where(dict(phonenumber=datadict['psnumber']))
    if lm.check_exist() is True:
        Error+=("Account with the following {}number exists".format(datadict['psnumber']),)
    if len(Error)> 0:
        res = jsonify({'error': ",".join(Error), 'status': 400})
        return abort(make_response(res, 400))

    hashedpass=hash_password(password)
    UM.insert_data(UM.firstname, UM.lastname, UM.othername,\
    UM.email, UM.phonenumber, UM.psnumber, hashedpass, False)
    userdetails=UM.sub_set()
    token=''
    if userdetails['id'] is not None:
        token=jwt_encode(userdetails)
        session['email']=UM.email
        message="please click  the then link to activate your account"
        app.send_email(dict(email=UM.email,msg=message, route='confirm_email' ))#send confirmation link email_dict [{ dictionary with email message ,route}]"""
        data = {'user': userdetails, 'token': token}
        res  = jsonify({"status": 201, 'data': data})
        return make_response(res, 201)
    return  make_response(jsonify({"Error": 'Oops something went wrong'}), 500)

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
    if lm.get() is not None:
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
            res = {
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
@auth_admin
def make_admin():
    datadict=BaseView.get_jsondata()
    fields=['email']
    BaseView.required_fields_check(fields, datadict)
    CE=CheckEmail(datadict['email'])
    lm=UserLogin()
    lm.where(dict(email=CE.email))
    if lm.check_exist() is True:
        lm.update(dict(isAdmin=True), lm.id)
        res = {'status': 201,
        'data': {'message':'User have been granted admin rights' ,
        'user':{'id':lm.id}
         }
         }
    else:
        msg = "User not found"
        res={"status": 404, 'error':msg}
    return make_response(jsonify(res), res['status'])
@auth_admin
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
    fields=['password', 'newpassword', 'confirmpassword']
    BaseView.required_fields_check(fields, datadict)
    email=session['email']
    lm.where(dict(email=email))
    fg=ForgotPass(datadict['newpassword'])
    if lm.get() is not  None and lm.id is not None:
        hashedpas=hash_password(datadict['password'])
        if lm.password==hashedpas:
            newpass=hash_password(fg.password)
            lm.update(dict(password = newpass), lm.id)
            res = {'status': 202, 'message': "password updated successfuly"}
        else:
            msg = "wrong password try again"
            res={"status": 404, 'error':msg }
    else:
        msg = "Something went wrong, login and try again"
        res={"status": 404, 'error':msg}
    return make_response(jsonify(res), res['status'])

def forgot_password():
    datadict=BaseView.get_jsondata()
    session['email']= datadict['email']
    fields=['email']
    BaseView.required_fields_check(fields, datadict)
    lm=UserLogin()
    email=dict(email=datadict['email'])
    lm.where(email)
    if lm.get() is not  None and lm.id is not None:
        app.send_email(dict(email=datadict['email'], msg='Click the link to recover you password',route='recover_account'))
     
        res = {'Message': 'Email was sent to your account please check',
                   'status': 200}
    else:
        res = {
        'error': "Could not find a account with that email. Please sign up",
        'status': 400
        }
    return make_response(jsonify(res), res['status'])



def recover_account(token, email):
    datadict=BaseView.get_jsondata()
    fields=['password', 'confirmpassword']
    BaseView.required_fields_check(fields, datadict)
    res={}
    msg=''
    s = URLSafeTimedSerializer(Config.SECRET_KEY)
    lm=UserLogin()
    lm.where(dict(email=email))
    if lm.get() is not  None and lm.id is not None:
        newpass=hash_password(datadict['confirmpassword'])
        lm.update(dict(password=newpass), lm.id)
        res = {'status': 202, 'message': "Passwrd was reset successfuly"}
    else:
        msg = "Something went wrong, login and try again"
        res={"status": 404, 'error':msg}

    try:
        
        s.loads(token, salt='confirm_email', max_age=86400)
        
    except SignatureExpired:
        msg = "Activation link has expired , please reset your account"
        res={'status': 403, 'error':msg}
    return make_response(jsonify(res), res['status'])


def confirm_email(token, email):
    res={}
    msg=''
    s = URLSafeTimedSerializer(Config.SECRET_KEY)
    lm=UserLogin()
    
    lm.where(dict(email=email))
    if lm.get() is not  None and lm.id is not None:
        lm.update(dict(active=True), lm.id)
        res = {'status': 202, 'message': "Account is now activated"}
    else:
        msg = "Could not find account with this {} email".format(email)
        res={"status": 400, 'error':msg}

    try:
        
        s.loads(token, salt='confirm_email', max_age=86400)
        
    except SignatureExpired:
        msg = "Activation link has expired , please reset your account"
        
    return make_response(jsonify(res), res['status'])
    
def user_update_info():
    """Updates User information account
    Update [{firstname, lastname, otherbane, phonenumber, Pfnumber}]
    """
    datadict = BaseView.get_jsondata()
   
    fields_updates=["id", "firstname", "lastname", "othername", "email","phonenumber"\
        , "psnumber", "password"]
    BaseView.required_fields_check(fields_updates, datadict)
    lm=UserLogin()
    Error= ()
    userid ,firstname, lastname, othername,email, phonenumber, psnumber, password =\
    [val for val in datadict.values()]
   
    
    if session.get('email') != datadict['email']:
            Error+=(" Could not perform this action",)
        
    if len(Error)> 0:
        res = jsonify({'error': ",".join(Error), 'status': 403})
        return abort(make_response(res, 403))

    lm.where(dict(email=datadict['email']))
    id=datadict['id']
    if lm.check_exist() is True and userid==lm.id:
        BaseView.required_fields_check(fields_updates, datadict)

        UsersModel(firstname, lastname, othername,\
            email, phonenumber, psnumber, password)

        lm.update(dict(firstname = firstname,lastname=lastname,thername=othername,\
            phonenumber=phonenumber,psnumber=psnumber, 
            ), id)
        msg= "Information updated successfuly"
        res={"status": 200, 'Error':msg }
    else:
        msg="Sorry could not Update your details contact the Admin"
        res={"status": 401, 'Error':msg }
    return make_response(jsonify(res), res['status'])