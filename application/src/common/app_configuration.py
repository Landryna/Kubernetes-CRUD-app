from flask_restplus import Api as App_wrapper
from kubernetes import config
import os


class AppConfiguration:
    _instance = None

    @staticmethod
    def get_instance():
        if AppConfiguration._instance is None:
            AppConfiguration()
        return AppConfiguration._instance

    def __init__(self):
        if AppConfiguration._instance is not None:
            raise Exception('This class is a singleton!')
        else:
            AppConfiguration._instance = self

    def get_api_configuration(self, app):
        """
        Get FlaskRestPlus api configuration

        :param app: Flask app
        :return: FlaskRestPlus api configuration
        """
        # disable default 404 error msg provided by Flask
        app.config['ERROR_404_HELP'] = False

        return App_wrapper(app, title='CRUD operations on Kubernetes Resources',
                           description='App performs CRUD operations on Kubernetes cluster')

    def get_api_namespace(self, api, name, path):
        """
        Create api namespace in order to split default api routes

        :param api: FlaskRestPlus api object
        :param name: Name for api namespace
        :param path: Path for api namespace
        :return: Api namespace
        """
        return api.namespace(name, path=path)

    def configure_k8s_connectivity(self):
        """
        Configure Kubernetes connectivity if app is deployed on K8s environment.
        """
        try:
            if os.environ.get('K8S_ENVIRONMENT') == 'True':
                config.load_incluster_config()
        except AttributeError:
            pass
