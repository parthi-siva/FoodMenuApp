from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    order = db.relationship('Order', backref='orders', lazy='dynamic')

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
    orderedItem = db.relationship('Order', backref='ordereditem', lazy='dynamic')
    def __repr__(self):
        return '<Item Name : {}>'.format(self.itemname)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    e_id = db.Column(db.Integer, db.ForeignKey("items.itemid"))
    quantity = db.Column(db.Integer)
    order_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Item id : {}>'.format(self.item_id)
