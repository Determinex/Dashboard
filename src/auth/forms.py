# ------------------------------------------------------------------------------ #
# File: src/auth/forms.py                                                        #
# Project: Dashboard                                                             #
# File Created: 2025-02-14 11:00:00                                              #
# Last Mod Date: 2025-02-14 11:00:00                                             #
# Last Mod By: Determinex                                                        #
# ------------------------------------------------------------------------------ #
# Component of: src/__init__.py                                                  #
# Used in: src/auth/routes.py, templates, static                                 #
# Description: This file contains the form elements for login and registration   #
# Content: Contains the form elements for login and registration page elements   #
# --- used in the header & navigation html page template components utilized by  #
# --- Jinja2 templating engine in the Flask web application.                     #
# ------------------------------------------------------------------------------ #

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from src.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_password(self, password):
        user = User.query.filter_by(password=password.data).first()
        if user is not None:
            raise ValidationError('Please use a different password.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class BookmarkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    folder_id = SelectField('Folder', coerce=int)  # Choices populated in the route
    tag_id = SelectField('Tag', coerce=int)  # Choices populated in the route
    submit = SubmitField('Save Bookmark')