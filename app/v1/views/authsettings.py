from app.v1.views import BaseView
from app.v1.models.auth_login import UserLogin,ForgotPass
from flask import make_response, abort, jsonify, request, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app.v1.views.auth import hash_password
from instance.config import Config
import app
from app.v1.models.auth_model import UsersModel

def change_password():
    """ function for changes
    Arguments {[new password, new password, confirm password]}
    retuns succes 200 or 404 if failed """
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
    fields=['email']
    BaseView.required_fields_check(fields, datadict)
    lm=UserLogin()
    email=dict(email=datadict['email'])
    lm.where(email)
    if lm.check_exist is True:
        app.send_email(dict(email=datadict['email'], msg='Click the link to recover you password',route='recover_account'))
     
        res = {'Message': 'Email was sent to your account please check',
                   'status': 200}
    else:
        res = {
        'error': "Could not find a account with that email. Please sign up",
        'status': 404
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
    app.Upload()
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