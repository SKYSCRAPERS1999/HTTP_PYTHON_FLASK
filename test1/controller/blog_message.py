from test1.model.models import User, Category
from flask import Flask, request, url_for, render_template, redirect, flash, sessions, session, abort
from test1 import app, db

@app.route('/')
def show_entries():
    categorys = Category.query.all()
    return render_template('show_entries.html', entries=categorys)

@app.route('/add_entry',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    content = request.form['content']
    category = Category(title,content)
    db.session.add(category)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print([username, password])
        if username == "impulse" and password == "123456":
            session["logged_in"] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else:
            flash('Wrong username or password!')
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)