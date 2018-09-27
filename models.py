from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Models
class User(db.Model):
	"""
	Model to store User data
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	money = db.Column(db.DECIMAL, nullable=False)
	transactions = db.relationship('Transaction', backref='user', lazy=True)

	def __init__(self, name, email, password):
		self.name = name.title()
		self.email = email.lower()
		self.password = self.hash_password(password)
		self.money = 5000.00
		
	def hash_password(self, password):
		return generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

class Transaction(db.Model):
	"""
	Model to store transaction data for every user
	"""
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	symbol = db.Column(db.String(10), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	price = db.Column(db.DECIMAL, nullable=False)
	transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	buy_transaction = db.Column(db.Boolean, nullable=False)
	def __init__(self, user_id, symbol, quantity, price, buy_transaction):
		self.user_id = user_id
		self.symbol = symbol
		self.quantity = quantity
		self.price = price
		self.buy_transaction = buy_transaction
