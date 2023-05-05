# ==================================================== Imports ====================================================================
import imp
from flask import session, render_template, request, url_for, redirect, flash
from flask import current_app as app
from .models import Customer, List, Card, ADD
from datetime import date
import matplotlib 
matplotlib.use('Agg')
from matplotlib import pyplot as plt


# ==================================================== Creating Routes ============================================================

# ==================================================== Main Route : Home Page ====================================================
@app.route('/')
def Welcome():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login_add():
    # Checking if request is post
    if request.method == 'POST':
        formed = request.form
        email_add = formed['email']
        pass1_add = formed['pass1']

        # Checking if customer is in the database
        check = Customer.query.filter_by(Customer_email = email_add).first()
        if check is not None:
            # Customer is in database : verifying password
            if check.Customer_pass == pass1_add:
                # Customer verified : adding data in the session
                session["cust"] = check.Customer_name
                session["cid"] = check.Customer_id
                # redirecting to user's dashboard
                return redirect(url_for('show_add'))
            else:
                # Incorrect password
                flash("Incorrect password! Check password and try again.", category="e")
                return render_template('login.html')
        else:
            # User is not in the database
            flash("User not found!", category="success")
            return render_template('login.html')
    else:
        # If request is get : render login page
        return render_template('login.html')

# ==================================================== Route : Register ===============================================
@app.route('/register', methods=['GET', 'POST'])
def register_add():
    # Checking if request is post
    if request.method == 'POST':
        # Getting data from the form
        formed = request.form
        name_add = formed['name']
        email_add = formed['email']
        pass1_add = formed['pass1']
        # Validating inputs
        ncount, pcount = 0, 0
        for i in range(len(name_add)):
            if name_add[i] == " ":
                ncount += 1
        for i in range(len(pass1_add)):
            if pass1_add[i] == " ":
                pcount += 1

        # Checking if customer is already in the database
        check = Customer.query.filter_by(Customer_email = email_add).first()
        if check is None:
            # Customer is not available 
            if ncount != len(name_add) and pcount != len(pass1_add):
                if len(pass1_add) < 6 or ' ' in pass1_add:
                    # if Password length is less than 6 charectors
                    flash("Password should be at least 6 charectors long!", category="e")
                    return render_template('register.html')
                # Everything is fine : Creating customer account
                new_cust = Customer(Customer_name=name_add, Customer_email=email_add, Customer_pass=pass1_add)
                ADD.session.add(new_cust)
                ADD.session.commit()
                # Customer created : adding data in the session for login
                check2 = Customer.query.filter_by(Customer_email=email_add).first()
                session["cust"] = check2.Customer_name
                session["cid"] = check2.Customer_id
                # redirecting to user's dashboard
                return redirect(url_for('show_add'))
            else:
                # If input is not valid
                flash("Please enter valid detalis.", category='note')
                return render_template('register.html')
        else:
            # if customer is already in the database
            flash("email already exist", category="e")
            return render_template('register.html')
    else:
        # if request is get : render register page
        return render_template('register.html')

# ==================================================== Route : Logout ===============================================
@app.route('/logout')
def disappear():
    if "cust" in session:
        # when customer is in session : clear session data
        session.clear()
        flash("Logged out successfully!", category="success")
        # redirect to the login page
        return redirect(url_for('login_add'))
    return redirect(url_for('login_add'))



# ==================================================== Route : Dashboard =========================================================
@app.route('/dashboard')
def show_add():
    if "cid" in session:           # To check if user is logged in
        tday = str(date.today())
        all_lists = []             # Full information of all Lists of the user
        all_lnames = []
        c_id = session.get('cid')
        # Retriving all lists of the user from DB
        temp_lists = List.query.filter_by(Customerl_id = c_id).all()

        # Retriving all cards of the given list from DB
        for l in temp_lists:
            all_lnames.append(l.List_name)
            cards = Card.query.filter_by(Listc_id = l.List_id).all()
            temp_card = []         # Full information of all Cards of the given List

            # Checking and updating cards as 'Failed to complete' if deadline has passed and task is pending
            for t in cards:
                if t.Card_dline < tday and t.Card_status == 'Pending':
                    t.Card_status = 'Failed to complete'
                    ADD.session.commit()

                    # Making bundle of card info
                    c = [t.Card_list, t.Card_title, t.Card_content, t.Card_dline, 'Failed to complete']
                    temp_card.append(c)
                else:
                    c = [t.Card_list, t.Card_title, t.Card_content, t.Card_dline, t.Card_status]
                    temp_card.append(c)

            # Making bundle of List info
            temp_list = [l.List_name, l.List_desc, temp_card, l.List_id]
            all_lists.append(temp_list)
        # Rendering user's Dashboard with full info of List and Cards
        return render_template("dashboard.html", lister = all_lists, user = session.get("cust"))

    # Redirecting user to the Home page if not logged in
    else:
        flash("Please login or register to continue.", category="note")
        return redirect(url_for('Welcome'))


# ==================================================== Route : Add List =========================================================
@app.route('/createlist', methods=['GET', 'POST'])
def list_add():
    if request.method == "POST" and "cid" in session:
        listName = request.form["name"]
        listDesc = request.form["desc"]
        ncount = 0
        for i in range(len(listName)):
            if listName[i] == " ":
                ncount += 1
        if ncount != len(listName):
            c_id = session.get('cid')
            temp_lists = List.query.filter_by(Customerl_id = c_id).all()
            lnme = []
            for t in temp_lists:
                lnme.append(t.List_name)
            if listName not in lnme:
                newList = List(List_name = listName, List_desc = listDesc, Customerl_id = c_id)
                ADD.session.add(newList)
                ADD.session.commit()
                return redirect(url_for('show_add'))
            else:
                flash('The given list name is already exist. Please try with another name!', category='note')
                return redirect(url_for('show_add'))
        else:
            flash("Please enter a valid name.", category='note')
            return render_template("listadd.html", user = session.get("cust"))

    elif request.method == "GET" and "cid" in session:
        return render_template("listadd.html", user = session.get("cust"))
    else:
        flash("Please login to continue.", category="note")
        return redirect(url_for('login_add'))



# ==================================================== Route : Add Card ====================================================================
@app.route('/<lname>/createcard', methods=['GET', 'POST'])
def task_add(lname):
    # Getting all list 
    temp_lists = List.query.filter_by(Customerl_id = session["cid"]).all()
    if len(temp_lists) > 0:
        g_lists = []
        for l in temp_lists:
            g_lists.append(l.List_name)
    if lname in g_lists:
        # Checking request method is POST and user is logged in
        if request.method == "POST" and "cid" in session:
            print(request.form)
            cardList = request.form["list"]
            cardName = request.form["name"]
            cardCont = request.form["desc"]
            cardDL = request.form["deadline"]
            # Validating inputs
            ncount, pcount = 0, 0
            for i in range(len(cardName)):
                if cardName[i] == " ":
                    ncount += 1
            for i in range(len(cardCont)):
                if cardCont[i] == " ":
                    pcount += 1
            # Checking if Card is mark as Completed or not
            if "status" in request.form:
                cardStatus = request.form["status"]
            else:
                cardStatus = "Pending"

            if ncount != len(cardName) and pcount != len(cardCont):
                # Making sure that new Card has a unique name
                l = List.query.filter_by(Customerl_id = session.get('cid'), List_name = cardList).first()
                check = Card.query.filter_by(Listc_id = l.List_id, Card_title = cardName).first()
                if check is None:
                    # Card name is unique : Creating Card
                    get_list = List.query.filter_by(List_name = cardList, Customerl_id = session.get("cid")).first()
                    l_id = get_list.List_id
                    newcard = Card(Card_list = cardList, Card_title = cardName, Card_content = cardCont,
                                    Card_dline = cardDL, Listc_id = l_id, Card_status = cardStatus)
                    ADD.session.add(newcard)
                    ADD.session.commit()
                    return redirect(url_for('show_add'))

                else:
                    # Card name is not unique : returned to dashboard
                    flash('The given card name is already exist. Please try with another name!', category='note')
                    return redirect(url_for('show_add'))
            else:       
                #getting list names in case of error
                flash("Please enter valid detalis.", category='e')
                return redirect(url_for('display.task_add', lname = lname))
        # If customer is logged in and request is get
        elif request.method == "GET" and "cid" in session:
            tday = str(date.today())
            glists = g_lists.copy()
            glists.remove(lname)
            # Rendering card add  form
            return render_template("cardadd.html", user = session.get("cust"), lists = glists, td = tday, own = lname)
        else:
            # If customer is not logged in
            flash("Please login to continue.", category="note")
            return redirect(url_for('login_add'))
    else:
        # If lname not in the database
        flash(f"There is no list with the name {lname}", category="note")
        return redirect(url_for('show_add'))



# ==================================================== Route : Delete List ====================================================================
@app.route('/dlist/<lname>/confirm')
def confirmlist_delete(lname):
    # Checking if the customer is logged in
    if "cust" and "cid" in session:    
        # Checking if list is available in the database   
        check = List.query.filter_by(Customerl_id = session.get("cid"), List_name = lname).first()
        if check is not None:
            # List is available : send confirmation
            return render_template('confirml.html', list = lname, user = session.get("cust"))
        else:
            # If list is not present in the database : redirected to dashboard
            flash( f"There is no list with the name {lname}", category = "note" )
            return redirect(url_for('show_add'))
    else:
        # If customer is not logged in : redirected to login page
        flash("Please login to continue.", category="note")
        return redirect(url_for('login_add'))


@app.route('/dlist/<list>/delete', methods=['GET', 'POST'])
def deletelist(list):
    # Checking if request is post : deletion confirmed
    if request.method == 'POST':
        # Getting list_id by name
        dlis = List.query.filter_by(Customerl_id = session.get("cid"), List_name = list).first()
        l_id = dlis.List_id
        # Deleting list 
        List.query.filter_by(Customerl_id = session.get("cid"), List_id = l_id).delete()
        # Deleting Cards of the list
        Card.query.filter_by(Listc_id = l_id).delete()
        ADD.session.commit()
        # Redirected to dashboard
        flash("List deleted successfully!", category = "success")
        return redirect(url_for('show_add'))
    else:
        # Redirected for confirmation
        return redirect(f'/dlist/{list}/confirm')



# ==================================================== Route : Delete Card ====================================================================
@app.route('/dcard/<int:lid>/<cname>/confirm')
def confirmcard_delete(cname, lid):
    # Checking if the customer is logged in
    if "cust" and "cid" in session:
        # Checking if List is available in the database
        check = List.query.filter_by(Customerl_id = session.get("cid"), List_id = lid).first()
        if check is not None:
            # List is available : Checking if card is available in the List
            temp_card = Card.query.filter_by(Listc_id = lid, Card_title = cname).first()
            if temp_card is not None:
                # Card is available : send confirmation
                return render_template('confirmc.html', card = cname, lis_id = lid, user = session.get("cust"))
            else:
                # Card is not present in the database : redirected to dashboard
                flash(f"There is no such card.", category="note")
                return redirect(url_for('show_add'))
        else:
            # List is not present in the database : redirected to dashboard
            flash(f"There is no such list.", category="note")
            return redirect(url_for('show_add'))
    else:
        # If customer is not logged in : redirected to login page
        flash("Please login to continue.", category="note")
        return redirect(url_for('login_add'))


@app.route('/dcard/<int:lid>/<cname>/delete', methods=['GET', 'POST'])
def deletecard(lid, cname):
    # Checking if request is post : deletion confirmed
    if request.method == 'POST':
        # Deleting Card
        Card.query.filter_by(Listc_id = lid, Card_title = cname).delete()
        ADD.session.commit()
        # Redirected to dashboard
        flash("Card deleted successfully!", category="success")
        return redirect(url_for('show_add'))
    else:
        # Redirected for confirmation
        return redirect(f'/dcard/{lid}/{cname}/confirm')



# ==================================================== Route : Edit List ====================================================================
@app.route('/editlist/<lname>', methods=['GET', 'POST'])
def updatelist(lname):
    # Checking if request is post
    if request.method == 'POST':
        # Getting new data
        new_lname = request.form["name"]
        new_ldesc = request.form["desc"]
        # Validating input
        ncount = 0
        for i in range(len(new_lname)):
            if new_lname[i] == " ":
                ncount += 1

        if ncount != len(new_lname):
            # Input is valid : update list data
            temp_list = List.query.filter_by(Customerl_id = session.get("cid"), List_name = lname).first()
            temp_cards = Card.query.filter_by(Listc_id = temp_list.List_id).all()
            temp_list.List_name = new_lname
            temp_list.List_desc = new_ldesc
            # Update list name in the cards
            if temp_cards is not None:
                for t in temp_cards:
                    t.Card_list = new_lname
            ADD.session.commit()
            flash("List updated successfully!", category="success")
            return redirect(url_for('show_add'))
        else:
            # Input is not valid : redirected to the same page
            flash("Please enter valid detalis.", category='note')
            return redirect(url_for('updatelist', lname=lname))

    else:
        # Checking if the customer is logged in
        if "cust" and "cid" in session:
            # Checking if List is available in the database
            check = List.query.filter_by(Customerl_id = session.get("cid"), List_name = lname).first()
            if check is not None:
                # List is available : rendering editing page
                temp_list = List.query.filter_by(Customerl_id = session.get("cid"), List_name = lname).first()
                content = temp_list.List_desc
                return render_template('elist.html', list = lname, cont = content, user = session.get("cust"))
            else:
                # List is not available : redirected to dashboard
                flash(f"There is no list with the name {lname}", category="note")
                return redirect(url_for('show_add'))
        else:
            # Customer is not logged in : redirected to login page
            flash("Please login to continue.", category="note")
            return redirect(url_for('login_add'))



# ==================================================== Route : Edit Card ====================================================================
@app.route('/editcard/<int:lid>/<cname>', methods=['GET', 'POST'])
def updatecard_add(cname, lid):
    # Checking if user is logged in and method is post
    if request.method == 'POST' and 'cust' in session:
        ncardList = request.form["list"]
        ncardName = request.form["name"]
        ncardCont = request.form["desc"]
        ncardDL = request.form["deadline"]
        # Validating input
        ncount, pcount = 0, 0
        for i in range(len(ncardName)):
            if ncardName[i] == " ":
                ncount += 1
        for i in range(len(ncardCont)):
            if ncardCont[i] == " ":
                pcount += 1

        check = List.query.filter_by(Customerl_id = session.get('cid'), List_id = lid).first()
        checkn = List.query.filter_by(Customerl_id = session.get('cid'), List_name = ncardList).first()
        check2 = Card.query.filter_by(Listc_id = checkn.List_id, Card_title = ncardName).first()
        check3 = Card.query.filter_by(Listc_id = checkn.List_id, Card_title = cname).first()

        if ((ncardList == check.List_name) and (check3 is None or check3.Card_id == check2.Card_id)) or (ncardList != check.List_name and check2 is None):
            if ncount != len(ncardName) and pcount != len(ncardCont):
                # Getting id of the new list 
                # get_flist = List.query.filter_by(List_name = ncardList, Customerl_id = session.get("cid")).first()
                l_id = check.List_id
                get_card = Card.query.filter_by(Card_title = cname, Listc_id = lid).first()

                # Updating card data
                if "status" in request.form:
                    ncardStatus = request.form["status"]
                    get_card.Card_status = ncardStatus     
                get_card.Card_list = ncardList
                get_card.Card_title = ncardName
                get_card.Card_content = ncardCont
                get_card.Listc_id = l_id
                get_card.Card_dline = ncardDL
                ADD.session.commit()

                flash("Task updated successfully!", category="success")
                return redirect(url_for('show_add'))
            else:   
                # Invalid inputs : redirected to the same page     
                flash("Please enter valid detalis.", category='e')
                return redirect(url_for('updatecard_add', cname=cname, lid=lid))
        else:
            # Card name is not unique : returned to dashboard
            flash('The given card name is already exist. Please change the card name!', category='note')
            return redirect(url_for('show_add'))
    else:
        # Checking if the customer is logged in
        if "cust" and "cid" in session:
            # Checking if List is available in the database
            check = List.query.filter_by(List_id = lid, Customerl_id = session.get("cid")).first()
            lname = check.List_name 

            if check is not None:
                # List is available : checking if card is there in the list
                temp_card = Card.query.filter_by(Listc_id = lid, Card_title = cname).first()
                if temp_card is not None:
                    # Card is available : getting info and rendering template
                    g_list = temp_card.Card_list
                    # g_name = temp_card.Card_add_title
                    g_cont = temp_card.Card_content
                    g_status = temp_card.Card_status
                    g_dline = temp_card.Card_dline

                    tday = str(date.today())
                    # Getting all list to render the card edit page
                    temp_lists = List.query.filter_by(Customerl_id = session["cid"]).all()
                    if len(temp_lists) > 0:
                        glists = []
                        for l in temp_lists:
                            glists.append(l.List_name)
                    glists.remove(lname)
                    return render_template('editc.html', ecard=cname, elis_id=lid, user=session.get("cust"),
                                            elists=glists, econt=g_cont, elist=g_list, edl=g_dline,
                                            estatus=g_status, td=tday, own=lname)
                else:
                    # Card is not available in the list
                    flash(f"Card not found.", category="note")
                    return redirect(url_for('show_add'))
            else:
                # List is not available in the database
                flash(f"List not found.", category="note")
                return redirect(url_for('show_add'))

        else:
            # Customer is not logged in : redirected to login page
            flash("Please login to continue.", category="note")
            return redirect(url_for('login_add'))



# ==================================================== Route : Summary ====================================================================
@app.route('/dashboard/summary')
def show_summary():
    # Checking is customer is logged in
    if "cid" in session:
        lists = []
        temp_lists = List.query.filter_by(Customerl_id = session.get("cid")).all()
        # Getting card info of every list
        for l in temp_lists:
            cards = Card.query.filter_by(Listc_id = l.List_id).all()
            # Collecting Cards by status
            complete_cards = Card.query.filter_by(Listc_id = l.List_id, Card_status='Completed').all()
            pending_cards = Card.query.filter_by(Listc_id = l.List_id, Card_status='Pending').all()
            dlpassed_cards = Card.query.filter_by(Listc_id = l.List_id, Card_status='Failed to complete').all()
            fname = l.List_name

            total_cards = len(cards)
            comp_cards = len(complete_cards)
            pen_cards = len(pending_cards)
            dpass_cards = len(dlpassed_cards)

            lists.append([l.List_name, l.List_desc, total_cards, comp_cards, pen_cards, dpass_cards])
            # Graph ploting
            if total_cards > 0:
                pdata = [comp_cards, pen_cards, dpass_cards]
                pcolor = ['#089034', '#eda918', '#f00e2a']
                plabel = ['Completed', 'Pending', 'Failed to complete']
                plt.clf()
                plt.bar(plabel, pdata, color=pcolor)
                plt.ylabel('No of tasks')
                plt.savefig(f'static/images/{fname}.PNG')
        # Rendering summary page with data
        return render_template("summary.html", lister = lists, user = session.get("cust"))
    else:
        # Customer is not logged in : redirected to login page 
        flash("Please login to continue.", category="note")
        return redirect(url_for('login_add'))

# ========================================================= End ===============================================================================
