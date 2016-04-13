#!/usr/bin/env python
# -*- coding: utf- -*-
# routes.py

from flask import Flask, request, render_template, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required, LoginManager
from forms import AdminRegistrationForm, LoginForm
from asfas import app, db, login_manager, CsrfProtect, bcrypt
from models import User

@app.route('/')
def index():
    return render_template('index.html')

@login_required
@app.route('/admin/register/', methods=['GET', 'POST'])
def register_admin():
    form = AdminRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=pw_hash, email=form.email.data, \
            admin=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return 'User created.'
    return render_template('admin_register.html', form=form)

@app.route('/admin/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('admin_login.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
