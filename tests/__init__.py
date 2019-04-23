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
    
    def SetUp(self):
        db.create_tables()
        copApp.config.from_object(configs["testing"])
        self.client= copApp.test_client
        self.token = ''