#!/usr/bin/env python
# -*- coding: utf- -*-
# routes.py

from flask import Flask, request, render_template, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required, LoginManager, current_user
from forms import AdminRegistrationForm, LoginForm, EditAdminForm
from asfas import app, db, login_manager, CsrfProtect, bcrypt
from models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/register/', methods=['GET', 'POST'])
@login_required
def register_admin():
    form = AdminRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=pw_hash, email=form.email.data, \
            admin=True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('admin_index'))
    return render_template('admin_register.html', form=form)

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for('admin_index'))
    return render_template('admin_login.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/admin/edit/', methods=['GET', 'POST'])
@login_required
def edit_admin():
    form = EditAdminForm()
    form.make_optional(form.email)
    form.make_optional(form.password)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=str(current_user)).first()
        if form.email.data and user.email != form.email.data:
            user.email = form.email.data
        if form.password.data and not bcrypt.check_password_hash(user.password, form.password.data):
            pw_hash = bcrypt.generate_password_hash(form.password.data)
            user.password = pw_hash
        db.session.commit()
        return redirect(url_for('admin_index'))
    return render_template('admin_edit.html', form=form)

@app.route('/admin/index')
@login_required
def admin_index():
    return render_template('admin_index.html')

@app.route('/admin/users/')
@login_required
def list_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

