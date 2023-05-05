# ==================================================== Imports ===================================================
from flask import make_response, request
from flask_restful import fields, marshal_with, reqparse
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from .models import Customer, List, Card, ADD
from datetime import date
import json

# ============================================ Custom Session ========================================================
Csession = dict()
td = str(date.today())

# ============================================ Error Code Dict =======================================================
errord = {
 	"CE1" : ('CUSTE001', 'Customer Name is required and should be string having length less than 31.'),
	"CE2" : ('CUSTE002', 'A valid Email is required and should be string having length less than 101.'),
	"CE3" : ('CUSTE003', 'A valid Password is required and should be string having length between 5 to 16.'),
	"CE4" : ('CUSTE004', 'Email already exist. Please try with a different Email.'),
    "CE5" : ('CUSTE005', 'Incorrect Password.'),
 	"CE6" : ('CUSTE006', 'Customer login is required, please login to continue.'),

	"LE1" : ('LIST001',	'A valid List name required and should be String having length less than 20.'),
	"LE2" : ('LIST002',	'A valid List description is required and should be String having length less than 100.'),
	"LE3" : ('LIST003',	'List name already exist, try with a different name.'),
    "LE4" : ('LIST004',	'The list you want to edit does not exist.'),
    "LE5" : ('LIST004',	'The list you want to delete does not exist.'),

	"DE1" : ('CARD001',	'A valid Card name required and should be String having length less than 20.'),
	"DE2" : ('CARD002',	'A valid Card description is required and should be String having length less than 200.'),
	"DE3" : ('CARD003',	'Card name already exist, try with a different name.'),
    "DE4" : ('CARD004', 'A valid Card Deadline is required.'),
    "DE5" : ('CARD005', 'A valid Card status [Pending, Completed, Failed to complete] is required.'),
    "DE6" : ('CARD006',	'The list in which you want to move the card not found.'),
    "DE7" : ('CARD007',	'Card not found.'),
    "DE8" : ('CARD008',	'List not found.')
}

# ============================================ Customer Error Class ==================================================

class CustomerNotFound(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class CustomerNotIn(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class EmailExist(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class IncorrectPassword(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class InvalidPassword(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class InvalidEmail(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class InvalidName(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class InvalidListInfo(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class InvalidCardInfo(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})

class NameExist(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})       

class NotFound(HTTPException):
    def __init__(self, status_code, error_code, error_msg):
        message = {"error_code": error_code, "error_message": error_msg}
        self.response = make_response(json.dumps(message), status_code, {"Content-Type": "application/json"})   

class ListNotFound(HTTPException):
    def __init__(self, status_code, error_msg):
        self.response = make_response(error_msg, status_code)  

# ============================================ Customer API ==========================================================
customer_register_out = {
    "Customer_id": fields.Integer,
    "Customer_name": fields.String,
    "Customer_email": fields.String,
    "Customer_pass": fields.String,
}

register_user_parser = reqparse.RequestParser()
register_user_parser.add_argument("name")
register_user_parser.add_argument("email")
register_user_parser.add_argument("password")

class CustomerAPI(Resource):
    def get(self):
        arg = request.args
        email = arg.get("email")
        password = arg.get("password")
        if (type(email) is str) and (email is not None) and len(email) <= 100 and "@" in email and ".com" in email:      
            if (type(password) is str) and (password is not None) and 15 >= len(password) >= 6:                                         
                check = Customer.query.filter_by(Customer_email = email).first()
                if check is not None:
                    if check.Customer_pass == password:
                        Csession["cust"] = check
                        Csession["cid"] = check.Customer_id
                        return  make_response('', 200)
                    raise IncorrectPassword(status_code=400 , error_code = errord["CE5"][0], error_msg=errord["CE5"][1])
                raise make_response('', 404)
            raise InvalidPassword(status_code=400 , error_code = errord["CE3"][0], error_msg=errord["CE3"][1])
        raise InvalidEmail(status_code=400 , error_code = errord["CE2"][0], error_msg=errord["CE2"][1])
        

    @marshal_with(customer_register_out)
    def post(self):
        args = register_user_parser.parse_args()
        name = args.get("name")
        email = args.get("email")
        password = args.get("password")
        ncount, pcount = 0, 0
        for i in range(len(name)):
            if name[i] == " ":
                ncount += 1
        for i in range(len(password)):
            if password[i] == " ":
                pcount += 1

        if (type(name) is str) and (name is not None) and len(name) <= 30 and ncount != len(name):        
            if (type(email) is str) and (email is not None) and len(email) <= 100 and "@" and ".com" in email:      
                if (type(password) is str) and (password is not None) and 15 >= len(password) >= 6 and pcount != len(password):                                         
                    check = Customer.query.filter_by(Customer_email = email).first()
                    if check is None:
                        new_cust = Customer(Customer_name=name, Customer_email=email, Customer_pass=password)
                        ADD.session.add(new_cust)
                        ADD.session.commit()      
                        check2 = Customer.query.filter_by(Customer_email=email).first()
                        Csession["cust"] = check2.Customer_name
                        Csession["cid"] = check2.Customer_id 
                        return check2
                    raise EmailExist(status_code=400 , error_code = errord["CE4"][0], error_msg=errord["CE4"][1])
                raise InvalidPassword(status_code=400 , error_code = errord["CE3"][0], error_msg=errord["CE3"][1])
            raise InvalidEmail(status_code=400 , error_code = errord["CE2"][0], error_msg=errord["CE2"][1])
        raise InvalidName(status_code=400 , error_code = errord["CE1"][0], error_msg=errord["CE1"][1])

class CustomerOUT(Resource):
    def get(self):
        if "cid" in Csession:
            Csession.clear()
            return make_response('', 200)
        return make_response('', 200)

# ============================================ List API ================================================================
list_out = {
    "List_id": fields.Integer,
    "List_name": fields.String,
    "List_desc": fields.String,
}

create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument("name")
create_list_parser.add_argument("description")


class ListAPI(Resource):
    @marshal_with(list_out)
    def post(self):
        if "cid" in Csession:
            args = create_list_parser.parse_args()
            name = args.get("name")
            desc = args.get("description")
            ncount = 0
            for i in range(len(name)):
                if name[i] == " ":
                    ncount += 1

            if (type(name) is str) and (name is not None) and len(name) <= 20 and ncount != len(name):      
                if (type(desc) is str) and (desc is not None) and len(desc) <= 100: 
                    temp_list = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = name).first()
                    if temp_list is None:
                        newList = List(List_name = name, List_desc = desc, Customerl_id = Csession.get("cid"))
                        ADD.session.add(newList)
                        ADD.session.commit()
                        temp = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = name).first()
                        return temp
                    raise NameExist(status_code=400 , error_code = errord["LE3"][0], error_msg=errord["LE3"][1])
                raise InvalidListInfo(status_code=400 , error_code = errord["LE2"][0], error_msg=errord["LE2"][1])
            raise InvalidListInfo(status_code=400 , error_code = errord["LE1"][0], error_msg=errord["LE1"][1])
        raise CustomerNotIn(status_code=400 , error_code = errord["CE6"][0], error_msg=errord["CE6"][1])

    @marshal_with(list_out)
    def put(self, list_name):
        if "cid" in Csession:
            temp = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = list_name).first()
            if temp is not None:
                id = temp.List_id
                args = create_list_parser.parse_args()
                name = args.get("name")
                desc = args.get("description")
                ncount = 0
                for i in range(len(name)):
                    if name[i] == " ":
                        ncount += 1
                tempcheck = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = name).first()
                if (list_name != name and tempcheck is None) or (list_name == name and tempcheck is not None):
                    if (type(name) is str) and (name is not None) and len(name) <= 20 and ncount != len(name):      
                        if (type(desc) is str) and (desc is not None) and len(desc) <= 100: 
                            temp.List_name = name
                            temp.List_desc = desc
                            tem_card = Card.query.filter_by(Listc_id = id).all()
                            for c in tem_card:
                                c.Card_list = name
                            ADD.session.commit()
                            templ = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = name).first()
                            return templ
                        raise InvalidListInfo(status_code=400 , error_code = errord["LE2"][0], error_msg=errord["LE2"][1])
                    raise InvalidListInfo(status_code=400 , error_code = errord["LE1"][0], error_msg=errord["LE1"][1])
                raise NameExist(status_code=400 , error_code = errord["LE3"][0], error_msg=errord["LE3"][1])
            raise NotFound(status_code=404 , error_code = errord["DE8"][0], error_msg=errord["DE8"][1]) 
        raise CustomerNotIn(status_code=400 , error_code = errord["CE6"][0], error_msg=errord["CE6"][1])

    def delete(self, list_name):
        if "cid" in Csession:
            temp = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = list_name).first()
            if temp is not None:
                id = temp.List_id
                List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = list_name).delete()
                Card.query.filter_by(Listc_id = id).delete()
                ADD.session.commit()
                return make_response('', 200)
            raise ListNotFound(status_code=404, error_msg='')
        raise CustomerNotIn(status_code=400 , error_code = errord["CE6"][0], error_msg=errord["CE6"][1])


    def get(self):
        if "cid" in Csession:
            all = dict()
            temp = List.query.filter_by(Customerl_id = Csession.get("cid")).all()
            for t in temp:
                newl = []
                newl.append(t.List_id)
                newl.append(t.List_desc)
                tempc = Card.query.filter_by(Listc_id = t.List_id).all()
                if temp is not None:
                    for c in tempc:
                        newc = []
                        newc.append(c.Card_id)
                        newc.append(c.Card_title)
                        newc.append(c.Card_content)
                        newc.append(c.Card_dline)
                        newc.append(c.Card_status)
                        newl.append(newc)
                all[t.List_name] = newl
            return all
        raise CustomerNotIn(status_code=400 , error_code = errord["CE6"][0], error_msg=errord["CE6"][1])



# ============================================ Card API ================================================================
card_out = {
    "Card_id": fields.Integer,
    "Card_list": fields.String,
    "Card_title": fields.String,
    "Card_content": fields.String,
    "Card_dline": fields.String,
    "Card_status": fields.String
}

create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument("title")
create_card_parser.add_argument("content")
create_card_parser.add_argument("deadline")
create_card_parser.add_argument("status")

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument("move to list")
update_card_parser.add_argument("title")
update_card_parser.add_argument("content")
update_card_parser.add_argument("deadline")
update_card_parser.add_argument("status")

class CardAPI(Resource):
    @marshal_with(card_out)
    def post(self, list_name):
        if "cid" in Csession:
            temp = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = list_name).first()
            if temp is not None:
                args = create_card_parser.parse_args()
                title = args.get("title")
                content = args.get("content")
                d = args.get("deadline")
                status = args.get("status")
                statusList = ["Pending", "Completed", "Failed to complete"]
                dnum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                dmon = ['01', '02', '03' , '04', '05', '06', '07', '08', '09', '10', '11', '12']
                ncount, pcount = 0, 0
                for i in range(len(title)):
                    if title[i] == " ":
                        ncount += 1   
                for i in range(len(content)):
                    if content[i] == " ":
                        pcount += 1                  
     
                if (type(title) is str) and (title is not None) and len(title) <= 20 and ncount != len(title):      
                    if (type(content) is str) and (content is not None) and len(content) <= 100 and pcount != len(content): 
                        if status in statusList:
                            if len(d) == 10 and d[0] in dnum and d[1] in dnum and d[2] in dnum and d[3] in dnum and d[4] == '-' \
                                and d[5:7] in dmon and d[7] == '-' and d[8] in dnum and d[9] in dnum and 31 >= int(d[8:10]) >= 1 and d >= td:
                                temp_card = Card.query.filter_by(Listc_id = temp.List_id, Card_title = title).first()
                                if temp_card is None:
                                    newCard = Card(Card_list = list_name, Card_title = title, Card_content = content,
                                            Card_dline = d, Listc_id = temp.List_id, Card_status = status)
                                    ADD.session.add(newCard)
                                    ADD.session.commit()
                                    ncard = Card.query.filter_by(Listc_id = temp.List_id, Card_title = title).first()
                                    return ncard
                                raise NameExist(status_code=400 , error_code = errord["DE3"][0], error_msg=errord["DE3"][1])
                            raise InvalidCardInfo(status_code=400 , error_code = errord["DE4"][0], error_msg=errord["DE4"][1])    
                        raise InvalidCardInfo(status_code=400 , error_code = errord["DE5"][0], error_msg=errord["DE5"][1])    
                    raise InvalidCardInfo(status_code=400 , error_code = errord["DE2"][0], error_msg=errord["DE2"][1])    
                raise InvalidCardInfo(status_code=400 , error_code = errord["DE1"][0], error_msg=errord["DE1"][1])
            raise NotFound(status_code=404 , error_code = errord["DE8"][0], error_msg=errord["DE8"][1]) 
        raise CustomerNotIn(status_code=400 , error_code = errord["CE6"][0], error_msg=errord["CE6"][1])


    @marshal_with(card_out)
    def put(self, list_name, card_name):
        if "cid" in Csession:
            temp = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = list_name).first()
            if temp is not None:
                tempc = Card.query.filter_by(Listc_id = temp.List_id, Card_title = card_name).first()
                if tempc is not None:
                    args = update_card_parser.parse_args()
                    mlist = args.get("move to list")
                    title = args.get("title")
                    content = args.get("content")
                    d = args.get("deadline")
                    status = args.get("status")
                    statusList = ["Pending", "Completed", "Failed to complete"]
                    tempm = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = mlist).first()
                    if tempm is not None:
                        dnum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        dmon = ['01', '02', '03' , '04', '05', '06', '07', '08', '09', '10', '11', '12']
                        ncount, pcount = 0, 0
                        for i in range(len(title)):
                            if title[i] == " ":
                                ncount += 1   
                        for i in range(len(content)):
                            if content[i] == " ":
                                pcount += 1                  
            
                        if (type(title) is str) and (title is not None) and len(title) <= 20 and ncount != len(title):      
                            if (type(content) is str) and (content is not None) and len(content) <= 100 and pcount != len(content) : 
                                if status in statusList:
                                    if len(d) == 10 and d[0] in dnum and d[1] in dnum and d[2] in dnum and d[3] in dnum and d[4] == '-' \
                                        and d[5:7] in dmon and d[7] == '-' and d[8] in dnum and d[9] in dnum and 31 >= int(d[8:10]) >= 1 and d >= td:
                                        temp_card = Card.query.filter_by(Listc_id = tempm.List_id, Card_title = title).first()
                                        if (mlist == list_name and temp_card != None) or (mlist != list_name and temp_card == None):
                                            tempc.Card_list = mlist 
                                            tempc.Card_title = title 
                                            tempc.Card_content = content
                                            tempc.Card_dline = d 
                                            tempc.Listc_id = tempm.List_id
                                            tempc.Card_status = status                               
                                            ADD.session.commit()
                                            ncard = Card.query.filter_by(Listc_id = tempm.List_id, Card_title = title).first()
                                            return ncard
                                        raise NameExist(status_code=400 , error_code = errord["DE3"][0], error_msg=errord["DE3"][1])
                                    raise InvalidCardInfo(status_code=400 , error_code = errord["DE4"][0], error_msg=errord["DE4"][1])    
                                raise InvalidCardInfo(status_code=400 , error_code = errord["DE5"][0], error_msg=errord["DE5"][1])    
                            raise InvalidCardInfo(status_code=400 , error_code = errord["DE2"][0], error_msg=errord["DE2"][1])    
                        raise InvalidCardInfo(status_code=400 , error_code = errord["DE1"][0], error_msg=errord["DE1"][1])
                    raise NotFound(status_code=404 , error_code = errord["DE6"][0], error_msg=errord["DE6"][1])
                raise NotFound(status_code=404 , error_code = errord["DE7"][0], error_msg=errord["DE7"][1])    
            raise NotFound(status_code=404 , error_code = errord["DE8"][0], error_msg=errord["DE8"][1]) 
        raise CustomerNotIn(status_code=400 , error_code = errord["CE6"][0], error_msg=errord["CE6"][1])


    def delete(self, list_name, card_name):
        if "cid" in Csession:
            temp = List.query.filter_by(Customerl_id = Csession.get("cid"), List_name = list_name).first()
            if temp is not None:
                tempc = Card.query.filter_by(Listc_id = temp.List_id, Card_title = card_name).first()
                if tempc is not None:
                    Card.query.filter_by(Listc_id = temp.List_id, Card_title = card_name).delete()
                    ADD.session.commit()
                    return make_response('', 200)
                raise NotFound(status_code=404 , error_code = errord["DE7"][0], error_msg=errord["DE7"][1])    
            raise NotFound(status_code=404 , error_code = errord["DE8"][0], error_msg=errord["DE8"][1]) 
        raise CustomerNotIn(status_code=400 , error_code = errord["CE6"][0], error_msg=errord["CE6"][1])

    
    