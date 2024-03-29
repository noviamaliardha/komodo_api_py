#/src/views/rincianView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.RincianModel import RincianModel, RincianSchema

sppd_rincian_api = Blueprint('sppd_rincian_api', __name__)
rincian_schema = RincianSchema()
 
#-------------------------------------------------------------------------
@sppd_rincian_api.route('/create_rincian', methods=['POST'])
def create():
  """
  Create rincian
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = rincian_schema.load(req_data)
  cek = RincianModel.get_one_rincian(req_data['NAMA_JENIS_RINCIAN'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = RincianModel(data)
  post.save()

  data = rincian_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincian_api.route('/master_rincian', methods=['GET'])
def get_all():
  """
  Get All rincian
  """
  posts = RincianModel.master_rincian()
  data = rincian_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincian_api.route('/view_rincian',   methods=['POST'])
def get_one():
  """
  Get A rincian
  """
  req_data = request.get_json()
  post = RincianModel.get_one_rincian(req_data['ID_JENIS_RINCIAN'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = rincian_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincian_api.route('/update_rincian', methods=['POST'])
def update():
  """
  Update Data rincian
  """
  req_data = request.get_json()
  post = RincianModel.get_one_rincian(req_data['ID_JENIS_RINCIAN'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = rincian_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = rincian_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = rincian_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincian_api.route('/delete_rincian', methods=['POST'])
def delete():
  """
  Delete A rincian
  """
  req_data = request.get_json()
  post = RincianModel.get_one_rincian(req_data['ID_JENIS_RINCIAN'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = rincian_schema.dump(post).data
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
