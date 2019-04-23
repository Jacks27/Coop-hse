
import hashlib
from flask import make_response, abort, jsonify, request
from app.v1.models.auth_model import UsersModel
from app.v1.views.validate import Validate
from app.v1.views import BaseView


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

    BaseView.required_fields_check(fields, datadict)