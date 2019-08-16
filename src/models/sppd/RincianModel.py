from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid

class RincianModel(db.Model):
  """
  rincian Model
  """

  __tablename__ = "M_RINCIAN"
  __table_args__ = {'schema' : 'newsppd'}


  ID_JENIS_RINCIAN = db.Column(db.String(100), primary_key=True)
  NAMA_JENIS_RINCIAN = db.Column(db.String(100),nullable = False)
  STATUS = db.Column(db.Boolean(0),nullable = False)


  def __init__(self, data):
    self.ID_JENIS_RINCIAN = str(uuid.uuid1())
    self.NAMA_JENIS_RINCIAN = data.get('NAMA_JENIS_RINCIAN')
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
  def master_rincian():
    return RincianModel.query.all()
  
  @staticmethod
  def get_one_rincian(ID_JENIS_RINCIAN):
    return RincianModel.query.get(ID_JENIS_RINCIAN)

  def __repr__(self):
    return '<ID_JENIS_RINCIAN {}>'.format(self.ID_JENIS_RINCIAN)

class RincianSchema(Schema):
    ID_JENIS_RINCIAN = fields.Str(dump_only=True)
    NAMA_JENIS_RINCIAN = fields.Str(required=True)
    STATUS = fields.Bool(required=True)