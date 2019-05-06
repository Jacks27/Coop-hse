from app.v1.views import BaseView
from app.v1.models import BaseModel
from app.v1.models.products import ProductBase, ProductsModel
from flask import make_response, abort, jsonify, request, abort, session, url_for

def createproduct():
    """create product  """
    datadict = BaseView.get_jsondata()
    print("datadict---------------", datadict)
    fields=[ "services_id" ,"project_name", "project_type", "size", "county", "location",\
         "location_info", "price", "other_information", "image" ]
    Error= ()
    BaseView.required_fields_check(fields, datadict)
    services_id, project_name, project_type, size, county, location,\
        location_info, price, other_information, image =[val for val in datadict.values()]

    
    pm=ProductsModel(services_id, project_name, project_type, size, \
        county, location, location_info,price, other_information,\
    image)
    pb=ProductBase()
    pb.where(dict(project_name=datadict['project_name']))
    if pb.check_exist() is True:
        Error+=("Project with the following {} name exists".format(datadict['project_name']),)
    
    pb.where(dict(image=datadict['image']))
    if pb.check_exist() is True:
        Error+=("Image with the following {} details exists".format(datadict['image']),)
    
    
    
    
    if len(Error)> 0:
        res = jsonify({'error': ",".join(Error), 'status': 400})
        return abort(make_response(res, 400))
    pb.insert_data(datadict['services_id'], pm.project_name, pm.project_type, pm.size, pm.county, pm.location, pm.location_info,\
        pm.price, pm.other_information, image)
    userdetails=pb.sub_set()

    if pb.id is not None:
        
        data = {'Item': userdetails, 'msg':"Item was added successfully"}
        res  = jsonify({"status": 201, 'data': data})
        return make_response(res, 201)
    return  make_response(jsonify({"Errro": 'Oops somthing went wrong'}), 500)

def get_products():
    """gets alist of all the products in the database
    Returns:
    Api responce with all the products

    """
    pb=ProductBase()
    select_cols= pb.tbl_colomns
    pb.select(select_cols)
    products =pb.get(False)
    res = jsonify({"status": 200,
                   'data': products
                   })
    return make_response(res, 200)
def update_product():
    """ Update data of a given id
    Returns:
    Api respons of row edited
    """
    datadict = BaseView.get_jsondata()
    print("datadict---------------", datadict)
    fields=["services_id" ,"project_name", "project_type", "size", "county", "location",\
         "location_info", "price", "other_information", "image" ]
    Id= datadict['id']
    del datadict['id']
    Error= ()
    BaseView.required_fields_check(fields, datadict)
    services_id, project_name, project_type, size, county, location,\
        location_info, price, other_information, image =[val for val in datadict.values()]

    
    ProductsModel(services_id, project_name, project_type, size, \
        county, location, location_info,price, other_information,\
    image)
    pb=ProductBase()
    pb.where(dict(id=Id) )
    if pb.check_exist() is False:
        Error+=("Could not find data with Id {}".format(datadict['id']),)
    if isinstance(Id, int) is False:
        Error+=("Id must be an integer")
    if len(Error)> 0:
        res = jsonify({'error': ",".join(Error), 'status': 400})
        return abort(make_response(res, 400))

 
    pb.update(dict(
        services_id = services_id, 
        project_name=project_name,
        project_type=project_type,
        size=size, 
        county=county,
        location= location,
        location_info=location_info,
        price=price,
        other_information= datadict['other_information'],\
        image=image
        ), Id)

    productdetails=pb.sub_set()

    if pb.id is not None:
        
        data = {'Item': productdetails, 'msg':"Item was Updated successfully"}
        res  = jsonify({"status": 201, 'data': data})
        return make_response(res, 201)
    return  make_response(jsonify({"Errro": 'Oops somthing went wrong'}), 500)

def productdetail(product_id):
    pb=ProductBase()
    productexist=pb.get_one(product_id)
    if productexist is not None:
        res = {'status': 200, 'data': productexist}
    else:
        res = {"status": 404,
                'error': "Product with id {} not found".format(product_id)
                }

    return make_response(jsonify(res), res['status'])

def deleteproduct(product_id):
    pb=ProductBase()
    productexist=pb.get_one(product_id)
    if productexist is not None:
        pb.delete(product_id)
        res = {'status': 200,
                   'data': {'message': "Product deleted successfully"}
                   }
    else:
        res = {"status": 404,
                   'error': "Product with id {} not found".format(product_id)}
    return make_response(jsonify(res), res['status'])

def checked_soldout(product_id):
    Id=product_id
    Error= ()
    pb=ProductBase()
    pb.where(dict(id=Id))
    if pb.check_exist() is False:
        Error +=("Could not find data with Id {}".format(Id),)
    if isinstance(Id, int) is False:
        Error+=("Id must be an integer")
    if len(Error)> 0:
        res = jsonify({'error': ",".join(Error), 'status': 400})
        return abort(make_response(res, 400))
    pb.update(dict(sold_out=True), product_id)

    productdetails=pb.sub_set()
    if pb.id is not None:
        
        data = {'Item': productdetails, 'msg':"Item was Updated successfully"}
        res  = jsonify({"status": 201, 'data': data})
        return make_response(res, 201)
    return  make_response(jsonify({"Errro": 'Oops somthing went wrong'}), 500)









