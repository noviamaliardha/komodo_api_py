# /run.py
import os
from src.app import create_app
app = create_app(env_name)
if __name__ == '__main__':
  env_name  =   os.environ['FLASK_ENV']
  
  # run app
  app.run()
