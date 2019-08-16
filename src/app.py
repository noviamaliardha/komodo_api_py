#src/app.py

from flask   import Flask
from .config import app_config
from .models import db

# import user_api blueprint
from .views.UserView    import user_api    as user_blueprint
from .views.CompanyView import company_api as company_blueprint
from .views.MaritalView import marital_api as marital_blueprint
from .views.TestView    import test_api    as test_blueprint
from .views.sppd.KotaView    import sppd_kota_api    as kota_blueprint
from .views.sppd.NegaraView    import sppd_negara_api    as negara_blueprint
from .views.sppd.ProvinsiView    import sppd_provinsi_api    as provinsi_blueprint
from .views.sppd.BuktiView  import bukti_api    as bukti_blueprint



def create_app(env_name):
  # Create app

  # app initiliazation
  app = Flask(__name__)

  #-------------------------------------------------------------------------
  app.config.from_object(app_config[env_name])
  #-------------------------------------------------------------------------

  # initializing db
  db.init_app(app)
  #-------------------------------------------------------------------------

  # register blueprint / api endpoint url 
  app.register_blueprint(user_blueprint,    url_prefix='/api/v1/users')
  app.register_blueprint(company_blueprint, url_prefix='/api/v1/company')
  app.register_blueprint(marital_blueprint, url_prefix='/api/v1/marital')
  app.register_blueprint(test_blueprint,    url_prefix='/api/v1/test')
  app.register_blueprint(kota_blueprint,    url_prefix='/api/v1/sppd/')
  app.register_blueprint(provinsi_blueprint,    url_prefix='/api/v1/sppd/')
  app.register_blueprint(bukti_blueprint,    url_prefix='/api/v1/sppd/')
  #-------------------------------------------------------------------------

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'WELCOME TO API SERVER PYTHON USING FLASK'
  #-------------------------------------------------------------------------

  return app
