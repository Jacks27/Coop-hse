import json
from tests.v1 import BaseTest

class TestAuth(BaseTest):

    def test_signup(self):
        data = self.generate_random_user()
        result= self.auth_request('app/v1/signup', 'POST', data)
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

