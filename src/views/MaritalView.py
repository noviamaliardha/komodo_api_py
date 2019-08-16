#/src/views/MaritalView.py
from flask                   import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.MaritalModel   import MaritalModel, MaritalSchema

marital_api     = Blueprint('marital_api', __name__)
marital_schema  = MaritalSchema()

#-------------------------------------------------------------------------
@marital_api.route('/create_marital', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Marital
  """
  req_data = request.get_json()
  data, error = marital_schema.load(req_data)
  cek = MaritalModel.get_one_marital(req_data['marital_id'])
  if error or cek :
    return custom_response({'status': 'failed','message':'failed insert data'}, 400)
  post = MaritalModel(data)
  post.save()

  data = marital_schema.dump(post).data
  return custom_response({'status': 'succes','message':'success insert data',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@marital_api.route('/master_marital', methods=['GET'])
def get_all():
  """
  Get All Marital
  """
  posts = MaritalModel.master_marital()
  data = marital_schema.dump(posts, many=True).data
  return custom_response({'status': 'succes','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@marital_api.route('/view_marital',   methods=['POST'])
def get_one():
  """
  Get A Marital
  """
  req_data = request.get_json()
  post = MaritalModel.get_one_marital(req_data['marital_id'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = marital_schema.dump(post).data
  return custom_response({'status': 'succes','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@marital_api.route('/update_marital', methods=['POST'])
@Auth.auth_required
def update():
  """
  Update Data Marital
  """
  req_data = request.get_json()
  post = MaritalModel.get_one_marital(req_data['marital_id'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = marital_schema.dump(post).data
  #  if data.get('owner_id') != g.user.get('id'):
  #    return custom_response({'error': 'permission denied'}, 400)
 
  data, error = marital_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)
  
  data = marital_schema.dump(post).data
  return custom_response({'status': 'succes','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
@marital_api.route('/delete_marital', methods=['POST'])
@Auth.auth_required
def delete():
  """
  Delete A Marital
  """
  req_data = request.get_json()
  post = MaritalModel.get_one_marital(req_data['marital_id'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = marital_schema.dump(post).data
  #if data.get('owner_id') != g.user.get('id'):
  # return custom_response({'error': 'permission denied'}, 400)
  post.delete()
  return custom_response({'status': 'succes','message':'data found','data':''}, 200)
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
