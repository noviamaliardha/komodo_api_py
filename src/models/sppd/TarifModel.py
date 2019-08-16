from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid
 
class TarifModel(db.Model):
  """
  tarif Model
  """

  __tablename__ = "M_TARIF"
  __table_args__ = {'schema' : 'newsppd'}

  ID_MASTER_TARIF = db.Column(db.String(100), primary_key=True)
  ID_KOTA_AWAL = db.Column(db.String(100),nullable = False)
  ID_KOTA_AKHIR = db.Column(db.String(100),nullable = False)
  ID_LEVEL = db.Column(db.String(100),nullable = False)
  NOMINAL = db.Column(db.Float,nullable = False)


  def __init__(self, data):
    self.ID_MASTER_TARIF = str(uuid.uuid1())
    self.ID_KOTA_AWAL = data.get('ID_KOTA_AWAL')
    self.ID_KOTA_AKHIR = data.get('ID_KOTA_AKHIR')
    self.ID_LEVEL = data.get('ID_LEVEL')
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
  def master_tarif():
    return TarifModel.query.all()
  
  @staticmethod
  def get_one_tarif(ID_MASTER_TARIF):
    return TarifModel.query.get(ID_MASTER_TARIF)

  def __repr__(self):
    return '<ID_MASTER_TARIF {}>'.format(self.ID_MASTER_TARIF)

class TarifSchema(Schema):
    ID_MASTER_TARIF = fields.Str(dump_only=True)
    ID_KOTA_AWAL = fields.Str(required=True)
    ID_KOTA_AKHIR = fields.Str(required=True)
    ID_LEVEL = fields.Str(required=True)
    NOMINAL = fields.Str(required=True)