import datetime
import hashlib
from flask import make_response, abort, jsonify, request
from app.v1.models.auth_model import UsersModel
from app.v1.models.auth_login import UserLogin
from app.v1.views.validate import Validate
from app.v1.views import BaseView
from instance.config import Config
from app.v1.models import BaseModel
import jwt

def signup():
    """create useer account  """
    datadict = BaseView.get_jsondata()
    fields=["firstname", "lastname", "othername", "phonenumber", "email" \
        , "passporturlstring", "password"]
    
    BaseView.required_fields_check(fields, datadict)

    firstname, lastname, othername, phonenumber, email, passporturlstring, password =\
    [val for val in datadict.values()]

    
    UM=UsersModel(firstname, lastname, othername,\
        phonenumber, email, passporturlstring, password)

    hashedpass=hash_password(password)
    

    id = UM.insert_data(UM.firstname, UM.lastname, UM.othername,\
    UM.phonenumber, UM.email, UM.passporturlstring, hashedpass)
    
    res  = jsonify({"status": 201, 'data': id})
    return  make_response(res, 201)

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
    print("user______________>id",lm.id) 
    if lm.check_exist() is True and lm.id is not None:
        hashpassword= hash_password(datadict['password'])
        if lm.password==hashpassword:
            payload = lm.sub_set()
            payload.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)})
            token = jwt_encode(payload)
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