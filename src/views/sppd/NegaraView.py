#/src/views/negaraView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.NegaraModel import NegaraModel, NegaraSchema

sppd_negara_api = Blueprint('sppd_negara_api', __name__)
negara_schema = NegaraSchema()
 
#-------------------------------------------------------------------------
@sppd_negara_api.route('/create_negara', methods=['POST'])
def create():
  """
  Create negara
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = negara_schema.load(req_data)
  cek = NegaraModel.get_one_negara(req_data['NAMA_NEGARA'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = NegaraModel(data)
  post.save()

  data = negara_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_negara_api.route('/master_negara', methods=['GET'])
def get_all():
  """
  Get All negara
  """
  posts = NegaraModel.master_negara()
  data = negara_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_negara_api.route('/view_negara',   methods=['POST'])
def get_one():
  """
  Get A negara
  """
  req_data = request.get_json()
  post = NegaraModel.get_one_negara(req_data['ID_NEGARA'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = negara_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_negara_api.route('/update_negara', methods=['POST'])
def update():
  """
  Update Data negara
  """
  req_data = request.get_json()
  post = NegaraModel.get_one_negara(req_data['ID_NEGARA'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = negara_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = negara_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = negara_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_negara_api.route('/delete_negara', methods=['POST'])
def delete():
  """
  Delete A negara
  """
  req_data = request.get_json()
  post = NegaraModel.get_one_negara(req_data['ID_NEGARA'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = negara_schema.dump(post).data
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
