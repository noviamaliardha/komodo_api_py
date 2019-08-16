#/src/views/buktiView.py
from flask                      import request, g, Blueprint, json, Response, request, flash
from ...shared.Authentication   import Auth
from ...models.sppd.BuktiModel  import BuktiModel, BuktiSchema
import os


sppd_bukti_api          = Blueprint('sppd_bukti_api', __name__)
bukti_schema       = BuktiSchema()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'exe', 'json'])
UPLOAD_FOLDER      = 'C:/xampp/htdocs/komodo_api_py/src/uploads'
#-------------------------------------------------------------------------
@sppd_bukti_api.route('/create_bukti', methods=['POST'])
def create():
  try:
    req_data = {} #pembuatan array utk dipakai schema pada bukti_schema
    #req_data['ID_EVIDENCE']     = request.form['ID_EVIDENCE']
    req_data['ID_PD']           = request.form['ID_PD']
    req_data['ALAMAT_FILE']     = UPLOAD_FOLDER +'/'+ request.files['file'].filename
    req_data['NAMA_EVIDENCE']   = request.form['NAMA_EVIDENCE']
    req_data['JENIS_EVIDENCE']  = request.form['JENIS_EVIDENCE']

    data, error = bukti_schema.load(req_data)

    #cek = BuktiModel.get_one_bukti(req_data['ID_EVIDENCE'])
    if error :
      return custom_response({'status': 'failed','message':'failed insert data'}, 400)
    if 'file' in request.files:
        bukti = request.files['file']
        if bukti.filename != '':
          if allowed_file(bukti.filename):
            bukti.save(os.path.join(UPLOAD_FOLDER, bukti.filename))
            post = BuktiModel(data)
            post.save()

    data = bukti_schema.dump(post).data
    return custom_response({'status': 'success','message':'success insert data',"data":data}, 200)
  except :
    return custom_response({'status': 'success','message':'error insert data',"data":"ERROR"}, 400)
#-------------------------------------------------------------------------
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#-------------------------------------------------------------------------
@sppd_bukti_api.route('/master_bukti', methods=['GET'])
def get_all():
  """
  Get All bukti
  """
  posts = BuktiModel.master_bukti()
  data = bukti_schema.dump(posts, many=True).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
@sppd_bukti_api.route('/view_bukti',   methods=['POST'])
def get_one():
  """
  Get A bukti
  """
  req_data = request.get_json()
  post = BuktiModel.get_one_bukti(req_data['ID_EVIDENCE'])
  if not post:
    return custom_response({'status': 'failed','message':'data not found',"data":""}, 404)
  data = bukti_schema.dump(post).data
  return custom_response({'status': 'success','message':'data found',"data":data}, 200)
#-------------------------------------------------------------------------
@sppd_bukti_api.route('/update_bukti', methods=['POST'])
def update():
  try:
    req_data = {}
    req_data['ID_EVIDENCE']     = request.form['ID_EVIDENCE']
    req_data['ID_PD']           = request.form['ID_PD']
    req_data['ALAMAT_FILE']     = UPLOAD_FOLDER +'/'+ request.files['file'].filename
    req_data['NAMA_EVIDENCE']   = request.form['NAMA_EVIDENCE']
    req_data['JENIS_EVIDENCE']  = request.form['JENIS_EVIDENCE']
    
    post = BuktiModel.get_one_bukti(req_data['ID_EVIDENCE'])
    if not post:
      return custom_response({'error': 'post not found'}, 404)
    data = bukti_schema.dump(post).data
  
    data, error = bukti_schema.load(req_data, partial=True)
    if error:
      return custom_response(error, 400)
    if 'file' in request.files:
        bukti = request.files['file']
        if bukti.filename != '':
          if allowed_file(bukti.filename):
            bukti.save(os.path.join(UPLOAD_FOLDER, bukti.filename))
    post.update(data)
    data = bukti_schema.dump(post).data
    return custom_response({'status': 'success','message':'data updated!',"data":data}, 200)

  except :
    return custom_response({'status': 'success','message':'data found',"data":"ERROR"}, 200)
#-------------------------------------------------------------------------
@sppd_bukti_api.route('/delete_bukti', methods=['POST'])
def delete():
  """
  Delete A bukti
  """
  req_data = request.get_json()
  post = BuktiModel.get_one_bukti(req_data['ID_EVIDENCE'])
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = bukti_schema.dump(post).data
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
