#!/usr/bin/env python
# -*- coding: utf- -*-
# routes.py

from flask import Flask, request, render_template, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required, LoginManager, current_user
from forms import AdminRegistrationForm, LoginForm, EditAdminForm, EditPageForm
from werkzeug import secure_filename
from asfas import app, db, login_manager, CsrfProtect, bcrypt, images
from models import User, Page
import os


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

@app.route('/admin/')
@login_required
def admin_index():
    return render_template('admin_index.html')

@app.route('/admin/users/')
@login_required
def list_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/page/<title>/edit/', methods=['GET', 'POST'])
@login_required
def page_edit(title=None):
    page = Page.query.filter_by(title=title).first()
    if not page:
        return redirect(url_for('admin_index'))
    form = EditPageForm(obj=page)
    form.make_optional(form.header_image)
    form.make_optional(form.content)
    form.make_optional(form.lower_image)
    if request.method == 'POST' and form.validate():
        if form.header_image.data and page.header_image != 'N/A':
            #page.header_image = form.header_image.data
            """
            page.header_image = secure_filename(form.header_image.data.filename)
            #save to app.config['UPLOADED_IMAGES_DEST']
            form.header_image.data.save('asfas/images/' + page.header_image)
            """
            header_image = request.files['header_image']
            page.header_image = secure_filename(form.header_image.data.filename)
            header_image.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], page.header_image))
            """
            header_image = images.save(request.files['header_image'])
            #rec = Image(filename=header_image, user = page.id)
            #rec.store()
            """
        if form.content.data and page.content != 'N/A':
            page.content = form.content.data
        if form.lower_image.data and page.lower_image != 'N/A':
            lower_image = request.files['lower_image']
            page.lower_image = secure_filename(form.lower_image.data.filename)
            lower_image.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], page.lower_image))
        db.session.commit()
        return redirect(url_for('page_view', title=title))
    return render_template('admin_page_edit.html', form=form, page=page)

@app.route('/admin/page/<title>/view/')
@login_required
def page_view(title=None):
    page = Page.query.filter_by(title=title).first()
    if not page:
        return redirect(url_for('admin_index'))
    else:
        return render_template('admin_page_view.html', page=page)
