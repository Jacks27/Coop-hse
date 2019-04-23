from flask import jsonify, make_response, abort, request
from app.v1.views.validate import Validate
class  BaseView(Validate):
    errors = []
    @staticmethod
    def get_jsondata():
        if request.is_json:
            data= request.get_json()
        else:
            data = request.form.to_dict()
        if not data:
            try:
                data = request.get_json(force=True)
            except Exception as e:
                data = {}
                BaseView.errors.append(e)
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()

            data[key] = value

        return data

    @classmethod
    def required_fields_check(cls, fields=[], datadict={}):
        """ Check all required fields in submited data
        uses validate class
        Arguments :
        Args [fields] expected fields in a list
        kwargs{dataDict} expected dict from submited data

        Retuens:
        A [bool] if all the fields exists
        a [http exit] if any field is missing        
        """
        validRequired = cls.required(data_fields=fields, dataDict=datadict)
        if validRequired['status'] is False:
            msg = validRequired['res']
            res = jsonify({'status':400, 'error': msg})
            return abort(make_response(res, 400))
        
   
    
