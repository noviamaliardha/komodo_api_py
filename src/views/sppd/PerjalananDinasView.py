#/src/views/perjalanandinasView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.PerjalananDinasModel import PerjalanandinasModel, PerjalanandinasSchema

sppd_perjalanandinas_api = Blueprint('sppd_perjalanandinas_api', __name__)
perjalanandinas_schema = PerjalanandinasSchema()
 
#-------------------------------------------------------------------------
@sppd_perjalanandinas_api.route('/create_perjalanan_dinas', methods=['POST'])
def create():
  """
  Create perjalanandinas
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = perjalanandinas_schema.load(req_data)
  cek = PerjalanandinasModel.get_one_perjalanandinas(req_data['ID_PERJALANAN_DINAS'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = PerjalanandinasModel(data)
  post.save()

  data = perjalanandinas_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_perjalanandinas_api.route('/master_perjalanan_dinas', methods=['GET'])
def get_all():
  """
  Get All perjalanandinas
  """
  posts = PerjalanandinasModel.master_perjalanandinas()
  data = perjalanandinas_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_perjalanandinas_api.route('/view_perjalanan_dinas',   methods=['POST'])
def get_one():
  """
  Get perjalanandinas
  """
  req_data = request.get_json()
  post = PerjalanandinasModel.get_one_perjalanandinas(req_data['ID_PERJALANAN_DINAS'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = perjalanandinas_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_perjalanandinas_api.route('/update_perjalanan_dinas', methods=['POST'])
def update():
  """
  Update Data perjalanandinas
  """
  req_data = request.get_json()
  post = PerjalanandinasModel.get_one_perjalanandinas(req_data['ID_PERJALANAN_DINAS'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = perjalanandinas_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = perjalanandinas_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = perjalanandinas_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_perjalanandinas_api.route('/delete_perjalanan_dinas', methods=['POST'])
def delete():
  """
  Delete perjalanandinas
  """
  req_data = request.get_json()
  post = PerjalanandinasModel.get_one_perjalanandinas(req_data['ID_PERJALANAN_DINAS'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = perjalanandinas_schema.dump(post).data
  #if data.get('owner_id') != g.user.get('id'):
  # return custom_response({'error': 'permission denied'}, 400)
  post.delete()
  return custom_response({'status': 'success','message':'data deleted!'}, 200)
#-------------------------------------------------------------------------

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
