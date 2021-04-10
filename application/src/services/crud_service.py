import json

from kubernetes import client
from kubernetes.client.exceptions import ApiException

from controllers.utils.http_status_code import HttpStatusCode
from controllers.utils.kind import Kind
from exceptions.app_exceptions import ServiceUnavailable
from exceptions.kube_api_exceptions import ResourceNotFoundException, ResourceAlreadyExistException, \
    InvalidResourceManifestException


class CRUDService:
    _instance = None

    @staticmethod
    def get_instance():
        if CRUDService._instance is None:
            CRUDService()
        return CRUDService._instance

    def __init__(self):
        if CRUDService._instance is not None:
            raise Exception('This class is a singleton!')
        else:
            CRUDService._instance = self

    def convert_k8s_resource(self, resource):
        """
        Convert retrieved and not deserialized Kubernetes object into Python dict

        :param resource: Kubernetes resource
        :return: Kubernetes object converted into Python dict
        """
        # Decode Kubernetes object from bytes to str.
        resource = resource.data.decode('utf-8')
        return json.loads(resource)

    def convert_kube_api_error_msg_output(self, error_msg):
        """
        Convert retrieved Kubernetes exception body into Python dict

        :param error_msg: Exception message
        :return: Kubernetes Exception converted into Python dict
        """
        # Decode Kubernetes object from bytes to str.
        error_msg = error_msg.decode('utf-8')
        return json.loads(error_msg)

    def handle_kube_api_exception(self, exception):
        """
        Handle Kubernetes Api Exception

        :param exception: Kubernetes Api Exception
        """
        error_msg = self.convert_kube_api_error_msg_output(exception.body)
        if error_msg['code'] == HttpStatusCode.NotFound.value:
            raise ResourceNotFoundException('Provided resource not found or namespace does not exist.')
        elif error_msg['code'] == HttpStatusCode.Conflict.value:
            raise ResourceAlreadyExistException('Resource already exist.')
        elif error_msg['code'] == HttpStatusCode.BadRequest.value or HttpStatusCode.UnprocessableEntity.value:
            raise InvalidResourceManifestException('Invalid request body. Check if provided values are correct.')
        else:
            raise ServiceUnavailable('The service is unavailable.')

    def get_modified_resource_metadata(
            self,
            resource_manifest,
            name,
            kind, api_version,
            namespace=None):
        """
        Get modified Kubernetes resource metadata

        :param resource_manifest: Not modified resource manifest
        :param name: Resource name
        :param kind: Kind
        :param api_version: Api version
        :param namespace: Namespace resource
        :return: Modified resource metadata
        """
        if 'metadata' not in resource_manifest:
            resource_manifest['metadata'] = {}
        if namespace:
            resource_manifest['metadata']['namespace'] = namespace
        resource_manifest['metadata']['name'] = name
        resource_manifest['kind'] = kind
        resource_manifest['apiVersion'] = api_version
        return resource_manifest

    def get_namespace(self, namespace):
        """
        Get Kubernetes Namespace resource

        :param namespace:  Namespace resource
        :return: Namespace resource converted as Python dict
        """
        try:
            return self.convert_k8s_resource(
                client.CoreV1Api().read_namespace(namespace, _preload_content=False)
            )
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def get_service(self, service, namespace):
        """
        Get Kubernetes Service resource

        :param service: Service resource
        :param namespace: Namespace resource
        :return: Service resource converted as Python dict
        """
        try:
            return self.convert_k8s_resource(
                client.CoreV1Api().read_namespaced_service(service, namespace, _preload_content=False)
            )
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def get_pod(self, pod, namespace):
        """
        Get Kubernetes Pod resource

        :param pod: Pod resource
        :param namespace: Namespace resource
        :return: Pod resource converted as Python dict
        """
        try:
            return self.convert_k8s_resource(
                client.CoreV1Api().read_namespaced_pod(pod, namespace, _preload_content=False)
            )
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def get_list_of_resources(self, kind, namespace):
        """
        Get list of Kubernetes resources

        :param kind: Resource kind
        :param namespace: Namespace resource
        :return: List of Kubernetes resources
        """
        if kind.lower() == Kind.POD.value.lower():
            return self.convert_k8s_resource(
                client.CoreV1Api().list_namespaced_pod(namespace, _preload_content=False)
            )
        elif kind.lower() == Kind.SERVICE.value.lower():
            return self.convert_k8s_resource(
                client.CoreV1Api().list_namespaced_service(namespace, _preload_content=False)
            )
        elif kind.lower() == Kind.NAMESPACE.value.lower():
            return self.convert_k8s_resource(
                client.CoreV1Api().list_namespace(_preload_content=False)
            )
        else:
            raise ResourceNotFoundException('Provided kind is not supported.')

    def delete_namespace(self, namespace):
        """
        Delete Kubernetes Namespace resource

        :param namespace: Namespace resource
        """
        try:
            client.CoreV1Api().delete_namespace(namespace, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def delete_service(self, service, namespace):
        """
        Delete Kubernetes Service resource in provided Namespace

        :param service: Service resource
        :param namespace: Namespace resource
        """
        try:
            client.CoreV1Api().delete_namespaced_service(service, namespace, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def delete_pod(self, pod, namespace):
        """
        Delete Kubernetes Pod resource in provided Namespace

        :param pod: Pod resource
        :param namespace: Namespace resource
        """
        try:
            client.CoreV1Api().delete_namespaced_pod(pod, namespace, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def create_pod(self, name, namespace, pod_manifest):
        """
        Create Kubernetes Pod resource in provided Namespace using Pod manifest body

        :param name: Pod resource name
        :param namespace: Namespace resource
        :param pod_manifest: Pod resource manifest body
        """
        pod_manifest = self.get_modified_resource_metadata(
            pod_manifest, name, Kind.POD.value, Kind.VERSION.value, namespace=namespace
        )
        try:
            client.CoreV1Api().create_namespaced_pod(namespace, pod_manifest, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def create_service(self, name, namespace, service_manifest):
        """
        Create Kubernetes Service resource in provided Namespace using Service manifest body

        :param name: Service resource name
        :param namespace: Namespace resource
        :param service_manifest: Service resource manifest body
        """
        service_manifest = self.get_modified_resource_metadata(
            service_manifest, name, Kind.SERVICE.value, Kind.VERSION.value, namespace=namespace)
        try:
            client.CoreV1Api().create_namespaced_service(namespace, service_manifest, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def create_namespace(self, name):
        """
        Create Kubernetes Namespace resource

        :param name: Kubernetes Namespace resource name
        """
        try:
            namespace_manifest = self.get_modified_resource_metadata({}, name, Kind.NAMESPACE.value, Kind.VERSION.value)
            client.CoreV1Api().create_namespace(namespace_manifest, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def update_pod(self, name, namespace, pod_manifest):
        """
        Update existing Kubernetes Pod resource in provided Namespace using Pod manifest body

        :param name: Pod resource name
        :param namespace: Namespace resource
        :param pod_manifest: Pod resource manifest body
        """
        try:
            client.CoreV1Api().patch_namespaced_pod(name, namespace, pod_manifest, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)

    def update_service(self, name, namespace, service_manifest):
        """
        Update existing Kubernetes Service resource in provided Namespace using Service manifest body

        :param name: Service resource name
        :param namespace: Namespace resource
        :param service_manifest: Service resource manifest body
        """
        try:
            client.CoreV1Api().patch_namespaced_service(name, namespace, service_manifest, _preload_content=False)
        except ApiException as e:
            self.handle_kube_api_exception(e)
