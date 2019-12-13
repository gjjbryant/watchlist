'''
@Author: your name
@Date: 2019-12-11 10:08:35
@LastEditTime: 2019-12-13 14:00:52
@LastEditors: Please set LastEditors
@Description: In User Settings Edit         网页视图文件
@FilePath: \watchlist\watchlist\views.py
'''
from flask import render_template, request, url_for, redirect, flash   #使用 render_template() 函数可以把模板渲染出来，必须传入的参数为模板文件名（相对于 templates 根目录的文件路径）
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie

from  watchlist.models import Message
from  watchlist.form import HelloForm



@app.route('/', methods=['GET', 'POST']) #index页面默认只接受GET请求 所以增加POST请求  index 主页
def index():
    if request.method == "POST":
        if not current_user.is_authenticated:# 如果当前用户未认证
             return redirect(url_for('index'))  # 重定向到主页
        #获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invaild input.')
            return redirect(url_for('index')) #重定向回主页
        # 保存表单数据都数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)  

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST']) #编辑页面
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            current_user.name = user.name
            flash('login success! welcome ' + user.username + '!')
            return redirect(url_for('index')) 
            
        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['Confirmpassword']

        user = User.query.filter_by(username=username).first()

        if user is not None:
            flash('register fail!  this username already exsit!')
            return redirect(url_for('register')) 
        if password != confirmpassword:
            flash('Two password entries are inconsistent!')
            return redirect(url_for('register')) 
        
        user = User(username=username, name=username)
        user.set_password(password)
        db.session.add(user)

        db.session.commit()
        flash('register success!')   # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面
    
    return render_template('register.html')

@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()
    flash('GoodBye.')
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/message' ,methods=['GET', 'POST'])
@login_required
def message():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('message'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('message.html', form=form, messages=messages)
