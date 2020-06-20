# -*- coding: utf-8 -*-

# 通常建造一个网站我们需要模板（templates）和静态文件（static files）
# 模板即包含程序页面的 HTML 文件，静态文件则是要在 HTML 文件中加载的 CSS 和 Javascript 文件

# 使用 Flask 扩展
# 扩展即使用 Flask 提供的 API 接口编写的 Python 库，可以为 Flask 提供丰富的功能
# 使用 Flask 扩展时，初始化的步骤大致相同；大部分扩展都会提供一个扩展类，传入 Flask 
# 程序实例实例化这个类即完成初始化过程

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class, ALL
from pypinyin import lazy_pinyin
from flask_mail import Mail

app = Flask(__name__)   # 创建 Flask 程序实例，第一个参数是模块或包的名称；
                        # 此处的 __name__ 表示的是当前文件（模块）的名称 "app"，
                        # 这也帮助 Flask 在相应的文件夹内寻找所需资源

# 项目环境变量配置
# app.config 实际上是字典 dict 的子类，我们可以像操作字典一样来操作它
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
