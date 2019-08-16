#/src/views/UserView

from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

@user_api.route('/create_user', methods=['POST'])
def create():
  """
  Create User Function
  """
  req_data = request.get_json()
  data, error = user_schema.load(req_data)

  if error:
    return custom_response(error, 400)
  
  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_username(data.get('username'))
  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)
  
  user = UserModel(data)
  user.save()
  ser_data = user_schema.dump(user).data
  token = Auth.generate_token(ser_data.get('user_id'))
  return custom_response({'jwt_token': token}, 201)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@user_api.route('/master_user', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get all users
  """
  users = UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True).data
  return custom_response(ser_users, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@user_api.route('/view_user', methods=['POST'])
@Auth.auth_required
def get_a_user():
  """
  Get a single user
  """
  req_data = request.get_json()
  user = UserModel.get_one_user(req_data['user_id'])
  if not user:
    return custom_response({'error': 'user not found'}, 404)
  
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@user_api.route('/update_user', methods=['POST'])
@Auth.auth_required
def update():
  """
  Update me
  """
  req_data = request.get_json()
  data, error = user_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)

  user = UserModel.get_one_user(g.user.get('user_id'))
  user.update(data)
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)
#-------------------------------------------------------------------------
#endregion
#-------------------------------------------------------------------------
@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  """
  Delete a user
  """
  user = UserModel.get_one_user(g.user.get('user_id'))
  user.delete()
  return custom_response({'message': 'deleted'}, 204)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@user_api.route('/me', methods=['POST'])
@Auth.auth_required
def get_me():
  """
  Get me
  """
  users = UserModel.get_one_user(g.user.get('user_id'))
  ser_users = user_schema.dump(users).data
  return custom_response(ser_users, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@user_api.route('/login', methods=['POST'])
def login():
  """
  User Login Function
  """
  req_data = request.get_json()

  data, error = user_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  if not data.get('username') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  user = UserModel.get_user_by_username(data.get('username'))
  if not user:
    return custom_response({'error': 'invalid credential'}, 400)
  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credential'}, 400)
  ser_data = user_schema.dump(user).data
  token = Auth.generate_token(ser_data.get('user_id'))
  return custom_response({'jwt_token': token}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@user_api.route('/test', methods=['GET'])
@Auth.auth_required
def test():
  users = UserModel.get_one_user(g.user.get('user_id'))
  ser_users = user_schema.dump(users).data
  return custom_response(ser_users, 200)