# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime, binascii, hashlib
from . import db

class UserModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'users'
  user_id     = db.Column(db.Integer,     primary_key=True)
  username    = db.Column(db.String(100), nullable=True)
  password    = db.Column(db.String(150), nullable=True)
  person_id   = db.Column(db.String(32),  nullable=True)
  role_id     = db.Column(db.Integer)
  reset_status= db.Column(db.Integer)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.user_id    = data.get('user_id')
    self.username   = data.get('username')
    self.password   = self.__generate_hash(data.get('password'))
    self.person_id  = data.get('person_id')
    self.role_id    = data.get('role_id')
    self.reset_status = data.get('reset_status')


  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      if data.get('password'):
        self.password = self.__generate_hash(data.get('password'))
      setattr(self, key, item)
    #self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_users():
    return UserModel.query.all()

  @staticmethod
  def get_one_user(user_id):
    return UserModel.query.get(user_id)
  
  @staticmethod
  def get_user_by_username(value):
    return UserModel.query.filter_by(username=value).first()

  def __generate_hash(self, password):
    return hashlib.sha1(password.encode()).hexdigest()

  def check_hash(self, password):
    if self.password == hashlib.sha1(password.encode()).hexdigest():
      return True
  
  def __repr(self):
    return '<user_id {}>'.format(self.user_id)

class UserSchema(Schema):
  user_id    = fields.Int(dump_only=True)
  username   = fields.Str(required=False)
  password   = fields.Str(required=False)
  person_id  = fields.Str(required=False)
  role_id    = fields.Str(required=False)
  reset_status = fields.Str(required=False)