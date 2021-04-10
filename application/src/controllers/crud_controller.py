from common.app_configuration import AppConfiguration
from controllers.utils.http_status_code import HttpStatusCode
from dto.list_of_resources_dto import ListOfResourcesDto

from exceptions.app_exceptions import ServiceUnavailable
from exceptions.kube_api_exceptions import ResourceNotFoundException, ResourceAlreadyExistException, \
    InvalidResourceManifestException
from main import api
from flask_restplus import Resource

pod_controller = AppConfiguration. \
    get_instance(). \
    get_api_namespace(api, 'Pod', '/pod')

service_controller = AppConfiguration. \
    get_instance(). \
    get_api_namespace(api, 'Service', '/service')

namespace_controller = AppConfiguration. \
    get_instance(). \
    get_api_namespace(api, 'Namespace', '/namespace')


@api.errorhandler(ResourceNotFoundException)
def handle_kube_api_not_found_error(error):
    return {'message': str(error)}, HttpStatusCode.NotFound.value


@api.errorhandler(ServiceUnavailable)
def handle_internal_service_error(error):
    return {'message': str(error)}, HttpStatusCode.ServiceUnavailable.value


@api.errorhandler(ResourceAlreadyExistException)
def handle_resource_conflict_error(error):
    return {'message': str(error)}, HttpStatusCode.Conflict.value


@api.errorhandler(InvalidResourceManifestException)
def handle_invalid_resource_manifest(error):
    return {'message': str(error)}, HttpStatusCode.UnprocessableEntity.value


@api.errorhandler(InvalidResourceManifestException)
def handle_invalid_marshaling_error(error):
    return {'message': str(error)}, HttpStatusCode.BadRequest.value


@api.route('/list_resources/<string:namespace>/<string:kind>')
class GetResourceListController(Resource):
    @api.marshal_with(ListOfResourcesDto.model, mask=None, code=HttpStatusCode.OK.value)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.NotFound.value: 'Provided kind is not supported.'
    })
    def get(self, namespace, kind):
        """
        List of Kubernetes resources

        :param namespace: Namespace name
        :param kind: Kind name
        :return: List of Kubernetes resources DTO
        """
        list_of_resources = CRUDService.get_instance().get_list_of_resources(kind, namespace)
        return ListOfResourcesDto(list_of_resources)


# Required by Flask for splitting routes between many python modules
from controllers.namespace_controller import *
from controllers.pod_controller import *
from controllers.service_controller import *
