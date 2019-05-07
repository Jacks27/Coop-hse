from app.v1.models import BaseModel,Boolean
class ServiceModel(BaseModel):
    water=Boolean()
    electricity=Boolean()
    roads=Boolean()
    table_name= "services"
    tbl_colomns = ['water', 'electricity', 'roads']