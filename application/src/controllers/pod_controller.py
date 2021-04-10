from flask import request
from flask_restplus import Resource
from main import api
from controllers.crud_controller import pod_controller
from controllers.utils.http_status_code import HttpStatusCode
from dto.pod_dto import PodDto
from dto.pod_input_dto import PodInputDto
from dto.pod_update_dto import PodUpdateDto
from dto.kube_api_response_dto import KubeApiResponseDto
from services.crud_service import CRUDService


@pod_controller.route("/<string:name>/<string:namespace>/")
class PodController(Resource):
    @api.marshal_with(PodDto.model, mask=None, code=HttpStatusCode.OK.value)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.'
    })
    def get(self, name, namespace):
        """
        Get Kubernetes Pod resource

        :param name: Pod name
        :param namespace: Namespace name
        :return: Pod manifest DTO
        """
        pod = CRUDService.get_instance().get_pod(name, namespace)
        return PodDto(pod)

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.expect(PodInputDto.model)
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
        Create Kubernetes Pod resource

        :param name: Pod name
        :param namespace: Namespace name
        :return: Kubernetes Api response DTO
        """
        pod_manifest = request.get_json()
        CRUDService. \
            get_instance(). \
            create_pod(name, namespace, pod_manifest)
        return KubeApiResponseDto('Resource created.'), \
               HttpStatusCode.Accepted.value

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.expect(PodUpdateDto.model)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.UnprocessableEntity.value: 'Invalid request body. Check if provided values are correct.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.Accepted.value: 'Resource updated.',
        HttpStatusCode.BadRequest.value: 'Invalid request body. Check if provided values are correct.'
    })
    def put(self, name, namespace):
        """
        Update Kubernetes Pod resource

        :param name: Pod name
        :param namespace: Namespace name
        :return: Kubernetes Api response DTO
        """
        pod_manifest = request.get_json()
        CRUDService.get_instance().update_pod(name, namespace, pod_manifest)
        return KubeApiResponseDto('Resource updated.'), HttpStatusCode.Accepted.value

    @api.marshal_with(KubeApiResponseDto.model, mask=None, code=HttpStatusCode.Accepted.value)
    @api.doc(responses={
        HttpStatusCode.NotFound.value: 'Provided resource not found or namespace does not exist.',
        HttpStatusCode.ServiceUnavailable.value: 'The service is unavailable.',
        HttpStatusCode.Accepted.value: 'Resource deleted.'
    })
    def delete(self, name, namespace):
        """
        Delete Kubernetes Pod resource

        :param name: Pod name
        :param namespace: Namespace name
        :return: Kubernetes Api response DTO
        """
        CRUDService.get_instance().delete_pod(name, namespace)
        return KubeApiResponseDto('Resource deleted.'), HttpStatusCode.Accepted.value
