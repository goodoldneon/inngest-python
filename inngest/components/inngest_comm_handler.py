from dataclasses import dataclass
import hashlib
import json
from typing import Callable, Optional
from urllib.request import HTTPError, Request, urlopen


Handler = Callable[[], dict]
InngestFunction = Callable

version = "0.9.3"


@dataclass
class ActionResponse:
    body: str
    headers: dict[str, str]
    status: int


@dataclass
class RegistrationResult:
    message: str
    status: int


class InngestCommHandler:
    # _fns: dict[str, InngestFunction]
    # _framework_name: str
    # _handler: Handler
    # _headers: dict[str, str]
    # _inngest_register_url: str
    # _is_prod: bool
    # _name: str
    # _serve_host: Optional[str]
    # _serve_path: Optional[str]
    # _signing_key: Optional[str]

    def __init__(
        self,
        *,
        framework_name: str,
        app_name: str,
        functions: list[InngestFunction],
        options: Optional[dict] = None,
        handler: Handler,
        transform_res: object,
    ) -> None:
        self._framework_name = framework_name
        self._handler = handler
        self._name = app_name
        self._fns: list[InngestFunction] = []
        self._inngest_register_url = "http://127.0.0.1:8288/fn/register"

        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": f"inngest-js:v{version} ({framework_name})",
        }

        self._transform_res = transform_res

    def create_handler(self) -> Handler:
        def handler(*args, **kwargs):
            action_res = self._handle_action(1)

            return self._transform_res(action_res, *args, **kwargs)

        return handler

    def _handle_action(self, actions: object) -> ActionResponse:
        register_res = self._register(
            url="http://127.0.0.1:3006/api/inngest",
        )

        return ActionResponse(
            body=json.dumps({"message": register_res.message}),
            headers={},
            status=register_res.status,
        )

    def _register(
        self,
        *,
        url: str,
        dev_server_host: Optional[str] = None,
        deployId: Optional[str] = None,
    ) -> RegistrationResult:
        body = self._register_body(url)

        req = Request(
            self._inngest_register_url,
            json.dumps(body).encode("utf-8"),
            self._headers,
        )

        try:
            with urlopen(req) as response:
                res = response.read()
                breakpoint()
        except HTTPError as error:
            return RegistrationResult(
                message=f"Failed to register; {error.read()}",
                status=500,
            )

        # with urlopen(self._inngest_register_url, {

        # }) as response:
        #     response_content = response.read()

        pass

    def _register_body(self, url: str) -> dict:
        body = {
            "url": url,
            "deployType": "ping",
            "framework": self._framework_name,
            "appName": self._name,
            # "functions": this.configs(url),
            "functions": [],
            # "sdk": this.sdkHeader[1],
            "sdk": "js:v0.9.3",
            "v": "0.1",
        }

        body["hash"] = hashlib.sha256(json.dumps(body).encode("utf-8")).hexdigest()

        return body


__all__ = [
    "Handler",
    "InngestCommHandler",
    "InngestFunction",
]
