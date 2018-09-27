from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms import validators

class SignupForm(FlaskForm):
	name = StringField('Name', validators=[validators.DataRequired()])
	email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
	password = PasswordField('Password (8-20 characters)', validators=[validators.DataRequired(),
		validators.Length(min=8, max=20), validators.EqualTo('confirm_password')])
	confirm_password = PasswordField('Repeat Password')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[validators.DataRequired()])
	password = PasswordField('Password', validators=[validators.DataRequired()])

class BuyForm(FlaskForm):
	ticker = StringField('Ticker', validators=[validators.DataRequired()])
	quantity = IntegerField('Qty', validators=[validators.DataRequired(), validators.NumberRange(min=1, message='Need to purchase at least one')])
