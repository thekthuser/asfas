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

