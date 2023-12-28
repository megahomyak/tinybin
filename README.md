# Tinybin

Tinybin is a small text sharing service similar to Pastebin.

## Installation

* `pip install tinybin`
* `pip install uvicorn` - optional, if you want to run it with uvicorn (you'll need a different ASGI-compatible server)

## Usage

```python
from tinybin import api
import uvicorn

uvicorn.run(
    api,
    port=8000,
    host="127.0.0.1",
)
```

Beware that it will create a "texts" directory at its location of startup. It will store shared texts there.
