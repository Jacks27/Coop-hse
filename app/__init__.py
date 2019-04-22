"app/__init__.py"
from flask  import Flask
from app.v1.db_setup import SetUpDb
from instance.config import configs

def create_app(config="development"):
    app=Flask(__name__)
    app.config.from_object(configs[config])
    db = SetUpDb(config)
    with app.app_context():
        db.create_tables()
    
    return app
