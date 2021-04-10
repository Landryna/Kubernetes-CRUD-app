from flask_restplus import fields
from main import api


class PodUpdateLabel:
    model = api.model(
        'PodUpdateLabel',
        {
            'app': fields.String()
        }
    )

    def __init__(self, labels):
        self.app = labels['app']


class PodUpdateMetadata:
    model = api.model(
        'PodUpdateMetadata',
        {
            'labels': fields.Nested(PodUpdateLabel.model)
        }
    )

    def __init__(self, metadata):
        self.labels = PodUpdateLabel(metadata['labels'])


class PodUpdateDto:
    model = api.model(
        'PodUpdate',
        {
            'metadata': fields.Nested(PodUpdateMetadata.model),
        }
    )

    def __init__(self, pod):
        self.metadata = PodUpdateMetadata(pod['metadata'])
