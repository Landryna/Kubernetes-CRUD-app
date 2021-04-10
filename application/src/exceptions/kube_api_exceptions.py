class KubeApiException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ResourceNotFoundException(KubeApiException):
    pass


class InvalidResourceManifestException(KubeApiException):
    pass


class ResourceAlreadyExistException(KubeApiException):
    pass

