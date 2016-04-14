#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __init__.py

from flask import Flask
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
CsrfProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

import asfas.admin_routes
