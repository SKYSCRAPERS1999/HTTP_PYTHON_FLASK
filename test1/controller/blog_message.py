from test1.model.models import User, Category
from flask import Flask, request, url_for, render_template, redirect, flash, sessions, session, abort
from test1 import app, db
from flask_login import current_user, login_user, logout_user, login_required
from test1.model.forms import LoginForm, RegistrationForm
from datetime import datetime

@app.route('/')
def show_entries():
    if current_user.is_anonymous:
        categorys = None
    else:
        categorys = Category.query.filter_by( user_id=current_user.id ).all()
    return render_template('show_entries.html', entries=categorys)

@app.route('/add_entry',methods=['POST'])
@login_required
def add_entry():
    title = request.form['title']
    content = request.form['content']
    author = User.query.get(current_user.id)
    category = Category(title,content,author)
    db.session.add(category)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(show_entries))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.password != form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('show_entries'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/register', methods=['Get','Post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(show_entries))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        entries = [
            {'author':user, 'title' : 'Test post #1', 'content' : 'the last day of winter vacation!'},
            {'author':user, 'title': 'Test post #2', 'content': 'the last day of winter vacation!!!'}
        ]
        return render_template('user.html', user=user, entries = entries)
    else:
        flash('Permission denied')
        return redirect(url_for('show_entries'))

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()