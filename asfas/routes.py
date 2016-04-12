#!/usr/bin/env python
# -*- coding: utf- -*-
# routes.py

from flask import Flask, request, render_template
from flask.ext.login import login_user, logout_user, login_required, LoginManager
from forms import AdminRegistrationForm
from asfas import app, db, login_manager, CsrfProtect, bcrypt
from models import User

@app.route('/')
def index():
    return 'index'

#@login_required
@app.route('/admin/register/', methods=['GET', 'POST'])
def register_admin():
    form = AdminRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=pw_hash, email=form.email.data, \
            admin=True)
        db.session.add(user)
        db.session.commit()
        return 'User created.'
    return render_template('admin_register.html', form=form)
