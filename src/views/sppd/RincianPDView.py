#/src/views/rincianpdView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.RincianPDModel import RincianPDModel, RincianPDSchema

sppd_rincianpd_api = Blueprint('sppd_rincianpd_api', __name__)
rincianpd_schema = RincianPDSchema()
 
#-------------------------------------------------------------------------
@sppd_rincianpd_api.route('/create_rincianpd', methods=['POST'])
def create():
  """
  Create rincianpd
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = rincianpd_schema.load(req_data)
  cek = RincianPDModel.get_one_rincianpd(req_data['NAMA_RINCIAN'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = RincianPDModel(data)
  post.save()

  data = rincianpd_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincianpd_api.route('/master_rincianpd', methods=['GET'])
def get_all():
  """
  Get All rincianpd
  """
  posts = RincianPDModel.master_rincianpd()
  data = rincianpd_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincianpd_api.route('/view_rincianpd',   methods=['POST'])
def get_one():
  """
  Get A rincianpd
  """
  req_data = request.get_json()
  post = RincianPDModel.get_one_rincianpd(req_data['ID_RINCIAN_PD'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = rincianpd_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincianpd_api.route('/update_rincianpd', methods=['POST'])
def update():
  """
  Update Data rincianpd
  """
  req_data = request.get_json()
  post = RincianPDModel.get_one_rincianpd(req_data['ID_RINCIAN_PD'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = rincianpd_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = rincianpd_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = rincianpd_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_rincianpd_api.route('/delete_rincianpd', methods=['POST'])
def delete():
  """
  Delete A rincianpd
  """
  req_data = request.get_json()
  post = RincianPDModel.get_one_rincianpd(req_data['ID_RINCIAN_PD'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = rincianpd_schema.dump(post).data
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
