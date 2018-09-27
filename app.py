from flask import Flask, session, request, url_for, redirect, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import decimal

from models import db, User, Transaction
from forms import SignupForm, LoginForm, BuyForm

import iex

app = Flask(__name__)
app.secret_key = 'sekrit'
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
		print(form.validate())
		print(form.errors)
		if form.validate_on_submit():
			email = form.email.data
			password = form.password.data
			user = User.query.filter_by(email=email).first()
			print('Trying')
			if user != None:
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
	User's cash account is $5000.00 USD by default
	One account per email
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
				db.session.rollback()
				flash('Email is already in use.')
				return render_template('register.html', form=form, title='Register')
			else:
				db.session.commit()

			user = User.query.filter_by(email=email).first()
			session['user'] = user.id
			app.logger.info('Successful signup')
			return redirect(url_for('portfolio'))
		else:
			if 'password' in form.errors:
				flash('Passwords must match.')
	return render_template('register.html', form=form, title='Register')

# TODO
@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
	if 'user' not in session:
		return redirect(url_for('login'))
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
			total_price = quantity * symbol_price
			if total_price <= decimal.Decimal(user.money):
				new_transaction = Transaction(user_id=session['user'], symbol=symbol, quantity=quantity, price=total_price)
				user.money -= decimal.Decimal(total_price)

				db.session.add(new_transaction)
				db.session.commit()
				flash('Buy order created')
			else:
				flash('Not enough money')
			return redirect(url_for('portfolio'))
		flash(form.errors)

	symbol_count = {}
	transactions = Transaction.query.filter_by(user_id=session['user']).all()
	for transaction in transactions:
		print(dir(transaction))
		symbol_count[transaction.symbol.upper()] = symbol_count.get(transaction.symbol.upper(), 0) + transaction.quantity

	stocks = [{'symbol': symbol, 'count': symbol_count[symbol], 'value': iex.get_symbol_price(symbol) * symbol_count[symbol]}
	for symbol in symbol_count]
	value = '%.2f'%(sum(stock['value'] for stock in stocks))
	return render_template('portfolio.html', balance=balance, value=value, stocks=stocks, form=form, title='Portfolio')

# TODO
@app.route('/transactions', methods=['GET'])
def transactions():
	if 'user' not in session:
		return redirect(url_for('login'))

	return 'Trading page'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)