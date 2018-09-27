from flask import Flask, session, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from models import db, User

app = Flask(__name__)
app.secret_key = 'sekrit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def index():
	"""
	Landing page
	"""
	return 'Landing page'

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""
	"""
	if request.method == 'POST':
		email, password = request.form.get('email', ''), request.form.get('password', '')
		User.query.filter_by(email=email)
		session['user'] = None # Look up sql query here
	return 'Login with Email and Password'

@app.route('/logout')
def logout():
	"""
	Logout of website
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
	print(dir(request))
	print(request.method)
	if request.method == 'GET':
		return '''
		<form method="post">
			<input type="text" name=name placeholder="Name" />
			<input type="text" name=email placeholder="Email" />
			<input type="password" name=password placeholder="Password" />
			<input type="submit" value="Register"/>
		</form>
		'''
	elif request.method == 'POST':
		# Need to validate
		pass
	else:
		return redirect(url_for('index'))
	return 'Register with Name, Email, and Password'

@app.route('/trade', methods=['GET'])
def trade():
	if 'username' not in session:
		return redirect(url_for('login'))
	return 'Trading page'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)