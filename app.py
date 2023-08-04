
from flask import Flask, render_template, session, redirect
from functools import wraps


# mongoDB
import pymongo

app = Flask(__name__)

app.secret_key = b'\xf6e\xa5S\xef\xd4g\xdbT\xeb\x9d\xc8\x9e\xc6\xab\xcd'

# mongodb 포트 연결
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system


# 로그인 필수 - 메인 페이지에 접근을 막는다.
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/')
    return wrap

# Routes
from user import routes


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup')
def signuppage():
    return render_template('signup.html')