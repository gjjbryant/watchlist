'''
@Author: your name
@Date: 2019-12-11 10:13:45
@LastEditTime: 2019-12-11 10:14:05
@LastEditors: Please set LastEditors
@Description: In User Settings Edit         错误视图处理页面
@FilePath: \watchlist\watchlist\errors.py
'''
from flask import render_template

from watchlist import app


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500