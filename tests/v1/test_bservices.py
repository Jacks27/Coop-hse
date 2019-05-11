import json
from tests.v1 import BaseTest

class TestServices(BaseTest):
        services = {
            "water": True,
            "electricity": True,
            "roads": True
        }
        def test_create_services(self):
                data=self.services
                result= self.auth_request('app/v1/create_service', 'POST', data)
                print(json.loads(result.data))
                self.assertEqual(result.status_code, 201)
                datacheck = json.loads(result.data)
                self.check_standard_reply(datacheck, 201)