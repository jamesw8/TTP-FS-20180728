from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Models
class User(db.Model):
	"""
	Model to store User data
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), unique=True, nullable=False)
	
	def __init__(self, username, email, password):
		self.name = name.title(),
		self.email = email.lower(),
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)
