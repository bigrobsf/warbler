import jwt
from functools import wraps
from flask import abort, request, make_response, jsonify, json
from project.models import User
from project import bcrypt
from jwt.exceptions import DecodeError
from project.users.token import confirm_token

def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if user:
        if bcrypt.check_password_hash(user.password, password):
            token = jwt.encode({'id': user.id}, 'secret',
                               algorithm='HS256').decode('utf-8')
            return token

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get('authorization'):
            split_token = request.headers.get('authorization').split(" ")[1]
        try:
            token = jwt.decode(split_token, 'secret', algorithm='HS256')
            if token:
                return fn(*args, **kwargs)
        except DecodeError as e:
            return abort(401, 'Please log in again')
        except UnboundLocalError as e:
            return abort(401, 'Please log in again')
        return abort(401, 'Please log in')
    return wrapper

def current_user_id():
    if request.headers.get('authorization'):
        split_token = request.headers.get('authorization').split(" ")[1]
    try:
        token = jwt.decode(split_token, 'secret', algorithm='HS256')
        return token.get('id')
    except DecodeError as e:
        return None

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get('authorization'):
            split_token = request.headers.get('authorization').split(" ")[1]
        try:
            token = jwt.decode(split_token, 'secret', algorithm='HS256')
            correct_user = kwargs.get('user_id') == token.get('id')
            if correct_user or token:
                return fn(*args, **kwargs)
        except UnboundLocalError as e:
            return abort(401, 'Please log in again')
        except DecodeError as e:
            return abort(401, 'Please log in again')
        return abort(401, 'Unauthorized')
    return wrapper

def _user_login(self, username, password):
    return self.client.post(
        'api/users/auth',
        content_type='application/json',
        data=json.dumps({
            'username': username,
            'password': password
        })).json

def make_json_response(message, status_code=200):
    return make_response(jsonify({
        'message': message
    }), status_code)
