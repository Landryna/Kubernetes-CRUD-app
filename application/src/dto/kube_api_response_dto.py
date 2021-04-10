from flask_restplus import fields
from main import api


class KubeApiResponseDto:
    model = api.model(
        'KubeApiResponse',
        {
            'message': fields.String()
        }
    )

    def __init__(self, message):
        self.message = message
