#!/usr/bin/env python
# -*- coding: utf-8 -*-
# forms.py

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms import validators, ValidationError
from models import User
from asfas import bcrypt

class AdminRegistrationForm(Form):
    class Meta:
        model = User

    def username_unique(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            return True
        else:
            raise ValidationError('This username is not available.')

    username = TextField('Username', [validators.DataRequired(), \
        validators.Length(min=4, max=35), username_unique])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired(), \
        validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    class Meta:
        model = User

    def check_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            raise ValidationError('Incorrect username.')
        return True

    def check_password(form, field):
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, field.data):
            return True
        raise ValidationError('Incorrect password.')

    username = TextField('Username', [validators.DataRequired(), check_username])
    password = PasswordField('Password', [validators.DataRequired(), check_password])
