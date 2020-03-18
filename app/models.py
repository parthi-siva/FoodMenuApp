from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from app import db, login, admin

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))

class EmplyeeMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Employee ID : {}>'.format(self.employee_id)

class SuperUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(64), index=True, unique=True)

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(64), index=True)
    emp_id = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    order = db.relationship('Orders', backref='orders', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee Name : {}>'.format(self.ename)

class Items(db.Model):
    itemid = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.Integer)
    item_nature = db.Column(db.String(64))
    orderedItem = db.relationship('Orders', backref='ordereditem', lazy='dynamic')
    def __repr__(self):
        return '<Item Name> : {}'.format(self.itemname)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.itemid"))
    e_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    quantity = db.Column(db.Integer)
    order_date = db.Column(db.DateTime, index=True)
    def __repr__(self):
        return '<Item id : {}>'.format(self.item_id)

class Itemsview(ModelView):
    form_columns = ["itemid", "itemname", "price", "item_nature"]

admin.add_view(Itemsview(Items, db.session))
admin.add_view(ModelView(EmplyeeMaster, db.session))
