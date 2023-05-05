from flask_sqlalchemy import SQLAlchemy
# from .database import ADD
ADD = SQLAlchemy()
#Creating Models
class Customer(ADD.Model):
    Customer_id = ADD.Column(ADD.Integer, primary_key = True, autoincrement = True)
    Customer_name = ADD.Column(ADD.String(30), nullable = False)
    Customer_email = ADD.Column(ADD.String(100), nullable = False, unique = True)
    Customer_pass = ADD.Column(ADD.String(15), nullable = False)
    lists = ADD.relationship("List", backref="custom")

class List(ADD.Model):
    List_id = ADD.Column(ADD.Integer, primary_key = True, autoincrement = True)
    List_name = ADD.Column(ADD.String(20), nullable = False)
    List_desc = ADD.Column(ADD.String(100), nullable = False)
    Customerl_id = ADD.Column(ADD.Integer, ADD.ForeignKey("customer.Customer_id"), nullable = False)
    cards = ADD.relationship("Card", backref="task")

class Card(ADD.Model):
    Card_id = ADD.Column(ADD.Integer, primary_key = True, autoincrement = True) 
    Card_list = ADD.Column(ADD.String(20), nullable = False)
    Card_title = ADD.Column(ADD.String(20), nullable = False)
    Card_content = ADD.Column(ADD.String(200), nullable = False)
    #card deadline status : 
    Card_status = ADD.Column(ADD.String(30), nullable = False)
    Card_dline = ADD.Column(ADD.String(12), nullable = False)
    Listc_id = ADD.Column(ADD.Integer, ADD.ForeignKey("list.List_id"), nullable = False)