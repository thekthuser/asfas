#!/usr/bin/env python
# -*- coding: utf- -*-
# routes.py

from flask import Flask, request, render_template, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required, LoginManager, current_user
from forms import AdminRegistrationForm, LoginForm, EditAdminForm
from asfas import app, db, login_manager, CsrfProtect, bcrypt
from models import User, Page

@app.route('/')
def index():
    page = Page.query.filter_by(title='home').first()
    return render_template('page.html', page=page)

@app.route('/page/<title>/')
def page(title=None):
    if title == None:
        return redirect(url_for('index'))
    page = Page.query.filter_by(title=title).first()
    return render_template('page.html', page=page)


