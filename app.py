from flask import Flask, request
from inngest import InngestFunction, create_function
from inngest.flask import serve

app = Flask(__name__)


def example_handler(event: object) -> dict:
    print("Success!")
    # breakpoint()
    return {"body": "hello!"}


example_fn = create_function(
    "The name of my function",
    "app/flask.test",
    example_handler,
)

fns: list[InngestFunction] = [example_fn]

inngest_controller = serve("My Flask App", fns)

app.add_url_rule(
    "/api/inngest",
    methods=("GET", "POST", "PUT"),
    view_func=inngest_controller,
)
