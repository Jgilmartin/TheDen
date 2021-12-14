from enum import unique
from html import entities
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user
from flask_admin import Admin
import sqlite3
from sqlite3 import *

from PIL import Image
import base64
import io
import numpy as np
import hashlib

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'secret-key'
admin = Admin(app)

# Connect to database
connection = sqlite3.connect('database.db', check_same_thread=False)
cur = connection.cursor()


@login_manager.user_loader
def load_user(id):
    cur.execute("SELECT username FROM users WHERE profile_id=:id", {"id": id})
    user = cur.fetchone()
    return user[0]


@app.route('/')
def index():
    print('landing')
    if(not current_user.is_authenticated):
        print('not_auth')
        return redirect(url_for('login'))
    print('authenticated')
    return redirect(url_for("generateFeed"))


@app.route('/register', methods=['GET', 'POST'])
def register():  # Create a new User and subsequent Profile
    print('register')

    if request.method == 'POST':
        # Won't work because of email on newUser
        username = request.form['new-username']
        password = request.form['new-password']

        password = hashlib.pbkdf2_hmac('sha224',)

        return redirect(url_for("newUser"))
    elif request.method == 'GET':
        return render_template("newUser.html")


@app.route('/newUser', methods=['GET', 'POST'])
def newUser():  # Create the profile and submit to database
    print("new user")

    if request.method == "GET":
        return render_template("edit_profile.html")
    elif request.method == "POST":
        # Retrieve new profile intformation from edit_profile form and INSERT into db

        return redirect(url_for("generateFeed"))


@app.route('/generateFeed', methods=['GET'])
def generateFeed():
    print("generating feed")
    # Algorithmically generate a feed from follower list
    # GET follower data from database
    return render_template("feed.html")


@app.route('/createPost', methods=['GET',  'POST'])
def createPost():
    print("creating post")

    if request.method == "GET":
        return render_template("newPost.html")
    elif request.method == "POST":
        # Retrieve post information from newPost.html and INSERT into db
        # Blob a photo.... make null if no photo

        return redirect(url_for("generateFeed"))


@app.route('/viewPost', methods=['GET'])
def viewPost():
    print("viewing post")
    # Get all post data from db and pass it through render_template

    return render_template("postView.html")


@app.route('/createComment', methods=['GET', 'POST'])
def createComment():
    print("creating comment")

    if request.method == "GET":
        # You can only access createcomment from postView.html
        #post = request.form["post_id"]

        return render_template("newComment.html")
    elif request.method == "POST":
        # Retrieve post information from newComment.html and INSERT into db
        # Blob a photo.... make null if no photo
        # Don't forget parent post

        return redirect(url_for("generateFeed"))


@app.route("/viewProfile", methods=['GET'])
def viewProfile():
    print("viewing Profile")

    # retreive screenname...
    default = "bofadeezSlayer"

    cur.execute('SELECT pfp, screenname, follower_list, following_list, bio, post_list FROM profile WHERE screenname=:screenname', {
                "screenname": default})
    result = cur.fetchone()
    if result is None:
        # maybe an error profile page... like deleted profile... probably redirect back to wherever you came
        pass

    pfp = base64.b64encode(result[0]).decode('utf-8')
    screenname = result[1]
    follower_string = result[2]
    following_string = result[3]
    bio = result[4]
    string_post_list = result[5]  # TODO: convert string to post_ids

    # get counts on follower/following strings
    follower_count = len(follower_string.split(",")) - 1
    following_count = len(following_string.split(",")) - 1

    post_ids = string_post_list.split(",")
    post_ids.pop(-1)

    post_list = []
    for pid in post_ids:
        cur.execute('SELECT * FROM posts WHERE id=:id', {"id": pid})
        result = cur.fetchone()
        if result is not None:
            post = []
            for value in result:
                post.append(value)

            post[2] = base64.b64encode(post[2]).decode('utf-8')
            post_list.append(post)

    print(len(post_list))

    return render_template("profile.html", img_data=pfp,
                           screen_name=screenname, follow_count=follower_count, following_count=following_count, bio_text=bio, post_list=post_list)


@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def Login():

    print('postLogin')
    if request.method == 'GET':
        if(current_user.is_authenticated):
            return redirect(url_for('viewProfile'))

        return render_template('login.html')

    if request.method == 'POST':
        inputted_username = request.form["username"]
        inputted_password = request.form["password"]

        # INSERT login logic... retrieve username and password from db
        cur.execute('SELECT username, password FROM users WHERE username=:username AND password=:password', {
                    "username": inputted_username, "password": inputted_password})
        ogLogin = ""
        result = cur.fetchone()
        if result is None:
            result = cur.execute('SELECT username FROM users WHERE username=:username', {
                                 "username": inputted_username}).fetchone()
            ogLogin = result
            print(result)
            if result is None:
                print('user notfound')
                flash('User not found. Try Registering?')
                return redirect(url_for("login"))
            flash('Username or password is incorrect')
            return redirect(url_for("login"))
        login_user(ogLogin)

        return redirect(url_for("generateFeed"))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
