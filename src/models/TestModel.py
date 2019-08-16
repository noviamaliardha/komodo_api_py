# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime, binascii, hashlib
from sqlalchemy import MetaData, select
from . import db

class TestModel():
  """
  Test Model
  """

  # class constructor
  def __init__(self):
    self.a = 'a'

  @staticmethod
  def test():
    return TestModel.query.all()

  @staticmethod
  def join():
    meta = MetaData(db.engine, reflect=True)
    user_t = meta.tables['users'] #ambil metadata dari tabel users
    role_t = meta.tables['user_role'] #ambil metadata dari tabel user_role

    join_obj = user_t.join(role_t,role_t.c.role_id == user_t.c.role_id)
    # using select_from
    sel_st = select([user_t.c.role_id, role_t.c.role_id, user_t.c.username]).select_from(join_obj)

    res = db.session.execute(sel_st)
    arr = []
    for _row in res:
      print(_row)
      arr=_row
      pass
    return arr

  @staticmethod
  def master(sql):
    rs = db.session.execute(sql)
    db.session.remove
    return rs

def __repr(self):
    return '<user_id {}>'.format(self.user_id)

#region comment
"""
cursor = rs.cursor
items = []
for row in rs: 
  i = 0
  for key in cursor.description:
    items.append({key[0]: value for value in row[i]})
    i = i+1
    print (i)
"""
#endregion
