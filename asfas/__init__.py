#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __init__.py

from flask import Flask
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import socket

app = Flask(__name__)

#if __name__ == '__main__':
if socket.gethostname() == 'kth.site':
    app.config.from_object('dev_settings')
else:
    app.config.from_object('prod_settings')

login_manager = LoginManager()
login_manager.init_app(app)
CsrfProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

import asfas.admin_routes
import asfas.routes
