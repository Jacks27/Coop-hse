import random
import string
from instance.config import configs
import unittest
import json
from app import create_default_admin
from app.v1.db_setup import SetUpDb
from run import copApp


db = SetUpDb(config_name='testing')

class BaseTest(unittest.TestCase):
    
    def setUp(self):
        
        db.create_tables()
        copApp.config.from_object(configs["testing"])
        self.client = copApp.test_client
        self.token = ''
        create_default_admin()
        self.login()

    def post(self, path, data):
        result =self.auth_request(path, 'POST', data)
        return result

        
    def auth_request(self, Url, methods, data={}):
        return self.client().open(Url,  method=methods,
         headers={'Authorization':"Bearer"+ self.token},
         data=json.dumps(data))

    def check_standard_reply(self, datacheck, status, error=False):
        self.assertTrue('status' in datacheck)
        if not error:
            self.assertTrue('data' in datacheck)
        else:
            self.assertTrue('error' in datacheck )
    @staticmethod
    def generate_name(strLen=10):
        letters= string.ascii_letters
        return''.join(random.choice(letters) for i in range(strLen))
    @staticmethod
    def generate_number():
        return random.randint(0, 19)
    
   

    @staticmethod
    def generate_admin():
        admin_data = {
            "email":"lilu@quickmail.rocks"
        }
        return admin_data

    def generate_random_user( self):
        return {
                "firstname":"jackson",
                "lastname":"kariuki",
                "othername":"karis",
                "email":"{}.ka@gmail.com".format(BaseTest.generate_name(6)),
                "phonenumber":"256056456552{}".format(BaseTest.generate_number()),
                "psnumber":"https://www.xmicrosoft.com",
                "password": "jacks278"
            }
    
        
    def login(self):
        login_data = {
            "email":"lilu@quickmail.rocks",
            "password" : "jacks278"
            }
        result2 = self.auth_request(
            '/app/v1/login', 'POST', login_data)
       
        data = json.loads(result2.data)
        
        if data['data']['token']:
            self.token = data['data']['token']
        print('______', self.token)
        return login_data
        
    def tearDown(self):
        db.drop_tables()
