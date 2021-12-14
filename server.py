from enum import unique
from html import entities
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user
from flask_admin import Admin
from sqlite3 import *

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
    return redirect(url_for("generate_feed"))


@app.route('/register', methods= ['GET', 'POST'])
def register(): #Create a new User and subsequent Profile
    print('register')

    if request.method == 'POST':
        username = request.form['username'] #Won't work because of email on newUser
        password = request.form['password']

        return redirect(url_for("newUser"))
    elif request.method == 'GET':
        return render_template("newUser.html")



@app.route('/newUser', methods= ['GET', 'POST'])
def newUser(): #Create the profile and submit to database
    print("new user")

    if request.method == "GET":
        return render_template("edit_profile.html")
    elif request.method == "POST":
        #Retrieve new profile intformation from edit_profile form and INSERT into db

        return redirect(url_for("generate_feed"))

@app.route('/generate_feed', methods= ['GET'])
def generateFeed():
    print("generating feed")
    #Algorithmically generate a feed from follower list
    #GET follower data from database
    return render_template("feed.html")

@app.route('/createPost', methods = ['GET',  'POST'])
def createPost():
    print("creating post")

    if request.method == "GET":
        return render_template("newPost.html")
    elif request.method == "POST":
        #Retrieve post information from newPost.html and INSERT into db
        #Blob a photo.... make null if no photo

        return redirect(url_for("generate_feed"))

@app.route('/viewPost', methods = ['GET'])
def viewPost():
    print("viewing post")
    #Get all post data from db and pass it through render_template

    return render_template("postView.html")

@app.route('/createComment', methods= ['GET', 'POST'])
def createComment():
    print("creating comment")

    if request.method == "GET":
        #You can only access createcomment from postView.html
        #post = request.form["post_id"]

        return render_template("newComment.html")
    elif request.method == "POST":
        #Retrieve post information from newComment.html and INSERT into db
        #Blob a photo.... make null if no photo
        #Don't forget parent post

        return redirect(url_for("generate_feed"))

@app.route('/login', methods =['GET','POST'], endpoint='login')
def Login():
    print('postLogin')
    if request.method == 'GET':
        if(current_user.is_authenticated):
            return redirect(url_for('studentView'))

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
        return redirect(url_for("generate_feed"))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)