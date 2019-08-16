#/src/views/tarifView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.TarifModel import TarifModel, TarifSchema

sppd_tarif_api = Blueprint('sppd_tarif_api', __name__)
tarif_schema = TarifSchema()

#-------------------------------------------------------------------------
@sppd_tarif_api.route('/create_tarif', methods=['POST'])
def create():
  """
  Create tarif
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = tarif_schema.load(req_data)
  cek = TarifModel.get_one_tarif(req_data['ID_KOTA_AWAL'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = TarifModel(data)
  post.save()

  data = tarif_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_tarif_api.route('/master_tarif', methods=['GET'])
def get_all():
  """
  Get All tarif
  """
  posts = TarifModel.master_tarif()
  data = tarif_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_tarif_api.route('/view_tarif',   methods=['POST'])
def get_one():
  """
  Get A tarif
  """
  req_data = request.get_json()
  post = TarifModel.get_one_tarif(req_data['ID_MASTER_TARIF'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = tarif_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_tarif_api.route('/update_tarif', methods=['POST'])
def update():
  """
  Update Data tarif
  """
  req_data = request.get_json()
  post = TarifModel.get_one_tarif(req_data['ID_MASTER_TARIF'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = tarif_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = tarif_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = tarif_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_tarif_api.route('/delete_tarif', methods=['POST'])
def delete():
  """
  Delete A tarif
  """
  req_data = request.get_json()
  post = TarifModel.get_one_tarif(req_data['ID_MASTER_TARIF'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = tarif_schema.dump(post).data
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
