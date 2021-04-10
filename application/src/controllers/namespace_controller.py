from flask_restplus import Resource

from controllers.crud_controller import namespace_controller
from controllers.utils.http_status_code import HttpStatusCode
from dto.kube_api_response_dto import KubeApiResponseDto
from dto.namespace_dto import NamespaceDto
from main import api
from services.crud_service import CRUDService


@namespace_controller.route("/<string:name>/")
class NamespaceController(Resource):
    @api.marshal_with(NamespaceDto.model, mask=None, code=HttpStatusCode.OK.value)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.'
    })
    def get(self, name):
        """
        Get Kubernetes Namespace resource

        :param name: Namespace name
        :return: Namespace manifest DTO
        """
        namespace = CRUDService.get_instance().get_namespace(name)
        return NamespaceDto(namespace)

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.doc(responses={
        HttpStatusCode.Conflict.value: 'Resource already exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.Accepted.value: 'Resource created.'
    })
    def post(self, name):
        """
        Create Kubernetes Namespace resource

        :param name: Namespace name
        :return: Kubernetes Api response DTO
        """
        CRUDService.get_instance().create_namespace(name)
        return KubeApiResponseDto('Resource created.'), HttpStatusCode.Accepted.value

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.Accepted.value: 'Resource deleted.'
    })
    def delete(self, name):
        """
        Delete Kubernetes Namespace resource

        :param name: Namespace name
        :return: Kubernetes Api response DTO
        """
        CRUDService.get_instance().delete_namespace(name)
        return KubeApiResponseDto('Resource deleted.'), HttpStatusCode.Accepted.value
