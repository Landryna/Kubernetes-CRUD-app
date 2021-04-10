from flask_restplus import fields
from main import api


class ServiceMetadata:
    model = api.model(
        'ServiceMetadata',
        {
            'name': fields.String(),
            'namespace': fields.String()
        }
    )

    def __init__(self, metadata):
        self.name = metadata['name']
        self.namespace = metadata['namespace']


class ServiceSelector:
    model = api.model(
        'ServiceSelector',
        {
            'app': fields.String()
        }
    )

    def __init__(self, selector):
        self.app = selector['app']


class ServicePort:
    model = api.model(
        'ServicePort',
        {
            'port': fields.String(),
            'protocol': fields.String(),
            'target_port': fields.String()
        }
    )

    def __init__(self, port):
        self.port = port['port']
        self.protocol = port['protocol']
        self.target_port = port['targetPort']


class ServiceSpec:
    model = api.model(
        'ServiceSpec',
        {
            'selector': fields.Nested(ServiceSelector.model),
            'cluster_ip': fields.String(),
            'type': fields.String(),
            'ports': fields.List(fields.Nested(ServicePort.model))
        }
    )

    def __init__(self, spec):
        self.selector = ServiceSelector(spec['selector'])
        self.cluster_ip = spec['clusterIP']
        self.type = spec['type']
        self.ports = [ServicePort(port) for port in spec['ports']]


class ServiceDto:
    model = api.model(
        'Service',
        {
            'metadata': fields.Nested(ServiceMetadata.model),
            'kind': fields.String(),
            'spec': fields.Nested(ServiceSpec.model),
            'api_version': fields.String()
        }
    )

    def __init__(self, service):
        self.metadata = ServiceMetadata(service['metadata'])
        self.kind = service['kind']
        self.spec = ServiceSpec(service['spec'])
        self.api_version = service['apiVersion']
