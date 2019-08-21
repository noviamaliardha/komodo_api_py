from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid
 
class ProvinsiModel(db.Model):
  """
  Provinsi Model
  """

  __tablename__ = "M_PROVINSI"
  __table_args__ = {'schema' : 'newsppd'}


  ID_PROVINSI = db.Column(db.String(100), primary_key=True)
  ID_NEGARA = db.Column(db.String(100), nullable=False)
  NAMA_PROVINSI = db.Column(db.String(100),nullable = False)
  STATUS = db.Column(db.Boolean(0),nullable = False)


  def __init__(self, data):
    self.ID_PROVINSI = str(uuid.uuid1())
    self.ID_NEGARA = data.get('ID_NEGARA')
    self.NAMA_PROVINSI = data.get('NAMA_PROVINSI')
    self.STATUS = data.get('STATUS')

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
  def master_provinsi():
    return ProvinsiModel.query.all()
  
  @staticmethod
  def get_one_provinsi(ID_PROVINSI):
    return ProvinsiModel.query.get(ID_PROVINSI)

  def __repr__(self):
    return '<ID_PROVINSI {}>'.format(self.ID_PROVINSI)

class ProvinsiSchema(Schema):
    ID_PROVINSI = fields.Str(dump_only=True)
    ID_NEGARA = fields.Str(required=True)
    NAMA_PROVINSI = fields.Str(required=True)
    STATUS = fields.Bool(required=True)