from flask_restplus import fields
from main import api


class PodLabel:
    model = api.model(
        'PodLabel',
        {
            'app': fields.String()
        }
    )

    def __init__(self, labels):
        self.app = labels['app']


class PodMetadata:
    model = api.model(
        'PodMetadata',
        {
            'name': fields.String(),
            'labels': fields.Nested(PodLabel.model),
            'namespace': fields.String()
        }
    )

    def __init__(self, metadata):
        self.name = metadata['name']
        self.labels = PodLabel(metadata['labels'])
        self.namespace = metadata['namespace']


class PodSpec:
    model = api.model(
        'PodSpec',
        {
            'service_account': fields.String(),
            'node_name': fields.String(),
            'security_context': fields.String(),
            'service_account_name': fields.String()
        }
    )

    def __init__(self, spec):
        self.service_account = spec['serviceAccount']
        self.node_name = spec['nodeName']
        self.security_context = spec['securityContext']
        self.service_account_name = spec['serviceAccountName']


class PodContainerStatus:
    model = api.model(
        'PodContainerStatus',
        {
            'ready': fields.String(),
            'image': fields.String()
        }
    )

    def __init__(self, container_status):
        self.ready = container_status['ready']
        self.image = container_status['image']


class PodStatus:
    model = api.model(
        'PodStatus',
        {
            'phase': fields.String(),
            'container_statuses': fields.List(fields.Nested(PodContainerStatus.model)),
            'pod_ip': fields.String(),
            'host_ip': fields.String()
        }
    )

    def __init__(self, status):
        self.phase = status['phase']
        self.container_statuses = [PodContainerStatus(container) for container in status['containerStatuses']]
        self.pod_ip = status['podIP']
        self.host_ip = status['hostIP']


class PodDto:
    model = api.model(
        'Pod',
        {
            'metadata': fields.Nested(PodMetadata.model),
            'status': fields.Nested(PodStatus.model),
            'kind': fields.String(),
            'spec': fields.Nested(PodSpec.model),
            'api_version': fields.String()
        }
    )

    def __init__(self, pod):
        self.metadata = PodMetadata(pod['metadata'])
        self.status = PodStatus(pod['status'])
        self.kind = pod['kind']
        self.spec = PodSpec(pod['spec'])
        self.api_version = pod['apiVersion']
