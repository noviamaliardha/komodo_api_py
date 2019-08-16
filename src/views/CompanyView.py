#/src/views/CompanyView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.CompanyModel import CompanyModel, CompanySchema

company_api = Blueprint('company_api', __name__)
company_schema = CompanySchema()

#-------------------------------------------------------------------------
@company_api.route('/create_company', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Company
  """
  req_data = request.get_json()
  #req_data['name'] = g.user.get('name')
  data, error = company_schema.load(req_data)
  cek = CompanyModel.get_one_company(req_data['company_id'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = CompanyModel(data)
  post.save()

  data = company_schema.dump(post).data
  return custom_response({'status': 'succes','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@company_api.route('/master_company', methods=['GET'])
def get_all():
  """
  Get All Company
  """
  posts = CompanyModel.master_company()
  data = company_schema.dump(posts, many=True).data
  return custom_response({'status': 'succes','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@company_api.route('/view_company',   methods=['POST'])
def get_one():
  """
  Get A Company
  """
  req_data = request.get_json()
  post = CompanyModel.get_one_company(req_data['company_id'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = company_schema.dump(post).data
  return custom_response({'status': 'succes','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@company_api.route('/update_company', methods=['POST'])
@Auth.auth_required
def update():
  """
  Update Data Company
  """
  req_data = request.get_json()
  post = CompanyModel.get_one_company(req_data['company_id'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = company_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = company_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = company_schema.dump(post).data
  return custom_response({'status': 'succes','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@company_api.route('/delete_company', methods=['POST'])
@Auth.auth_required
def delete():
  """
  Delete A Company
  """
  req_data = request.get_json()
  post = CompanyModel.get_one_company(req_data['company_id'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = company_schema.dump(post).data
  #if data.get('owner_id') != g.user.get('id'):
  # return custom_response({'error': 'permission denied'}, 400)
  post.delete()
  return custom_response({'status': 'succes','message':'data found',"data":data}, 200)
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
