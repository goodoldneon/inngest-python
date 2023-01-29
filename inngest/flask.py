import os
from typing import Optional

from flask import current_app, request

from .components.inngest_function import InngestFunction
from .components.inngest_comm_handler import (
    ActionResponse,
    Actions,
    ActionsRunResult,
    Handler,
    InngestCommHandler,
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
            breakpoint()
            return ActionsRunResult(
                #   fn_id: req.query[queryKeys.FnId] as string,
                #   data: req.body as Record<string, any>,
                #   env,
                #   isProduction,
                #   url,
            )

    def register():
        if request.method == "PUT":
            breakpoint()
            return ActionsRunResult(
                #   env,
                #   url,
                #   isProduction,
                #   deployId: req.query[queryKeys.DeployId]?.toString(),
            )

    def view():
        if request.method == "GET":
            # breakpoint()
            return ActionsRunResult(
                env=env,
                url=url,
                #   isIntrospection: Object.hasOwnProperty.call(
                #     req.query,
                #     queryKeys.Introspect
                #   ),
                is_introspection=False,
                is_production=False,
            )

    return Actions(
        register=register,
        run=run,
        view=view,
    )


def serve(
    name: str,
    functions: list[InngestFunction],
    options: Optional[dict] = None,
) -> Handler:
    def transform_res(action_res: ActionResponse, *args, **kwargs):
        if action_res.status == 500:
            current_app.logger.error(action_res.body)

        return action_res.body, action_res.status

    handler = InngestCommHandler(
        framework_name="express",
        app_name=name,
        functions=functions,
        handler=_serve_handler,
        options=options,
        transform_res=transform_res,
    )

    return handler.create_handler()


__all__ = ["serve"]
