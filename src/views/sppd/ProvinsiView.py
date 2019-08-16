#/src/views/provinsiView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.ProvinsiModel import ProvinsiModel, ProvinsiSchema

sppd_provinsi_api = Blueprint('sppd_provinsi_api', __name__)
provinsi_schema = ProvinsiSchema()

#-------------------------------------------------------------------------
@sppd_provinsi_api.route('/create_provinsi', methods=['POST'])
def create():
  """
  Create provinsi
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = provinsi_schema.load(req_data)
  cek = ProvinsiModel.get_one_provinsi(req_data['NAMA_PROVINSI'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = ProvinsiModel(data)
  post.save()

  data = provinsi_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_provinsi_api.route('/master_provinsi', methods=['GET'])
def get_all():
  """
  Get All provinsi
  """
  posts = ProvinsiModel.master_provinsi()
  data = provinsi_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_provinsi_api.route('/view_provinsi',   methods=['POST'])
def get_one():
  """
  Get A provinsi
  """
  req_data = request.get_json()
  post = ProvinsiModel.get_one_provinsi(req_data['ID_PROVINSI'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = provinsi_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_provinsi_api.route('/update_provinsi', methods=['POST'])
def update():
  """
  Update Data provinsi
  """
  req_data = request.get_json()
  post = ProvinsiModel.get_one_provinsi(req_data['ID_PROVINSI'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = provinsi_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = provinsi_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = provinsi_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_provinsi_api.route('/delete_provinsi', methods=['POST'])
def delete():
  """
  Delete A provinsi
  """
  req_data = request.get_json()
  post = ProvinsiModel.get_one_provinsi(req_data['ID_PROVINSI'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = provinsi_schema.dump(post).data
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
