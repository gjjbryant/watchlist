'''
@Author: your name
@Date: 2019-12-11 10:02:11
@LastEditTime: 2019-12-13 14:00:15
@LastEditors: Please set LastEditors
@Description: In User Settings Edit      初始化
@FilePath: \watchlist\watchlist\__init__.py
'''
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# ...

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gjj123456@127.0.0.1:3306/flask?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap()
bootstrap.init_app(app)
moment = Moment(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import views, errors, commands