# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask_pymongo import PyMongo
import os # if you haven't already
from dotenv import load_dotenv

# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'music'

# URI of database

# first load environment variables in .env
load_dotenv()

# then store environment variables with new names
USER = os.getenv("MONGO_USERNAME")
PASS = os.getenv("MONGO_PASSWORD")

app.config['MONGO_URI'] = 'mongodb+srv://'+USER+':'+PASS+'@cluster0-qzpzt.mongodb.net/music?retryWrites=true&w=majority'

mongo = PyMongo(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# My Name


# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

#SIGNUP
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            users.insert({'username' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Try logging in.'

    return render_template('signup.html')

# LOGIN

@app.route('/login', methods = ['POST'])
def login(): 
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})
    if login_user: 
        if request.form['password']==login_user['password']:
            session['username'] = request.form['username']
            return redirect (url_for('index'))
    return 'invalid password/username combination'

#LOGOUT

@app.route('/logout')
def logout():
    session.clear()   
    return redirect('/')

# ADD SONGS
@app.route('/add', methods=['GET', 'POST'])
def add():
    # define a variable for the collection you want to connect to
    song = mongo.db.songs
    users = mongo.db.users

    if request.method == 'GET':
        return "Go to the landing page to add a song!"
    else:
        mySong = request.form['mySong']
        artist = request.form['artist'] 
        description = request.form['description']
        if session:
            name = session['username']
            song.insert({'song': mySong, 'artist': artist, 'description': description, 'name': name})
        else: 
            song.insert({'song': mySong, 'artist': artist, 'description': description})

        print(request.form) # Demo that it defaults to an ImmutableMultiDict datatype.
        return redirect ('/show')

# Create a new route that shows a list of all of the song titles in your collection.

@app.route('/show')
def show():
    collection = mongo.db.songs
    data = list(collection.find({}).sort("artist"))
    return render_template('show.html', data=data)
# SHOW A LIST OF ALL SONG TITLES


# ADVANCED: A FORM TO COLLECT USER-SUBMITTED SONGS




# DOUBLE-ADVANCED: SHOW ARTIST PAGE




# TRIPLE-ADVANCED: SHOW SONG PAGE
