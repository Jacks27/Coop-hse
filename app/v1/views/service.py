from app.v1.models.servicesmodel import ServiceModel
from app.v1.views import BaseView
from flask import make_response, abort, jsonify, request, abort, session, url_for

def createservice():
    """create services  """
    datadict = BaseView.get_jsondata()
    print("datadict---------------", datadict)
    servicefields=[ "water" ,"electricity", "roads"]
    BaseView.required_fields_check(servicefields, datadict)
    water, electricity, roads=[val for val in datadict.values()]

    
    sm=ServiceModel(water, electricity, roads)

    sm.insert_data(water, electricity, roads)
    serviceid=sm.sub_set()

    if sm.id is not None:
        
        data = {'Item': serviceid, 'msg':"Item was added successfully"}
        res  = jsonify({"status": 201, 'data': data})
        return make_response(res, 201)
    return  make_response(jsonify({"Errro": 'Oops somthing went wrong'}), 500)
