from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid

class PerjalanandinasModel(db.Model):
  """
  perjalanan dinas Model
  """
  __tablename__ = "T_PERJALANAN_DINAS"
  __table_args__ = {'schema' : 'newsppd'}

  ID_PERJALANAN_DINAS = db.Column(db.String(100),primary_key = True)
  TGL_JAM_MULAI = db.Column(db.String(100),nullable = False)
  TGL_JAM_SELESAI = db.Column(db.String(100),nullable = False)
  ID_KOTA_AWAL = db.Column(db.String(100),nullable = False)
  ID_KOTA_AKHIR = db.Column(db.String(100),nullable = False)
  ID_PERSON = db.Column(db.String(100),nullable = False)
  STATUS = db.Column(db.String(100),nullable = False)

  def __init__(self, data):
    ID_PERJALANAN_DINAS = str(uuid.uuid1())
    TGL_JAM_MULAI = data.get('TGL_JAM_MULAI')
    TGL_JAM_SELESAI = data.get('TGL_JAM_SELESAI')
    ID_KOTA_AWAL = data.get('ID_KOTA_AWAL')
    ID_KOTA_AKHIR = data.get('ID_KOTA_AKHIR')
    ID_PERSON = data.get('ID_PERSON')
    STATUS = data.get('STATUS')

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
  def master_perjalanandinas():
    return PerjalanandinasModel.query.all()
  
  @staticmethod
  def get_one_perjalanandinas(ID_PERJALANAN_DINAS):
    return PerjalanandinasModel.query.get(ID_PERJALANAN_DINAS)

  def __repr__(self):
    return '<ID_PERJALANAN_DINAS {}>'.format(self.ID_PERJALANAN_DINAS)

class PerjalanandinasSchema(Schema):
    ID_PERJALANAN_DINAS = fields.Str(dump_only=True)
    TGL_JAM_MULAI = fields.Str(required=True)
    TGL_JAM_SELESAI = fields.Str(required=True)
    ID_KOTA_AWAL = fields.Str(required=True)
    ID_KOTA_AKHIR = fields.Str(required=True)
    ID_PERSON = fields.Str(required=True)
    STATUS = fields.Str(required=True)