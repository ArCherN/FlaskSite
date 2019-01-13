# -*- coding: utf-8 -*-

from flask import jsonify, render_template, request, redirect, flash, url_for
from app import app, custom_API, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.get(current_user.username)
    posts = Post.query.all()
    if not posts:
        posts = [{'author': {'username': 'nobody'}, 'body': 'Тут пока ничего нет...'}]
    return render_template("index.html", title='Home', posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/script/get_wo')
@login_required
def get_work_order():
    return render_template("about.html")


@app.route('/add')
@login_required
def addnum():
    return render_template("/_add_number.html")


@app.route('/_add_numbers')
@login_required
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/learning')
@login_required
def learn():
    buttons = custom_API.Methods.getButton('')
    return render_template('learn.html', buttons=buttons)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    if username != current_user.username:
        return redirect(url_for('user', username=current_user.username))
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)