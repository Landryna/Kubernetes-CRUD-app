from flask import Flask

from common.app_configuration import AppConfiguration


app = Flask(__name__)
api = AppConfiguration.get_instance().get_api_configuration(app)
AppConfiguration.get_instance().configure_k8s_connectivity()

# Required by Flask for splitting routes between many python modules
from controllers.crud_controller import *
