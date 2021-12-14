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

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'secret-key'
admin = Admin(app)
db = SQLAlchemy(app)


def file_to_BLOB(filename):
    with open(filename, "rb") as file:
        blobData = file.read()
    return blobData

#Connect to database
connection = sqlite3.connect('database.db', check_same_thread=False)
cur = connection.cursor()

class Users(UserMixin,db.Model): 
    id = db.Column(db.Integer, primary_key=True) 

    def __repr__(self): 
        return '<Users %r>' % self.username


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)



@app.route('/')
def index():
    print('landing')
    if(not current_user.is_authenticated):
        print('not_auth')
        return redirect(url_for('login'))
    print('authenticated')
    return redirect(url_for("generateFeed"))


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

        return redirect(url_for("generateFeed"))

@app.route('/generateFeed', methods= ['GET'])
def generateFeed():
    print("generating feed")
    #Algorithmically generate a feed from follower list
    target_profile_id = current_user.get_id()
    
    cur.execute('SELECT following_list FROM profile WHERE id=:id', {"id": target_profile_id})
    result = cur.fetchone()
    following_list = result[0].split(",")
    following_list.pop(-1) #Remove the empty last element

    post_list = []
    for profile_id in following_list:
        cur.execute('SELECT post_list, pfp, screenname FROM profile WHERE id=:id', {"id": profile_id})
        result = cur.fetchone()

        if result is not None:
            post_id_list = result[0].split(",")
            post_id_list.pop(-1)

            pfp = base64.b64encode(result[1]).decode('utf-8')
            author = result[2]


            cur.execute('SELECT * FROM posts where posts.id=:id', {"id": post_id_list[-1]})
            result = cur.fetchone()
            if result is not None:
                post = []
                for value in result:
                    post.append(value)

                post[2] = base64.b64encode(post[2]).decode('utf-8')
                post.append(pfp)
                post.append(author)
                post_list.append(post)

    #GET follower data from database
    print(len(post_list))
    return render_template("feed.html", post_list=post_list)

@app.route('/createPost', methods = ['GET',  'POST'])
def createPost():
    print("creating post")

    if request.method == "GET":
        return render_template("newPost.html")
    elif request.method == "POST":
        #Retrieve post information from newPost.html and INSERT into db
        #Blob a photo.... make null if no photo
        inputted_image = request.files["post-image"].read()
        print(inputted_image)
        inputted_textarea = request.form["text_content"]

        cur.execute("""INSERT INTO posts (media_content, text_content,num_likes,num_dislikes,comment_list,date_posted,author_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                        (inputted_image, inputted_textarea, 0, 0, "0,", "12/14/2021", current_user.get_id()))

        connection.commit()

        cur.execute('SELECT id FROM posts')
        all_posts = cur.fetchall()
        print(all_posts[-1][0])

        cur.execute('SELECT post_list FROM profile WHERE id=:id', {"id": current_user.get_id()})
        post_list_string = cur.fetchone()[0]

        post_list_string = post_list_string + str(all_posts[-1][0]) + ","

        cur.execute('UPDATE profile SET post_list=:post_string WHERE id=:id', {"post_string": post_list_string, "id": current_user.get_id()})

        return redirect(url_for("generateFeed"))


@app.route("/viewProfile", methods = ['GET'])
def viewProfile():
    print("viewing Profile")

    #retreive screenname...
    target_profile_id = current_user.get_id()

    cur.execute('SELECT pfp, screenname, follower_list, following_list, bio, post_list FROM profile WHERE id=:id', {"id": target_profile_id})
    result = cur.fetchone()
    if result is None:
        #maybe an error profile page... like deleted profile... probably redirect back to wherever you came
        pass

    pfp = base64.b64encode(result[0]).decode('utf-8')
    screenname = result[1]
    follower_string = result[2]
    following_string = result[3]
    bio = result[4]
    string_post_list = result[5] #TODO: convert string to post_ids

    #get counts on follower/following strings
    follower_count = len(follower_string.split(",")) - 1
    following_count = len(following_string.split(",")) - 1

    print(string_post_list)

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


@app.route('/login', methods =['GET','POST'], endpoint='login')
def Login():

    print('postLogin')
    if request.method == 'GET':
        if(current_user.is_authenticated):
            return redirect(url_for('viewProfile'))

        return render_template('login.html')

    if request.method == 'POST':
        inputted_username = request.form["username"]
        inputted_password = request.form["password"]

        #INSERT login logic... retrieve username and password from db
        cur.execute('SELECT * FROM users WHERE username=:username AND password=:password', {"username": inputted_username, "password": inputted_password})
        ogLogin =""
        result = cur.fetchone()

        if result is None:
            result = cur.execute('SELECT username FROM users WHERE username=:username',{"username":inputted_username}).fetchone()
            ogLogin = result
            print(result)
            if result is None:
                flash('User not found. Try Registering?')
                return redirect(url_for("login"))
            flash('Username or password is incorrect')
            return redirect(url_for("login"))
        user = Users()
        user.id = result[0]
        login_user(user)

        return redirect(url_for("generateFeed"))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)