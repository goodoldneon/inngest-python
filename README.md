# inngest-python


## Usage

```python
from inngest import InngestClient

client = InngestClient(inngest_key="your-key-here")
event = Event(name="testing.event", data={ "favorites": ["milk", "tea", "eggs"] })

client.send(event)
```
