from flask import Flask, session, request, url_for, redirect, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import decimal
from os import environ

from models import db, User, Transaction
from forms import SignupForm, LoginForm, BuyForm

import iex

# Create Flask application
app = Flask(__name__)
app.secret_key = 'sekrit'
# Set SQLite DB and create if not existing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
with app.app_context():
	db.create_all()

@app.route('/')
def index():
	"""
	Landing page
	"""
	return render_template('index.html', title='myPortfolio')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Login page with user querying
	"""
	if 'user' in session:
		return redirect(url_for('portfolio'))

	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			email = form.email.data
			password = form.password.data
			# Check if there is an email match in db
			user = User.query.filter_by(email=email).first()
			if user != None:
				# Check password if email exists
				if user.check_password(password):
					session['user'] = user.id
					return redirect(url_for('portfolio'))	
		flash('Email/Password combination does not exist.')
	return render_template('login.html', form=form, title='Login')

@app.route('/logout')
def logout():
	"""
	Log out of website by removing user key from session
	"""
	if 'user' in session:
		session.pop('user', None)

	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""
	Create a new account with a unique email
	User's cash account is $5000.00 USD by default
	"""
	if 'user' in session:
		return redirect(url_for('portfolio'))

	form = SignupForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			name = form.name.data
			email = form.email.data
			password = form.password.data
			# Create new User from model
			new_user = User(name=name, email=email, password=password)
			# Attempt to add new user to db
			try:
				db.session.add(new_user)
				db.session.flush()
			except IntegrityError:
				# Rollback if duplicate
				db.session.rollback()
				flash('Email is already in use.')
				return render_template('register.html', form=form, title='Register')
			else:
				db.session.commit()

			user = User.query.filter_by(email=email).first()
			# Store user id in session
			session['user'] = user.id
			return redirect(url_for('portfolio'))
		else:
			# Flash errors in form validation
			if 'password' in form.errors:
				flash('Passwords must match.')
	return render_template('register.html', form=form, title='Register')

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
	"""
	View user stock portfolio and make buy orders
	"""
	if 'user' not in session:
		return redirect(url_for('login'))
	# Fetch user information from db
	user = User.query.filter_by(id=session['user']).first()
	balance = '%.2f'%(user.money)
	
	form = BuyForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			symbol = form.ticker.data
			quantity = form.quantity.data
			symbol_price = iex.get_symbol_price(symbol)
			# Check if symbol exists
			if not symbol_price:
				flash('Symbol does not exist')
				return redirect(url_for('portfolio'))
			# Check if user has enough funds to purchase
			total_price = quantity * symbol_price
			if total_price <= decimal.Decimal(user.money):
				new_transaction = Transaction(user_id=session['user'], symbol=symbol.upper(), quantity=quantity, price=symbol_price, buy_transaction=True)
				user.money -= decimal.Decimal(total_price)
				db.session.add(new_transaction)
				db.session.commit()
				flash('Successfully bought {} shares of {} at {}'.format(quantity, symbol.upper(), symbol_price))
			else:
				flash('Not enough money')
			return redirect(url_for('portfolio'))

	# Gather portfolio information from transactions
	symbol_count = {}
	transactions = Transaction.query.filter_by(user_id=session['user']).all()
	for transaction in transactions:
		symbol_count[transaction.symbol.upper()] = symbol_count.get(transaction.symbol.upper(), 0) + transaction.quantity
	stocks = []
	for symbol in symbol_count:
		symbol_json = iex.get_symbol(symbol)
		open_price = symbol_json['open']
		cur_price = symbol_json['latestPrice']
		stocks.append({
			'change_sign': 1 if cur_price > open_price else -1 if cur_price < open_price else 0,
			'symbol': symbol,
		 	'count': symbol_count[symbol],
			'value': cur_price * symbol_count[symbol]
			})

	value = '%.2f'%(sum(stock['value'] for stock in stocks))
	return render_template('portfolio.html', balance=balance, value=value, stocks=stocks, form=form, title='Portfolio')

@app.route('/transactions', methods=['GET'])
def transactions():
	"""
	View all transactions for the user ordered by date
	"""
	if 'user' not in session:
		return redirect(url_for('login'))
	transactions = Transaction.query.filter_by(user_id=session['user']).order_by(Transaction.transaction_date.desc()).all()
	return render_template('transactions.html', transactions=transactions, title='Transactions')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=environ.get('port', 8000))