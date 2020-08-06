import logging

from dataclasses import dataclass

from api.src.api import BaseApiResponse, InternalErrorApiResponse
from api.src.check import CheckApiFunction
from api.src.create import CreateApiFunction

CHECK_RESOURCE = "/check"
CREATE_RESOURCE = "/create"

log = logging.getLogger(__name__)


@dataclass
class ApiEvent:
    """Class for accessing event information relevant to the API"""
    path: str
    resource: str
    http_method: str
    headers: dict

    def __str__(self):
        pass


def map_function(api_event: ApiEvent) -> BaseApiResponse:
    if api_event.http_method == "GET":
        if api_event.resource == CHECK_RESOURCE:
            log.debug(f"Event maps to method GET. resource {CHECK_RESOURCE}")
            return CheckApiFunction().run()

    if api_event.http_method == "POST":
        if api_event.resource == CREATE_RESOURCE:
            log.debug(f"Event maps to method POST, resource {CREATE_RESOURCE}")
            return CreateApiFunction().run()

    return InternalErrorApiResponse(f"No function for the path {api_event.path} for method {api_event.http_method}")


def lambda_handler(event, context):
    log.info(f"Raw Event: {event}")

    api_event = ApiEvent(
        path=event["path"],
        resource=event["resource"],
        http_method=event["httpMethod"],
        headers=event["headers"]
    )

    response = map_function(api_event)

    return response.as_dict