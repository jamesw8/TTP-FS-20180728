from flask import Flask, session, request, url_for, redirect, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from models import db, User
from forms import SignupForm, LoginForm

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
					return redirect(url_for('trade'))	
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

	print(request.form)
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
			return redirect(url_for('trade'))

	return render_template('register.html', form=form, title='Register')

# TODO
@app.route('/portfolio')
def portfolio():
	if 'user' not in session:
		return redirect(url_for('login'))

	return 'Portfolio'

# TODO
@app.route('/trade', methods=['GET'])
def trade():
	if 'user' not in session:
		return redirect(url_for('login'))

	return 'Trading page'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)