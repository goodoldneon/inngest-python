import os
from typing import Optional

from flask import current_app, request, Response

from .components.inngest_function import InngestFunction
from .components.inngest_comm_handler import (
    ActionResponse,
    Actions,
    ActionsRunResult,
    Handler,
    InngestCommHandler,
    StepRunData,
)


def _serve_handler() -> Actions:
    env = {k: v for k, v in os.environ.items()}
    url = request.url

    def run():
        if request.method == "POST":
            body = request.json
            assert body is not None

            return ActionsRunResult(
                fn_id=body["ctx"]["fn_id"],
                data=StepRunData(
                    event=body["event"],
                    steps=body["steps"],
                ),
                env=env,
                is_production=False,
                url=url,
            )

    def register():
        if request.method == "PUT":
            return ActionsRunResult(
                deploy_id=None,
                env=env,
                is_production=False,
                url=url,
            )

    def view():
        if request.method == "GET":
            return ActionsRunResult(
                env=env,
                #   isIntrospection: Object.hasOwnProperty.call(
                #     req.query,
                #     queryKeys.Introspect
                #   ),
                is_introspection=False,
                is_production=False,
                url=url,
            )

    return Actions(
        register=register,
        run=run,
        view=view,
    )


def _transform_res(action_res: ActionResponse):
    if action_res.status == 500:
        current_app.logger.error(action_res.body)

    return Response(
        headers=action_res.headers,
        response=action_res.body,
        status=action_res.status,
    )


def serve(
    name: str,
    functions: list[InngestFunction],
    options: Optional[dict] = None,
) -> Handler:
    handler = InngestCommHandler(
        framework_name="flask",
        app_name=name,
        functions=functions,
        handler=_serve_handler,
        options=options,
        transform_res=_transform_res,
    )

    return handler.create_handler()


__all__ = ["serve"]
