# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, send_from_directory, make_response
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, allowed_files, lazy_pinyin
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User, File
import os
import re
from app.email_verification import send_register_verification_email

@app.route('/')
def home():
    files = File.query.all()

    def rows(obj):
        return int(len(obj) * 8 / 101)
    
    def calcsize(filesize):
        if filesize < 100:
            return '{}B'.format(filesize)
        elif filesize < 1024*1024*0.9:
            return '{:.2f}KB'.format(filesize/1024)
        else:
            return '{:.2f}MB'.format(filesize/1024/1024)

    # for file in files:
    #     print(len(file.abstract))
    # print(current_user.username)
    return render_template('home.html', files=files, rows=rows, calcsize=calcsize)


@app.route('/download/<filename>', methods=['GET'])
@login_required
def download(filename):
        file = File.query.filter_by(filename=filename).first()
        return send_from_directory(app.config['UPLOADED_FILES_DEST'], file.filename, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'无效的用户名或密码！', 'warning')
            return redirect('/login')
        if not user.verification:
            send_register_verification_email(user)
            flash(u'用户未验证！请注意查收用户验证邮件！', 'warning')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/'
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect('/')
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_register_verification_email(user)
        flash(u'注册成功！但是请注意：请先到您的注册邮箱完成验证再登录！', 'success')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/register_verification/<token>', methods=['GET', 'POST'])
def rigister_verification(token):
    user = User.verify_register_verification_token(token)
    if not user:
        return render_template('cannot_verify.html', title='Not_Verified')
    user.verification = True
    db.session.commit()
    return render_template('verify_successfully.html', title='Verified', user=user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/manage')
def manage():

    def rows(obj):
        return int(len(obj) * 8 / 101)
    
    def calcsize(filesize):
        if filesize < 100:
            return '{}B'.format(filesize)
        elif filesize < 1024*1024*0.9:
            return '{:.2f}KB'.format(filesize/1024)
        else:
            return '{:.2f}MB'.format(filesize/1024/1024)

    return render_template('manage.html', title='Manage', rows=rows, calcsize=calcsize)


@app.route('/delete/<filename>/<sfilename>')
def delete(filename, sfilename):
    # print(filename, sfilename)
    for file in current_user.files:
        if filename == file.filename and sfilename == file.source_filename:
            db.session.delete(file)
            db.session.commit()
            os.remove(file.filepath)
            break
    return redirect(url_for('manage'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        source_filename = form.uploaded_file.data.filename
        py = lazy_pinyin(form.uploaded_file.data.filename)

        filename = ''

        if current_user.is_anonymous:
            is_free = True
        elif current_user.is_authenticated:
            # print(form.is_free.data)
            is_free = form.is_free.data
            if not is_free:
                filename = filename + 'By-{}-'.format(current_user.username)

        for n in py:
            filename += n
        form.uploaded_file.data.filename = filename

        try:
            filename = allowed_files.save(form.uploaded_file.data)
        except:
            flash(u'文件 {} 上传失败！'.format(source_filename), 'warning')
            return redirect('/upload')
        
        filepath = allowed_files.path(filename)
        abstract = form.abstract.data if form.abstract.data else "目前还没有介绍哦！"
        size = os.path.getsize(filepath)
        saved_file = File(source_filename = source_filename, filename=filename, abstract=abstract, filepath=filepath, size=size, is_free=is_free)
        
        if current_user.is_authenticated:
            current_user.files.append(saved_file)
        
        db.session.add(saved_file)
        db.session.commit()
        flash(u'文件 {} 上传成功！'.format(source_filename), 'success')
        return redirect('/upload')
    return render_template('upload.html', title='Upload File', form=form)

