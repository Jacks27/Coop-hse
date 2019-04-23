"app/__init__.py"
from flask  import Flask
from app.v1.db_setup import SetUpDb
from instance.config import configs
from app.v1 import my_v1

def create_app(config="development"):
    app=Flask(__name__)
    app.config.from_object(configs[config])
    db = SetUpDb(config)
    with app.app_context():
        db.create_tables()
    app.register_blueprint(my_v1, url_prefix='/app/v1')
    
    return app
