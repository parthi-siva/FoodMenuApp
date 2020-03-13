from flask import render_template,flash,redirect,url_for
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import Employee, Items
from flask_login import logout_user
from flask_login import login_required
from flask import request
from app.forms import RegistrationForm
import datetime

@login_required
@app.route('/index')
@app.route('/')
@login_required
def index():
    return render_template('base.html', title="Home")

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

@app.route("/menu")
@login_required
def menu():
    today = datetime.date.today().strftime("%A")
    menu = Items.query.filter_by(item_nature=today).all()
    return render_template('menu.html', title="Menu",menu=menu, length=len(menu))
