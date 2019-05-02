from app.v1.models import BaseModel, String, Strpatt, SizedString, Integer, SizedInteger

class UserLogin(BaseModel):
    table_name= "users"
class ForgotPass():
    password=SizedString(minlen=8)
