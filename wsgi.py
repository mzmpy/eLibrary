# -*- coding: utf-8 -*-

# Flask 会自动搜寻程序实例，自动搜寻需要符合以下规则：
# 1. 从当前目录寻找 app.py 和 wsgi.py 模块，并从中寻找名为 app 或 application 的程序实例
# 2. 从环境变量 FLASK_APP 对应的模块名 / 导入路径寻找名为 app 或 application 的程序实例

import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
if os.path.exists(dotenv_path):    
    load_dotenv(dotenv_path)
from app import app
