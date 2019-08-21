from .. import db
from .. import db
from marshmallow import fields, Schema
import uuid
 
class ApprovalModel(db.Model):
  """
  Approval Model
  """
  __tablename__ = "T_APPROVAL"
  __table_args__ = {'schema' : 'newsppd'}

  ID_APPROVAL = db.Column(db.String(100),primary_key = True)
  ID_PD = db.Column(db.String(100),nullable = False)
  ID_ORDER = db.Column(db.Integer, nullable=True)
  ID_PERSON = db.Column(db.String(100),nullable = False)
  ID_TYPE = db.Column(db.Integer, nullable=True)

  def __init__(self, data):
    self.ID_APPROVAL = str(uuid.uuid1())
    self.ID_PD = data.get('ID_PD')
    self.ID_ORDER = data.get('ID_ORDER')
    self.ID_PERSON = data.get('ID_PERSON')
    self.ID_TYPE = data.get('ID_TYPE')

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
  def master_approval():
    return ApprovalModel.query.all()
  
  @staticmethod
  def get_one_approval(ID_APPROVAL):
    return ApprovalModel.query.get(ID_APPROVAL)

  def __repr__(self):
    return '<ID_APPROVAL {}>'.format(self.ID_APPROVAL)

class ApprovalSchema(Schema):
    ID_APPROVAL = fields.Str(dump_only=True)
    ID_PD = fields.Str(required=True)
    ID_ORDER = fields.Int(required=True)
    ID_PERSON = fields.Str(required=True)
    ID_TYPE = fields.Int(required=True)