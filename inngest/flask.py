from typing import Optional

from flask import current_app

from .components.inngest_comm_handler import (
    ActionResponse,
    Handler,
    InngestCommHandler,
    InngestFunction,
)


def _handler():
    print("hi")
    # print(request)
    # breakpoint()
    return {
        "env": {},
        "url": "http://127.0.0.1:8080/api/inngest",
        #   url,
        "isIntrospection": False,
        "isProduction": False,
    }


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
        framework_name="flask",
        app_name=name,
        functions=functions,
        handler=_handler,
        options=options,
        transform_res=transform_res,
    )

    return handler.create_handler()


__all__ = ["serve"]
