# /run.py
import os
from src.app import create_app
app = create_app(env_name)
env_name  =   os.environ['FLASK_ENV']

if __name__ == '__main__':
  
  # run app
  app.run()
