from flask import render_template,flash,redirect,url_for
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ChoiceMenu
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Employee, Items, Orders
from flask import request
import datetime
from collections import defaultdict

@login_required
@app.route('/index')
@app.route('/')
@login_required
def index():
    return redirect(url_for('menu'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        current_user.email = form.username.data
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('menu')
        return redirect(next_page)
    return render_template('Login/login.html', form=form, title="Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Employee(ename=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('Login/register.html', title='Register', form=form)

@app.route("/menu", methods=['GET', 'POST'])
@login_required
def menu():
    today = datetime.date.today().strftime("%A")
    items = Items.query.filter_by(item_nature=today).all()
    form = ChoiceMenu()
    form.foodoption.choices = [(itm.itemid, itm.itemname) for itm in  items]
    if form.validate_on_submit():
        empid = Employee.query.filter_by(email=current_user.email).first()
        alreadyorderd = Orders.query.filter_by(item_id=form.foodoption.data, e_id=empid.id).first()
        if alreadyorderd is None:
            orders = Orders(item_id=form.foodoption.data, e_id=empid.id, quantity=form.quantity.data)
            db.session.add(orders)
            db.session.commit()
            return redirect(url_for('menu'))
        alreadyorderd.quantity += form.quantity.data
        db.session.commit()
        return redirect(url_for('menu'))
    return render_template("menu.html", form=form)

@app.route("/orders", methods=['GET', 'POST'])
@login_required
def Myorders():
    empid = Employee.query.filter_by(email=current_user.email).first()
    orderdetails = {}
    for val in Orders().query.filter_by(e_id=empid.id).all():
        itemName = Items.query.filter_by(itemid=val.item_id).first()
        orderdetails.update({ itemName.itemname : (val.quantity,val.id) })
    return render_template("orders.html", data=orderdetails)

@app.route("/orders/<int:order_id>/update", methods=['GET', 'POST'])
@login_required
def editorders(order_id):
    order = Orders().query.filter_by(id=order_id).first()
    itemName = Items.query.filter_by(itemid=order.item_id).first()
    form = ChoiceMenu()
    form.foodoption.choices = [(order.item_id, itemName.itemname)]
    #print(order.item_id,order.quantity, form.quantity.data)
    if form.validate_on_submit():
        order.item_id = form.foodoption.data 
        order.quantity = form.quantity.data
        db.session.commit()
        return redirect(url_for("Myorders"))
    elif request.method == "GET":
        form.foodoption.choices = [(order.item_id, itemName.itemname)]
        form.quantity.data = order.quantity
    return render_template("menu.html", form=form)

@app.route("/orders/<int:order_id>/delete", methods=['GET', 'POST'])
@login_required
def deleteorder(order_id):
    order = Orders().query.filter_by(id=order_id).first()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("Myorders"))
