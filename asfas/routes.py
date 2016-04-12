#!/usr/bin/env python
# -*- coding: utf- -*-
# routes.py

from flask import Flask
from asfas import app

@app.route('/')
def index():
    return 'index'
