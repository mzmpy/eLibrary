# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.routes import current_user
from app.models import User, File
from app import allowed_files

class LoginForm(FlaskForm):
    """创建登录表格的类"""
    username = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住用户')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    """创建注册表格的类"""
    username = StringField('账号', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '再次输入密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户已存在！')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('这个邮箱已被使用！')


class UploadForm(FlaskForm):
    """创建文件上传表格的类"""
    uploaded_file = FileField('选择文件', validators=[FileAllowed(allowed_files), FileRequired('未选择文件')])
    abstract = TextAreaField('简介')
    is_free = BooleanField('上传为公共文件')
    submit = SubmitField('上传')

    def validate_uploaded_file(self, uploaded_file):
        files = File.query.filter_by(source_filename=uploaded_file.data.filename).all()
        if files is not None:
            for file in files:
                if self.is_free.data and file.is_free:
                    # print(self.is_free)
                    raise ValidationError('公共文件已存在！改换文件名可继续上传！')
                elif not self.is_free.data and file.uploader.username == current_user.username and not file.is_free:
                    raise ValidationError('个人文件已存在！改换文件名可继续上传！')

    