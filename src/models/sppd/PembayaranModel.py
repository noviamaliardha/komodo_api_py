from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid
 
class PembayaranModel(db.Model):
  """
  pembayaran Model
  """
  __tablename__ = "T_PEMBAYARAN"
  __table_args__ = {'schema' : 'newsppd'}

  ID_KEUANGAN = db.Column(db.String(100),primary_key = True)
  ID_PD = db.Column(db.String(100),nullable = False)
  ID_COSTCENTER = db.Column(db.String(100),nullable = False)
  ID_ACCOUNT = db.Column(db.String(100),nullable = False)
  SALDO = db.Column(db.Float,nullable = False)

  def __init__(self, data):
    self.ID_KEUANGAN = str(uuid.uuid1())
    self.ID_PD = data.get('ID_PD')
    self.ID_COSTCENTER = data.get('ID_COSTCENTER')
    self.ID_ACCOUNT = data.get('ID_ACCOUNT')
    self.SALDO = data.get('SALDO')

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
  def master_pembayaran():
    return PembayaranModel.query.all()
  
  @staticmethod
  def get_one_pembayaran(ID_KEUANGAN):
    return PembayaranModel.query.get(ID_KEUANGAN)

  def __repr__(self):
    return '<ID_KEUANGAN {}>'.format(self.ID_KEUANGAN)

class PembayaranSchema(Schema):
    ID_KEUANGAN = fields.Str(dump_only=True)
    ID_PD = fields.Str(required=True)
    ID_COSTCENTER = fields.Str(required=True)
    ID_ACCOUNT = fields.Str(required=True)
    SALDO = fields.Str(required=True)