from app.v1.models import BaseModel, String, Strpatt, SizedString, Integer, Float, SizedInteger

class ProductsModel(BaseModel):
    services_id = Integer()
    project_name = String()
    project_type = String()
    size = String()
    county = String()
    location = String()
    location_info = String()
    price = Float()
    other_information = String()
    image =Strpatt(pat=r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
    
class ProductBase(BaseModel):
    tbl_colomns = ["services_id", "project_name", "project_type", "size", "county",\
        "location", "location_info", "price", "other_information", "image" ]
    table_name= 'products'
class Checkservice(BaseModel):
    table_name= 'services'