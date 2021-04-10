from enum import Enum


class Kind(Enum):
    POD = 'Pod'
    SERVICE = 'Service'
    NAMESPACE = 'Namespace'
    VERSION = 'v1'
