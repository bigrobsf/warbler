from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from project.models import Warble
from project.helpers import make_json_response, ensure_correct_user
from project import db, bcrypt

warbles_api = Api(Blueprint('warbles_api', __name__))

warble_fields = {
  'id': fields.Integer,
  'warble': fields.String,
  'user_id': fields.Integer
}