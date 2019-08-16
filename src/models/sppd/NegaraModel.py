from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid
 
class NegaraModel(db.Model):
  """
  Negara Model
  """

  __tablename__ = "M_NEGARA"
  __table_args__ = {'schema' : 'newsppd'}


  ID_NEGARA = db.Column(db.String(100), primary_key=True)
  NAMA_NEGARA = db.Column(db.String(100),nullable = False)
  STATUS = db.Column(db.Boolean(0),nullable = False)


  def __init__(self, data):
    self.ID_NEGARA = str(uuid.uuid1())
    self.NAMA_NEGARA = data.get('NAMA_NEGARA')
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
  def master_negara():
    return NegaraModel.query.all()
  
  @staticmethod
  def get_one_negara(ID_NEGARA):
    return NegaraModel.query.get(ID_NEGARA)

  def __repr__(self):
    return '<ID_NEGARA {}>'.format(self.ID_NEGARA)

class NegaraSchema(Schema):
    ID_NEGARA = fields.Str(dump_only=True)
    NAMA_NEGARA = fields.Str(required=True)
    STATUS = fields.Bool(required=True)