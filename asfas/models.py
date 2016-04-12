#!/usr/bin/env python
# -*- coding: utf-8 -*-
# models.py
from asfas import db

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True)
    admin = db.Column(db.Integer)

    def __init__(self, username, password, email, admin=False, active=True):
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin
        self.active = active

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return self.username
