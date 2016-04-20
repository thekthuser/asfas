#!/usr/bin/env python
# -*- coding: utf-8 -*-
# forms.py

from flask.ext.wtf import Form
from wtforms import PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms import validators, ValidationError
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.ext.uploads import UploadSet, IMAGES
from models import User, Page
from asfas import bcrypt, images

#images = UploadSet('images', IMAGES)


class AdminRegistrationForm(Form):
    class Meta:
        model = User

    def username_unique(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            return True
        else:
            raise ValidationError('This username is not available.')

    username = StringField('Username', [validators.DataRequired(), \
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

    username = StringField('Username', [validators.DataRequired(), check_username])
    password = PasswordField('Password', [validators.DataRequired(), check_password])


class EditAdminForm(Form):
    class Meta:
        model = User

    def make_optional(form, field):
        field.validators.insert(0, validators.Optional())

    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired(), \
        validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')


class EditPageForm(Form):
    class Meta:
        model = Page

    def make_optional(form, field):
        field.validators.insert(0, validators.Optional())

    header_image = FileField('Header Image', [FileAllowed(images)])
    content = StringField('Page Content', widget=TextArea())
    lower_image = FileField('Lower Image', [FileAllowed(images)])
