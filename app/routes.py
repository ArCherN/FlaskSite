# -*- coding: utf-8 -*-

from flask import jsonify, render_template, request, redirect, flash, url_for
from app import app, custom_API
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/script/get_wo')
def get_work_order():
    return render_template("about.html")

@app.route('/add')
def addnum():
    return render_template("/_add_number.html")

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/learning')
def learn():
    buttons = custom_API.Methods.getButton('')
    return render_template('learn.html', buttons=buttons)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect (url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
