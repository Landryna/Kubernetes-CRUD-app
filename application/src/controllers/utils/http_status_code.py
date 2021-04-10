from enum import Enum


class HttpStatusCode(Enum):
    OK = 200
    Accepted = 202
    BadRequest = 400
    Conflict = 409
    NotFound = 404
    UnprocessableEntity = 422
    ServiceUnavailable = 503
