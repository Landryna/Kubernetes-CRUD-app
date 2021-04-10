from flask_restplus import fields
from main import api


class ServiceInputPort:
    model = api.model(
        'ServiceInputPort',
        {
            'protocol': fields.String(),
            'port': fields.Integer(),
            'targetPort': fields.Integer()
        }
    )

    def __init__(self, port):
        self.protocol = port['protocol']
        self.port = port['port']
        self.targetPort = port['targetPort']


class ServiceInputSelector:
    model = api.model(
        'ServiceInputSelector',
        {
            'app': fields.String()
        }
    )

    def __init__(self, selector):
        self.app = selector['app']


class ServiceInputSpec:
    model = api.model(
        'ServiceInputSpec',
        {
            'selector': fields.Nested(ServiceInputSelector.model),
            'ports': fields.List(fields.Nested(ServiceInputPort.model))
        }
    )

    def __init__(self, spec):
        self.containers = spec['selector']
        self.ports = [ServiceInputPort(port) for port in spec['ports']]


class ServiceInputDto:
    model = api.model(
        'ServiceInputDto',
        {
            'spec': fields.Nested(ServiceInputSpec.model),
        }
    )

    def __init__(self, service):
        self.spec = ServiceInputSpec(service['spec'])
