# inngest-python


## Install

```
pip install inngest
```

## Usage

```python
from inngest import InngestClient, Event

client = InngestClient(inngest_key="your-key-here")
event = Event(name="testing.event", data={ "favorites": ["milk", "tea", "eggs"] })

client.send(event)
```
