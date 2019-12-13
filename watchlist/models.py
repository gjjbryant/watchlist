'''
@Author: your name
@Date: 2019-12-11 10:04:02
@LastEditTime: 2019-12-13 13:36:24
@LastEditors: Please set LastEditors
@Description: In User Settings Edit       模型
@FilePath: \watchlist\watchlist\models.py
'''
# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from watchlist import db


class User(db.Model,UserMixin):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20)) #用户名
    password_hash = db.Column(db.String(128)) # 密码散列值

    def set_password(self,password):
        self.password_hash = generate_password_hash(password) # 将生成的密码保持到对应字段
    
    def validate_password(self,password):                     # 用于验证密码的方法，接 受密码作为参数
        return check_password_hash(self.password_hash,password)
    

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份



#留言板信息
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)