from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid

class KotaModel(db.Model):
  """
  Company Model
  """

  __tablename__ = "M_KOTA"
  __table_args__ = {'schema' : 'newsppd'}


  ID_KOTA = db.Column(db.Integer, primary_key=True)
  ID_PROVINSI = db.Column(db.String(100),nullable = False)
  NAMA_KOTA = db.Column(db.String(100),nullable = False)
  STATUS = db.Column(db.Boolean(0),nullable = False)


  def __init__(self, data):
    self.ID_KOTA = str(uuid.uuid1())
    self.ID_PROVINSI = data.get('ID_PROVINSI')
    self.NAMA_KOTA = data.get('NAMA_KOTA')
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
  def master_kota():
    return KotaModel.query.all()
  
  @staticmethod
  def get_one_kota(ID_KOTA):
    return KotaModel.query.get(ID_KOTA)

  def __repr__(self):
    return '<ID_KOTA {}>'.format(self.ID_KOTA)

class KotaSchema(Schema):
    ID_KOTA = fields.Str(dump_only=True)
    ID_PROVINSI = fields.Str(required=True)
    NAMA_KOTA = fields.Str(required=True)
    STATUS = fields.Bool(required=True)