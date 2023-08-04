from flask import Flask
from app import app
from user.models import User

# 회원가입 - POST
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

# 로그아웃  
@app.route('/user/signout')
def signout():
    return User().signout()

# 로그인 - POST
@app.route('/user/login', methods=['POST'])
def login():
    return User().login()
