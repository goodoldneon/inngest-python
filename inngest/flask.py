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


def _serve_handler(*args, **kwargs) -> Actions:
    # print("hi")
    # # print(request)
    # breakpoint()
    # return {
    #     "env": {},
    #     "url": "http://127.0.0.1:8080/api/inngest",
    #     #   url,
    #     "isIntrospection": False,
    #     "isProduction": False,
    # }

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
            # breakpoint()
            return ActionsRunResult(
                deploy_id=None,
                env=env,
                is_production=False,
                url=url,
            )

    def view():
        if request.method == "GET":
            # breakpoint()
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


def _transform_res(action_res: ActionResponse, *args, **kwargs):
    if action_res.status == 500:
        current_app.logger.error(action_res.body)

    # if request.method == "PUT":
    #     breakpoint()
    #     pass

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
        framework_name="express",
        app_name=name,
        functions=functions,
        handler=_serve_handler,
        options=options,
        transform_res=_transform_res,
    )

    return handler.create_handler()


__all__ = ["serve"]
