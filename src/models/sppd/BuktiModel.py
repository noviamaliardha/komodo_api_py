# src/models/CompanyModel.py
from .. import db
from marshmallow import fields, Schema
import datetime, uuid

class BuktiModel(db.Model):

  __tablename__ = 'T_BUKTI'
  __table_args__ = {'schema': 'newsppd'}

  ID_EVIDENCE       = db.Column(db.Integer, primary_key=True)
  ID_PD             = db.Column(db.String(100))
  NAMA_EVIDENCE     = db.Column(db.String(100))
  ALAMAT_FILE       = db.Column(db.String(100))
  JENIS_EVIDENCE    = db.Column(db.String(100))



  def __init__(self, data):
    self.ID_EVIDENCE      = str(uuid.uuid1()) #generate UUID
    self.ID_PD            = data.get('ID_PD')
    self.NAMA_EVIDENCE    = data.get('NAMA_EVIDENCE')
    self.ALAMAT_FILE      = data.get('ALAMAT_FILE')
    self.JENIS_EVIDENCE   = data.get('JENIS_EVIDENCE')
    
  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    #self.created_date = datetime.datetime.date()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def master_bukti():
    return BuktiModel.query.all()
  
  @staticmethod
  def get_one_bukti(ID_EVIDENCE):
    return BuktiModel.query.get(ID_EVIDENCE)


class BuktiSchema(Schema):
    ID_EVIDENCE       = fields.Str(dump_only=True)
    ID_PD             = fields.Str(required=False)
    NAMA_EVIDENCE     = fields.Str(required=False)
    ALAMAT_FILE       = fields.Str(required=False)
    JENIS_EVIDENCE    = fields.Str(required=False)
