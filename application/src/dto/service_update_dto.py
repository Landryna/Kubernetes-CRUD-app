from flask_restplus import fields
from main import api


class ServiceUpdateSelector:
    model = api.model(
        'ServiceUpdateSelector',
        {
            'app': fields.String()
        }
    )

    def __init__(self, selector):
        self.app = selector['app']


class ServiceUpdateSpec:
    model = api.model(
        'ServiceUpdateMetadata',
        {
            'selector': fields.Nested(ServiceUpdateSelector.model),
        }
    )

    def __init__(self, spec):
        self.selector = ServiceUpdateSelector(spec['selector'])


class ServiceUpdateDto:
    model = api.model(
        'ServiceUpdate',
        {
            'spec': fields.Nested(ServiceUpdateSpec.model),
        }
    )

    def __init__(self, service):
        self.spec = ServiceUpdateSpec(service['spec'])
