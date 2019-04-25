import random
import string
from instance.config import configs
import unittest
import json
from app.v1.db_setup import SetUpDb
from run import copApp

config_name = "testing"
db = SetUpDb(config_name)

class BaseTest(unittest.TestCase):
    
    def setUp(self):
        db.create_tables()
        copApp.config.from_object(configs["testing"])
        self.client = copApp.test_client
        self.token = ''

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

    def generate_random_user( self):
        return {
                "firstname":"jackson",
                "lastname":"kariuki",
                "othername":"karis",
                "email":"{}.ka@gmail.com".format(BaseTest.generate_name(6)),
                "phonenumber":"234454552{}".format(BaseTest.generate_number()),
                "passporturlstring":"https://www.xmicrosoft.com",
                "password": "jacks278"
            }

    def login(self):
        login_data = {
            "email":"34455677837",
            "password" : "jacks278"
            }
        return login_data
