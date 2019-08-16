# src/models/CompanyModel.py
from . import db
import datetime
from marshmallow import fields, Schema

class CompanyModel(db.Model):
  """
  Company Model
  """

  __tablename__ = 'company'

  company_id   = db.Column(db.String(3), primary_key=True, nullable=False)
  name         = db.Column(db.String(128),nullable =True)
  phone        = db.Column(db.String(30))
  address      = db.Column(db.String)
  website      = db.Column(db.String)
  email        = db.Column(db.String)
  created_by   = db.Column(db.String)
  created_time = db.Column(db.DateTime)

  def __init__(self, data):
    self.company_id   = data.get('company_id')
    self.name         = data.get('name')
    self.phone        = data.get('phone')
    self.address      = data.get('address')
    self.website      = data.get('website')
    self.email        = data.get('email')
    self.created_by   = data.get('created_by')
    self.created_time = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.created_time = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def master_company():
    return CompanyModel.query.all()
  
  @staticmethod
  def get_one_company(company_id):
    return CompanyModel.query.get(company_id)

  def __repr__(self):
    return '<company_id {}>'.format(self.company_id)

class CompanySchema(Schema):
  """
  Blogpost Schema
  """
  company_id   = fields.Str(required=True)
  name         = fields.Str(required=False)
  phone        = fields.Str(required=False)
  address      = fields.Str(required=False)
  website      = fields.Str(required=False)
  email        = fields.Str(required=False)
  created_by   = fields.Str(required=False)
  created_time = fields.DateTime(dump_only=True)