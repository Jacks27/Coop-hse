from app.v1.models import BaseModel, String, Strpatt, SizedString

class UsersModel(BaseModel):
    """User model""" 
    firstname = Strpatt(pat='[-a-zA-Z]+$')
    lastname = Strpatt(pat='[-a-zA-Z]+$')
    othername = Strpatt(pat='[-a-zA-Z]+$')
    email = Strpatt(pat=r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    phonenumber = SizedString(minlen=10)
    psnumber = SizedString(minlen=8)
    password = SizedString(minlen=8)
    tbl_colomns = ["firstname","lastname","othername","email","phonenumber","psnumber","password","isadmin"]
    table_name = 'users'
