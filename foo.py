from inngest import InngestClient, Event

client = InngestClient(endpoint="http://localhost:8288", inngest_key="local")
event = Event(name="test/demo", data={"favorites": ["milk", "tea", "eggs"]})

client.send(event)
