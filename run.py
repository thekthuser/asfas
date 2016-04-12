#!/usr/bin/env python
# -*- coding: utf-8 -*-
# run.py

from flask import Flask
import socket
from asfas import app

if __name__ == '__main__':
    if socket.gethostname() == 'kth.site':
        app.config.from_object('dev_settings')
    else:
        app.config.from_object('prod_settings')
    app.run()
