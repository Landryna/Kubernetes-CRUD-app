from flask_restplus import fields
from main import api


class PodInputLabel:
    model = api.model(
        'PodInputLabel',
        {
            'app': fields.String()
        }
    )

    def __init__(self, labels):
        self.app = labels['app']


class PodInputMetadata:
    model = api.model(
        'PodInputMetadata',
        {
            'labels': fields.Nested(PodInputLabel.model),
        }
    )

    def __init__(self, metadata):
        self.labels = PodInputLabel(metadata['labels'])


class PodInputPort:
    model = api.model(
        'PodInputPort',
        {
            'containerPort': fields.Integer()
        }
    )

    def __init__(self, port):
        self.containerPort = port['containerPort']


class PodInputContainer:
    model = api.model(
        'PodInputContainer',
        {
            'name': fields.String(),
            'image': fields.String(),
            'ports': fields.List(fields.Nested(PodInputPort.model))
        }
    )

    def __init__(self, container):
        self.name = container['name']
        self.image = container['image']
        self.ports = [PodInputPort(port) for port in container['ports']]


class PodInputSpec:
    model = api.model(
        'PodInputSpec',
        {
            'containers': fields.List(fields.Nested(PodInputContainer.model))
        }
    )

    def __init__(self, spec):
        self.containers = spec['containers']


class PodInputDto:
    model = api.model(
        'PodInput',
        {
            'metadata': fields.Nested(PodInputMetadata.model),
            'spec': fields.Nested(PodInputSpec.model),
        }
    )

    def __init__(self, pod):
        self.metadata = PodInputMetadata(pod['metadata'])
        self.spec = PodInputSpec(pod['spec'])
