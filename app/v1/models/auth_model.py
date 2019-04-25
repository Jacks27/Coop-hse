from app.v1.models import BaseModel, String, Strpatt, SizedString, Integer, SizedInteger

class UsersModel(BaseModel):
    """ User model """ 
    
    firstname = Strpatt(pat='[-a-zA-Z]+$')
    lastname = Strpatt(pat='[-a-zA-Z]+$')
    othername = Strpatt(pat='[-a-zA-Z]+$') 
    email = Strpatt(pat=r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    phonenumber = SizedString(minlen=10)
    passporturlstring = Strpatt(\
    pat=r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
    password = SizedString(minlen=8)
    tbl_colomns = ["firstname", "lastname", "othername", "email", "phonenumber", "passporturlstring", "password"] 
    table_name = 'users'
