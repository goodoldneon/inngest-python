from flask import Flask, request
from inngest.flask import serve

app = Flask(__name__)


inngest_controller = serve("My Flask App", [])

app.add_url_rule("/api/inngest", view_func=inngest_controller)
