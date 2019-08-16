#/src/views/TestView.py
from flask                   import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.TestModel      import TestModel
import time
start_time = time.time()

test_api     = Blueprint('test_api', __name__)

@test_api.route('/', methods=['GET'])
def test():
  user = TestModel.master("""SELECT 
  *
  FROM 
    file_save
  WHERE person_id = '1' ORDER BY file_id DESC LIMIT 1""")
  cursor = user.cursor
  items = [[]]
  i = 0
  d = ''
  for row in user: 
    items.append(row)
    for key in cursor.description:
      items[0].append(row[i])
      i = i+1

    a = str(items[0]).replace('[','')
    print (a)
    b = a.replace(']','')
    c = b.replace("'",'')
    d = c.split(',')
    print("--- %s seconds ---" % (time.time() - start_time))
  return ''.join(d)

@test_api.route('/join', methods=['GET'])
def join():
  user = TestModel.join()
  return 'a'
#-------------------------------------------------------------------------
def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
#-------------------------------------------------------------------------