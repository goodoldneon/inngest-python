import dataclasses
import hashlib
import json
from typing import Callable, Optional
from urllib.request import HTTPError, Request, urlopen

from inngest.helpers.consts import EnvKeys
from inngest.types import FunctionConfig
from .inngest_function import InngestFunction

version = "0.9.3"


# @dataclasses.dataclass
# class ActionsRunResult:
#     data: dict
#     env: dict
#     fn_id: str


@dataclasses.dataclass
class StepRunData:
    event: dict
    steps: dict


@dataclasses.dataclass
class ActionsRunResult:
    env: dict
    is_production: bool
    url: str
    data: Optional[StepRunData] = None
    deploy_id: Optional[str] = None
    is_introspection: Optional[bool] = None
    fn_id: Optional[str] = None


@dataclasses.dataclass
class StepRunResponse:
    pass


@dataclasses.dataclass
class Actions:
    register: Callable[[], Optional[ActionsRunResult]]
    run: Callable[[], Optional[ActionsRunResult]]
    view: Callable[[], Optional[ActionsRunResult]]


Handler = Callable[[], Actions]


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def encode_json(data: object) -> str:
    return json.dumps(data, cls=JsonEncoder)


@dataclasses.dataclass
class ActionResponse:
    body: str
    headers: dict[str, str]
    status: int


@dataclasses.dataclass
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
        transform_res: Callable,
    ) -> None:
        self._framework_name = framework_name
        self._handler = handler
        self._name = app_name
        # self._fns: list[InngestFunction] = []
        self._inngest_register_url = "http://127.0.0.1:8288/fn/register"

        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": f"inngest-js:v{version} ({framework_name})",
        }

        self._signing_key = None
        self._transform_res = transform_res

        self._fns = dict[str, InngestFunction]()
        for fn in functions:
            fn_id = fn.id(self._name)

            if fn_id in self._fns:
                raise Exception(
                    f'Duplicate function ID "{fn_id}"; please change a function\'s name or provide an explicit ID to avoid conflicts.'
                )

            self._fns[fn_id] = fn

    def _configs(self, url: str) -> list[FunctionConfig]:
        return [fn.get_config(url, self._name) for fn in self._fns.values()]

    def create_handler(self) -> Handler:
        def handler(*args, **kwargs):
            actions = self._handler(*args, **kwargs)
            action_res = self._handle_action(actions)

            return self._transform_res(action_res, *args, **kwargs)

        return handler

    def _handle_action(self, actions: Actions) -> ActionResponse:
        headers = {"x-inngest-sdk": "".join(self._sdk_header)}

        run_res = actions.run()
        if run_res:
            self._upsert_signing_key_from_env(run_res.env)

            assert run_res.fn_id is not None
            assert run_res.data is not None
            step_res = self._run_step(run_res.fn_id, "step", run_res.data)

            return ActionResponse(
                # body=encode_json({"message": step_res.body}),
                body=encode_json({}),
                headers={
                    **headers,
                    "Content-Type": "application/json"
                },
                # status=step_res.status,
                status=200,
            )

        view_res = actions.view()
        if view_res:
            self._upsert_signing_key_from_env(view_res.env)

            return ActionResponse(
                body="",
                headers={
                    **headers,
                    "Content-Type": "application/json"
                },
                status=200,
            )

        register_res = actions.register()
        if register_res:
            self._upsert_signing_key_from_env(register_res.env)

            registration_res = self._register(
                url="http://127.0.0.1:3006/api/inngest",
            )
            print(6)
            return ActionResponse(
                body=encode_json({"message": registration_res.message}),
                headers={
                    **headers,
                    "Content-Type": "application/json"
                },
                status=registration_res.status,
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
            encode_json(body).encode("utf-8"),
            self._headers,
        )

        try:
            with urlopen(req) as response:
                body = json.loads(response.read())
        except HTTPError as error:
            return RegistrationResult(
                message=f"Failed to register; {error.read()}",
                status=500,
            )

        return RegistrationResult(
            message="OK",
            status=response.status,
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
            "functions": self._configs(url),
            "sdk": self._sdk_header[1],
            "v": "0.1",
        }

        body["hash"] = hashlib.sha256(encode_json(body).encode("utf-8")).hexdigest()

        return body

    def _run_step(
        self,
        function_id: str,
        step_id: str,
        data: StepRunData,
    ) -> StepRunResponse:
        fn = self._fns.get(function_id)
        if fn is None:
            raise Exception(f'Could not find function with ID "{function_id}"')

        ret = fn.run_fn(data.event, data.steps)

    @property
    def _sdk_header(self) -> tuple[str, str, str]:
        return ("inngest-", f"js:v{version}", f" ({self._framework_name})")

    def _upsert_signing_key_from_env(self, env: dict) -> None:
        if not self._signing_key and EnvKeys.SigningKey in env:
            self._signing_key = env[EnvKeys.SigningKey]


__all__ = [
    "ActionResponse",
    "Handler",
    "InngestCommHandler",
    "InngestFunction",
]
