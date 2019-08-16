# src/models/CompanyModel.py
from . import db
from marshmallow import fields, Schema

class MaritalModel(db.Model):
  """
  Company Model
  """

  __tablename__ = 'marital'

  marital_id            = db.Column(db.String(2), primary_key=True, nullable=False)
  marital_description   = db.Column(db.String(200),nullable = False)


  def __init__(self, data):
    self.marital_id         = data.get('marital_id')
    self.marital_description = data.get('marital_description')

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    #self.created_time = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def master_marital():
    return MaritalModel.query.all()
  
  @staticmethod
  def get_one_marital(marital_id):
    return MaritalModel.query.get(marital_id)

  def __repr__(self):
    return '<marital_id {}>'.format(self.marital_id)

class MaritalSchema(Schema):
    marital_id          = fields.Str(required=True)
    marital_description = fields.Str(required=True)