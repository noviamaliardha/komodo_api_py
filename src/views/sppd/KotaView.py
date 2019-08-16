#/src/views/KotaView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.KotaModel import KotaModel, KotaSchema

sppd_kota_api = Blueprint('sppd_kota_api', __name__)
kota_schema = KotaSchema()

#-------------------------------------------------------------------------
@sppd_kota_api.route('/create_kota', methods=['POST'])
def create():
  """
  Create kota
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = kota_schema.load(req_data)
  cek = KotaModel.get_one_kota(req_data['NAMA_KOTA'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = KotaModel(data)
  post.save()

  data = kota_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_kota_api.route('/master_kota', methods=['GET'])
def get_all():
  """
  Get All kota
  """
  posts = KotaModel.master_kota()
  data = kota_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_kota_api.route('/view_kota',   methods=['POST'])
def get_one():
  """
  Get A kota
  """
  req_data = request.get_json()
  post = KotaModel.get_one_kota(req_data['ID_KOTA'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = kota_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_kota_api.route('/update_kota', methods=['POST'])
def update():
  """
  Update Data kota
  """
  req_data = request.get_json()
  post = KotaModel.get_one_kota(req_data['ID_KOTA'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = kota_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = kota_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = kota_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_kota_api.route('/delete_kota', methods=['POST'])
def delete():
  """
  Delete A kota
  """
  req_data = request.get_json()
  post = KotaModel.get_one_kota(req_data['ID_KOTA'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = kota_schema.dump(post).data
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
