import json
from tests.v1 import BaseTest

class TestProducts(BaseTest):
    services = {
            "water": True,
            "electricity": True,
            "roads": True
        }
    product1 = {	"services_id": 1,
	"project_name": "bluespring2a",
	 "project_type": "house",
	 "size": "1/8 acre", 
	 "county":"nairobi",
	 "location": "mwihoko",
	 "location_info":"roads and other stuffs",
	 "price":230000.00, 
	 "other_information": "bore holes have been sunk",
	 "image":"www.emaaail.com"
	
    }
    product2 = {	
    "services_id": 1,
	"project_name": "bluespring2a",
	 "project_type": "house",
	 "size": "1/8 acre", 
	 "county":"nairobi",
	 "location": "mwihoko",
	 "location_info":"roads and other stuffs",
	 "price":"230k000.00", 
	 "other_information": "bore holes have been sunk",
	 "image":"www.emaaail.com"
	
    }
    def test_addproduct(self):
        data = self.product1
        result= self.auth_request('app/v1/add_project', 'POST', data)
        print(json.loads(result.data))
        self.assertEqual(result.status_code, 201)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 201)

    def test_missingfields(self):
        data = self.product1
        del data['image']
        result= self.auth_request('app/v1/add_project', 'POST', data)
        print(json.loads(result.data))
        self.assertEqual(result.status_code, 400)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 400, True)
    def test_exsitingdbdata(self):
        data = self.product1
        result= self.auth_request('app/v1/add_project', 'POST', data)
        print(json.loads(result.data))
        self.assertEqual(result.status_code, 400)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 400, True)

    def test_intergevalue_fields(self):
        data = self.product2
        result= self.auth_request('app/v1/add_project', 'POST', data)
        print(json.loads(result.data))
        self.assertEqual(result.status_code, 400)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 400, True)
    def test_recover_password(self):
        data = self.product2
        result= self.auth_request('app/v1/add_project', 'POST', data)
        print(json.loads(result.data))
        self.assertEqual(result.status_code, 400)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 400, True)