from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import validators

class SignupForm(FlaskForm):
	name = StringField('Name', validators=[validators.DataRequired()])
	email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
	password = PasswordField('Password (8-20 characters)', validators=[validators.DataRequired(),
		validators.Length(min=8, max=20)])

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[validators.DataRequired()])
	password = PasswordField('Password', validators=[validators.DataRequired()])