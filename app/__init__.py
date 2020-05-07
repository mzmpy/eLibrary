# -*- coding: utf-8 -*-

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class, ALL
from pypinyin import lazy_pinyin
from flask_mail import Mail

app = Flask(__name__)

# 环境变量配置
app.config.from_object(Config)

# 数据库组件配置
db = SQLAlchemy(app) # 将 Flask 应用和数据库绑定
migrate = Migrate(app, db) # 数据库迁移引擎

# 登录组件配置
login = LoginManager(app)
login.login_view = 'login'

# 文件上传组件配置
allowed_files = UploadSet(extensions=ALL) # 支持所有文件类型的上传
configure_uploads(app, allowed_files)
patch_request_class(app, 512 * 1024 * 1024) # 文件最大上传大小为 512Mb

# 创建邮件实例
mail = Mail(app)

from app import routes, models
