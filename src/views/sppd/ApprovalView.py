#/src/views/ApprovalView.py
from flask import request, g, Blueprint, json, Response
from ...shared.Authentication import Auth
from ...models.sppd.ApprovalModel import ApprovalModel, ApprovalSchema

sppd_approval_api = Blueprint('sppd_approval_api', __name__)
approval_schema = ApprovalSchema()

#-------------------------------------------------------------------------
@sppd_approval_api.route('/create_approval', methods=['POST'])
def create():
  """
  Create approval
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = approval_schema.load(req_data)
  cek = ApprovalModel.get_one_approval(req_data['ID_PERSON'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = ApprovalModel(data)
  post.save()

  data = approval_schema.dump(post).data
  return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_approval_api.route('/master_approval', methods=['GET'])
def get_all():
  """
  Get All approval
  """
  posts = ApprovalModel.master_approval()
  data = approval_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_approval_api.route('/view_approval',   methods=['POST'])
def get_one():
  """
  Get approval
  """
  req_data = request.get_json()
  post = ApprovalModel.get_one_approval(req_data['ID_APPROVAL'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = approval_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_approval_api.route('/update_approval', methods=['POST'])
def update():
  """
  Update Data approval
  """
  req_data = request.get_json()
  post = ApprovalModel.get_one_approval(req_data['ID_APPROVAL'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = approval_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = approval_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = approval_schema.dump(post).data
  return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@sppd_approval_api.route('/delete_approval', methods=['POST'])
def delete():
  """
  Delete approval
  """
  req_data = request.get_json()
  post = ApprovalModel.get_one_approval(req_data['ID_APPROVAL'])
  if not post:
    return custom_response({'error': 'data not found'}, 404)
  data = approval_schema.dump(post).data
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
