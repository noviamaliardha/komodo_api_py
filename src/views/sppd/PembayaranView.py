#/src/views/pembayaranView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.PembayaranModel import PembayaranModel, PembayaranSchema

sppd_pembayaran_api = Blueprint('sppd_pembayaran_api', __name__)
pembayaran_schema = PembayaranSchema()
 
#-------------------------------------------------------------------------
@sppd_pembayaran_api.route('/create_pembayaran', methods=['POST'])
def create():
  """
  Create pembayaran
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = pembayaran_schema.load(req_data)
  cek = PembayaranModel.get_one_pembayaran(req_data['ID_PD'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = PembayaranModel(data)
  post.save()

  data = pembayaran_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_pembayaran_api.route('/master_pembayaran', methods=['GET'])
def get_all():
  """
  Get All pembayaran
  """
  posts = PembayaranModel.master_pembayaran()
  data = pembayaran_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_pembayaran_api.route('/view_pembayaran',   methods=['POST'])
def get_one():
  """
  Get pembayaran
  """
  req_data = request.get_json()
  post = PembayaranModel.get_one_pembayaran(req_data['ID_KEUANGAN'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = pembayaran_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_pembayaran_api.route('/update_pembayaran', methods=['POST'])
def update():
  """
  Update Data pembayaran
  """
  req_data = request.get_json()
  post = PembayaranModel.get_one_pembayaran(req_data['ID_KEUANGAN'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = pembayaran_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = pembayaran_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = pembayaran_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_pembayaran_api.route('/delete_pembayaran', methods=['POST'])
def delete():
  """
  Delete pembayaran
  """
  req_data = request.get_json()
  post = PembayaranModel.get_one_pembayaran(req_data['ID_KEUANGAN'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = pembayaran_schema.dump(post).data
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
