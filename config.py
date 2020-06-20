# -*- coding: utf-8 -*-

import os

# Flask 中环境变量变量一般使用大写字母形式

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FILES_PER_PAGE = 10
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-key'

    # SQLALCHEMY_DATABASE_URI配置变量记录应用的数据库的位置
    # Sqlite连接字符串中的/斜杠说明：三斜杠表示相对路径，四斜杠表示绝对路径
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS配置项用于设置数据发生变更之后
    # 是否发送信号给应用，我们不需要这个功能
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_FILES_DEST = os.path.join(os.getcwd(), 'saved_files')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['littlenodot3@gmail.com']
