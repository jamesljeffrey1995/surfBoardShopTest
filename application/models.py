from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    ordersbyuser = db.relationship('Orders',backref='customer', lazy=True)


    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Email: ', self.email, '\r\n',
            'Name: ', self.first_name, ' ', self.last_name
        ])


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_ordered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_order = db.relationship('Product', secondary = 'order_line')

class Order_line(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id= db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    style = db.Column(db.String(100), nullable=False, unique=True)
    volume = db.Column(db.Float, nullable=False)
    size = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    product_line= db.relationship(Orders, secondary='order_line')
