import json
from tests.v1 import BaseTest

class TestAuth(BaseTest):

    def test_signup(self):
        data = self.generate_random_user()
        result = self.auth_request('/app/v1/signup', 'POST', data)
        print(json.loads(result.data))
        self.assertEqual(result.status_code, 201)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 201)

    def test_login(self):
        data=self.login()
        result= self.auth_request('app/v1/login', 'POST', data)
        print(json.loads(result.data))
        self.assertEqual(result.status_code, 200)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 200)
    def test_login_wrong_data(self):
        rawdata=self.generate_random_user()
        data={'email':rawdata['email'], 'password':rawdata['password']}
        result= self.auth_request('app/v1/login', 'POST', data)
        print(json.loads(result.data))
        datacheck2 = json.loads(result.data)
        self.check_standard_reply(datacheck2, 400, True)
    def test_make_admin(self):
        data=   {
        "email": "hubuhutusa@royalmarket.online"
        }
        result = self.auth_request('app/v1/create_admin', 'PATCH', data)
        self.assertEqual(result.status_code, 201)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 201, False)
    def test_forgot_password(self):
        data = {
            "email": "hubduhutusa@royalmarket.online"
            }
        result = self.auth_request('app/v1/forgot_password', 'POST', data)
        self.assertEqual(result.status_code, 400)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 400, True)

    def test_recover_password(self):
        data = {
        "password":"1234567890",
        "confirmpassword":"1234567890"
        }
        result = self.auth_request('app/v1/recover_account/Imh1YnVodXR1c2FAcm95YWxtYXJrZXQub25saW5lIg.XMouRw.81GP9i44qBDxdZr8TzInSLSVe5w/hubuhutusa%40royalmarket.online', 'POST', data)
        self.assertEqual(result.status_code, 403)
        datacheck = json.loads(result.data)
        self.check_standard_reply(datacheck, 403, True)
        
        


