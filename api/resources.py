from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt,decode_token)
from api.models import User,AuthToken ,PublicDiscussions
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from api.models import app
import requests
import os
import pyqrcode


parser = reqparse.RequestParser()


class UserRegistration(Resource):
    def post(self):
        data = request.json
        if User.find_by_email(data['email']):
            return {'message': 'User with this email {} already exists'.format(data['email'])}, 422
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=User.generate_hash(data['password'])
        )
        # new_user.save_to_db()
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['email'])
            return {
                       'message': 'User {} was created'.format(data['email']),
                       'access_token': access_token,
                   }, 201
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):

    def post(self):
        data = request.json
        current_user = User.find_by_email(data['email'])

        if not current_user:
            return {'message': 'User with these credentials {} doesn\'t exist'.format(data['email'])}, 404

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['email'])
            return {
                       'message': 'Logged in as {}'.format(current_user.email),
                       'access_token': access_token,
                   }, 200
        else:
            return {'message': 'Invalid credentials'}, 401


# recieve emails as list, session ids and generate auth token.
class AuthGenerator(Resource):
    def post(self):
        emaillist = []
        data = request.json
        for i in data['email']:
            new_auth = AuthToken(
                session_id = data['session_id'],
                token = create_access_token(identity=i)
            )
            new_auth.save_to_db()
            emaillist.append("token for {} was created".format(i))

        try:
            return {
                      'messages':emaillist
                  }, 201
        except:
            return {'message': 'Something went wrong'}, 500

class QRGenerator(Resource):
    def post(self):
        data = request.json
        session_id = data['session_id']
        session = AuthToken.find_by_session(session_id=session_id)
        for i in session[session_id]:
            jti = i['token']
            email=decode_token(jti)['identity']
            qr_code = pyqrcode.create(jti, error='L', version=27, mode='binary')
            qr_code.png('qr.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
            AuthToken.send_email(session_id=session_id,email=email)
            os.remove("qr.png")
            return "succesfully sent"

class PublicDiscussion(Resource):
    def get(self):
        return PublicDiscussions.return_all()

