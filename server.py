from enum import unique
from html import entities
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user
from flask_admin import Admin
from sqlite3 import *


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    
app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'secret-key'
admin = Admin(app)



@app.route('/')
def index():
    print('landing')
    if(not current_user.is_authenticated):
        print('not_auth')
        return redirect(url_for('login'))
    print('authenticated')
    return render_template('studentView.html')

@app.route('/index')
def deez():
    print('bofa')
    return 'bofa'

@app.route('/login', methods =['GET','POST'], endpoint='login')
def Login():
    print('postLogin')
    if request.method == 'GET':
        if(current_user.is_authenticated):
            return redirect(url_for('studentView.html'))
        return render_template('login.html')

    if request.method == 'POST':
        print(request.form['username'])
        user = Users.query.filter_by(username = request.form['username'])
        if user is None:
            return redirect(url_for('login'))
        
        user = user.first()
        
        if user is None:
            return redirect(url_for('login'))

        if not user.checkPassword(request.form['password']):
            return redirect(url_for('login'))

        login_user(user)
        print (user.userLevel)
        return render_template('studentView.html',userid = user.id)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)