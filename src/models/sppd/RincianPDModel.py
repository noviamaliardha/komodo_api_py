from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid

class RincianPDModel(db.Model):
  """
  rincianpd Model
  """

  __tablename__ = "T_RINCIAN_PD"
  __table_args__ = {'schema' : 'newsppd'}


  ID_RINCIAN_PD = db.Column(db.String(100), primary_key=True)
  ID_PD = db.Column(db.String(100),nullable = False)
  ID_M_TARIF = db.Column(db.String(100),nullable = False)
  ID_EVIDENCE = db.Column(db.String(100),nullable = False)
  NAMA_RINCIAN = db.Column(db.String(100),nullable = False)
  NOMINAL = db.Column(db.Float,nullable = False)


  def __init__(self, data):
    self.ID_RINCIAN_PD = str(uuid.uuid1())
    self.ID_PD = data.get('ID_KOTA_AWAL')
    self.ID_M_TARIF = data.get('ID_KOTA_AKHIR')
    self.ID_EVIDENCE = data.get('ID_LEVEL')
    self.NAMA_RINCIAN = data.get('NOMINAL')
    self.NOMINAL = data.get('NOMINAL')

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
  def master_rincianpd():
    return RincianPDModel.query.all()
  
  @staticmethod
  def get_one_rincianpd(ID_RINCIAN_PD):
    return RincianPDModel.query.get(ID_RINCIAN_PD)

  def __repr__(self):
    return '<ID_RINCIAN_PD {}>'.format(self.ID_RINCIAN_PD)

class RincianPDSchema(Schema):
    ID_RINCIAN_PD = fields.Str(dump_only=True)
    ID_PD = fields.Str(required=True)
    ID_M_TARIF = fields.Str(required=True)
    ID_EVIDENCE = fields.Str(required=True)
    NAMA_RINCIAN = fields.Str(required=True)
    NOMINAL = fields.Str(required=True)