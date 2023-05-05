from flask import Flask
from flask_restful import Api
from os import path
from flask_cors import CORS
from app.models import ADD

appli = None
api = None

#Creating application
def initiate_app():
    #Creating a Flask instance
    appli = Flask(__name__, template_folder="templates") 
    appli.config['SECRET_KEY'] = "21f1001069"

    #Adding datatbase
    appli.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addDB.sqlite3'
    appli.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Initalizing database
    ADD.init_app(appli)
    #Initalizing API
    api = Api(appli)
    appli.app_context().push() 
    CORS(appli)
    
    #Calling fun to create database
    initiate_DB(appli)
    return appli, api

#Creating database
def initiate_DB(app):
    if path.exists('/addDB.sqlite3') == False:
        ADD.create_all(app=app)
    return True


# --------------------------------------------------
apple, api = initiate_app()
# Calling fun to create application

# Import all the controllers so they are loaded
from app.app import *

# from app import initiate_app
from app.api import CustomerAPI, CustomerOUT, ListAPI, CardAPI

api.add_resource(CustomerAPI, "/api/customer/register", "/api/customer/login")
api.add_resource(CustomerOUT, "/api/customer/logout")
api.add_resource(ListAPI, "/api/list/create", "/api/list/<list_name>/edit", "/api/list/<list_name>/delete")
api.add_resource(CardAPI, "/api/card/<list_name>/create", "/api/card/<list_name>/<card_name>/delete", \
                            "/api/card/<list_name>/<card_name>/edit", "/api/card/<list_name>/<card_name>")


# Running the application
if __name__ == '__main__':
    apple.run(debug=True)
