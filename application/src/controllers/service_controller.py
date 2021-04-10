from flask import request
from flask_restplus import Resource

from controllers.crud_controller import service_controller
from controllers.utils.http_status_code import HttpStatusCode
from dto.kube_api_response_dto import KubeApiResponseDto
from dto.service_dto import ServiceDto
from dto.service_input_dto import ServiceInputDto
from dto.service_update_dto import ServiceUpdateDto
from main import api
from services.crud_service import CRUDService


@service_controller.route("/<string:name>/<string:namespace>/")
class ServiceController(Resource):
    @api.marshal_with(ServiceDto.model, mask=None, code=HttpStatusCode.OK.value)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.'
    })
    def get(self, name, namespace):
        """
        Get Kubernetes Service resource

        :param name: Service name
        :param namespace: Namespace name
        :return: Service manifest DTO
        """
        service = CRUDService.get_instance().get_service(name, namespace)
        return ServiceDto(service)

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.expect(ServiceInputDto.model)
    @api.doc(responses={
        HttpStatusCode.Conflict.value: 'Resource already exist.',
        HttpStatusCode.UnprocessableEntity.value: 'Invalid request body. Check if provided values are correct.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.Accepted.value: 'Resource created.',
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.BadRequest.value: 'Invalid request body. Check if provided values are correct.'
    })
    def post(self, name, namespace):
        """
        Create Kubernetes Service resource

        :param name: Service name
        :param namespace: Namespace name
        :return: Kubernetes Api response DTO
        """
        service_manifest = request.get_json()
        CRUDService.get_instance().create_service(name, namespace, service_manifest)
        return KubeApiResponseDto('Resource created.'), HttpStatusCode.Accepted.value

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.expect(ServiceUpdateDto.model)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.UnprocessableEntity.value: 'Invalid request body. Check if provided values are correct.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.Accepted.value: 'Resource updated.',
        HttpStatusCode.BadRequest.value: 'Invalid request body. Check if provided values are correct.'
    })
    def put(self, name, namespace):
        """
        Update Kubernetes Service resource

        :param name: Service name
        :param namespace: Namespace name
        :return: Kubernetes Api response DTO
        """
        service_manifest = request.get_json()
        CRUDService.get_instance().update_service(name, namespace, service_manifest)
        return KubeApiResponseDto('Resource updated.'), HttpStatusCode.Accepted.value

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.Accepted.value: 'Resource deleted.'
    })
    def delete(self, name, namespace):
        """
        Delete Kubernetes Service resource

        :param name: Service name
        :param namespace: Namespace name
        :return: Kubernetes Api response DTO
        """
        CRUDService.get_instance().delete_service(name, namespace)
        return KubeApiResponseDto('Resource deleted.'), HttpStatusCode.Accepted.value
