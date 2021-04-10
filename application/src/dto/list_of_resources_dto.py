from flask_restplus import fields
from main import api


class ListOfResourcesDto:
    model = api.model(
        'ListOfResources',
        {
            'resources': fields.List(fields.String()),
        }
    )

    def __init__(self, resources):
        self.resources = [resource['metadata']['name'] for resource in resources['items']]

