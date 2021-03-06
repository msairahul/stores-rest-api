import os

from flask import Flask
from security import authenticate, identity
from flask_restful import Api
#from flask_jwt import JWT,jwt_required

from resources.item import Item,ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='rahul'
api = Api(app)

if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

#jwt = JWT(app, authenticate, identity)     # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items') 
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')

if __name__=="__main__":
    from db import db
    db.init_app(app)
    app.run(port=5050, debug=True)
        