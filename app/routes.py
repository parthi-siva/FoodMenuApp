from datetime import date, datetime
from collections import defaultdict
import time
from flask import render_template,flash,redirect,url_for
from flask import request, session
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, ChoiceMenu, ReportForm
from app.models import Employee, Items, Orders

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
        user = Employee.query.filter_by(emp_id=form.username.data).first()
        print(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        current_user.emp_id = form.username.data
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
        user = Employee(ename=form.name.data, emp_id=form.emp_id.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('Login/register.html', title='Register', form=form)

def datetime_from_utc_to_local():
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return datetime.strptime((datetime.utcnow() + offset).strftime("%Y-%m-%d"), "%Y-%m-%d")

@app.route("/menu", methods=['GET', 'POST'])
@login_required
def menu():
    menu_type = request.args.get("ordertype",1,type=int)
    if menu_type == 1:
        today = date.today().strftime("%A")
    elif menu_type == 0:
        today = "Daily"
    else:
        return redirect(url_for('logout'))
    items = Items.query.filter_by(item_nature=today).all()
    form = ChoiceMenu()
    form.foodoption.choices = [(itm.itemid, itm.itemname) for itm in  items]
    if form.validate_on_submit():
        alreadyorderd = Orders.query.filter_by(item_id=form.foodoption.data, e_id=current_user.emp_id).first()
        if alreadyorderd is None:
            orders = Orders(item_id=form.foodoption.data, e_id=current_user.emp_id,
                            quantity=form.quantity.data, order_date=datetime_from_utc_to_local())
            db.session.add(orders)
            db.session.commit()
            return redirect(url_for('menu'))
        alreadyorderd.quantity += form.quantity.data
        db.session.commit()
        return redirect(url_for('menu'))
    return render_template("menu.html", form=form, 
                           disabletime=datetime_from_utc_to_local().timetuple())

@app.route("/orders", methods=['GET', 'POST'])
@login_required
def Myorders():
    orderdetails = {}
    for val in Orders().query.filter_by(e_id=current_user.emp_id).all():
        itemName = Items.query.filter_by(itemid=val.item_id).first()
        orderdetails.update({itemName.itemname : (val.quantity,val.id)})
    return render_template("orders.html", data=orderdetails)

@app.route("/orders/<int:order_id>/update", methods=['GET', 'POST'])
@login_required
def editorders(order_id):
    order = Orders().query.filter_by(id=order_id).first()
    itemName = Items.query.filter_by(itemid=order.item_id).first()
    form = ChoiceMenu()
    form.foodoption.choices = [(order.item_id, itemName.itemname)]
    if form.validate_on_submit():
        order.item_id = form.foodoption.data
        order.quantity = form.quantity.data
        order.order_date = datetime_from_utc_to_local()
        db.session.commit()
        return redirect(url_for("Myorders"))
    elif request.method == "GET":
        form.foodoption.choices = [(order.item_id, itemName.itemname)]
        form.quantity.data = order.quantity
    return render_template("menu.html", form=form,
                            disabletime=datetime_from_utc_to_local().timetuple())

@app.route("/orders/<int:order_id>/delete", methods=['GET', 'POST'])
@login_required
def deleteorder(order_id):
    order = Orders().query.filter_by(id=order_id).first()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("Myorders"))

@app.route("/report", methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        session["startdate"] = form.startdate.data
        session["enddate"] = form.enddate.data
        return redirect(url_for("expense"))
    return render_template("report.html", form=form )

@app.route("/expense")
@login_required
def expense():
    startdate = datetime.strptime(session["startdate"],"%a, %d %b %Y %H:%M:%S %Z")
    enddate = datetime.strptime(session["enddate"],"%a, %d %b %Y %H:%M:%S %Z")
    print(startdate, enddate)
    page = request.args.get("page",1,type=int)
    report = Orders.query.filter(
                                Orders.order_date.between(startdate,enddate)). \
                                order_by(Orders.order_date).paginate(page=page,per_page=1)
    return render_template("expense.html", report=report, datetime=datetime)
