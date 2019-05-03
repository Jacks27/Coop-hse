from app.v1.models import BaseModel, String, Strpatt, SizedString, Float, SizedInteger

class Products(BaseModel):

    project_name = String()  
    project_type = String()  
    size = String()             
    county = String()           
    location = String()         
    location_info = String()    
    price = Float()       
    other_information = String(
    image   