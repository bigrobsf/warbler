from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from project.models import User
from project.helpers import make_json_response, ensure_correct_user
from project.helpers import jwt_required, authenticate, current_user_id
from project.users.token import generate_confirmation_token, random_password, confirm_token, generate_confirmation_token_assessment
from project import db, bcrypt

users_api = Api(Blueprint('users_api', __name__))

user_with_token_fields = {
    'token': fields.String
}

user_fields = {
  'id': fields.Integer,
  'user_name': fields.String,
  'first_name': fields.String,
  'last_name': fields.String,
  'email': fields.String
}



# user sign up
# user log in
# user log out
# get user
# edit user account
