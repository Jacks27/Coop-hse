from app.v1.models import BaseModel, String, Strpatt, SizedString, SizedInteger

class UserLogin(BaseModel):
    table_name= "users"
class ForgotPass(BaseModel):
    table_name= "users"
    password=SizedString(minlen=8)
def __init__():
    return super().__init__()