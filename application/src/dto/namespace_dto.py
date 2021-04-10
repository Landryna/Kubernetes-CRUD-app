from flask_restplus import fields
from main import api


class NamespaceMetadata:
    model = api.model(
        'NamespaceMetadata',
        {
            'name': fields.String(),
        }
    )

    def __init__(self, metadata):
        self.name = metadata['name']


class NamespaceSpec:
    model = api.model(
        'NamespaceSpec',
        {
            'finalizers': fields.List(fields.String)
        }
    )

    def __init__(self, spec):
        self.finalizers = spec['finalizers']


class NamespaceDto:
    model = api.model(
        'Namespace',
        {
            'metadata': fields.Nested(NamespaceMetadata.model),
            'status': fields.String(),
            'kind': fields.String(),
            'spec': fields.Nested(NamespaceSpec.model),
            'api_version': fields.String()
        }
    )

    def __init__(self, namespace):
        self.metadata = NamespaceMetadata(namespace['metadata'])
        self.status = namespace['status']
        self.kind = namespace['kind']
        self.spec = NamespaceSpec(namespace['spec'])
        self.api_version = namespace['apiVersion']
