from flask import Flask, jsonify, request, session, redirect

from passlib.hash import pbkdf2_sha256

# 데이터베이스에 사용자 정보를 넣기 위해 app에 있는 db를 가져온다.
from app import db

import uuid

class User:

    def start_session(self, user):
        # 사용된 패스워드만 삭제
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        print(request.form)

        # 사용자 정보 가져오기 - form에 입력된 이름, 이메일, 비밀번호를 가져온다.
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # 비밀번호를 암호화한다.
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # db에 넣기 전에 이메일 중복 검사한다.
        if db.users.find_one({ "email": user['email']}):
            return jsonify({ "error": "Email address already in use"}), 400

        # db에 사용자 정보를 넣는다.
        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({ "error": "Signup failed" }), 400
    
    # 로그아웃 - 세션 초기화
    def signout(self):
        session.clear()
        return redirect('/')
    
    # 로그인 처리 함수
    def login(self):

        user = db.users.find_one({
        "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
    
        return jsonify({ "error": "Invalid login credentials" }), 401