# Reloadable
Reruns a function upon failure

## Usage
The function `my_func` will run indefinitely until it stops raising exceptions,
which will never happen in this case.

```python
from reloadable import reloadable

@reloadable()
def my_func():
    raise Exception('Oops')
```

This module is useful when we want to run something for ever, like a code
that connects to a queue en fetches messages. Eventually it may disconnect and
raise an error trying to fetch a message, so reloadable can retry connecting.

```python
@reloadable()
def get_message():
    conn = Queue(host='...', password='...')
    
    while True:
        message = conn.fetch_message()
        # probably process message afterwards...
```

You can config a callback function that receives an exception, which will be
called if it occurs.

```python
def shit_happens(exception):
    logger.exception(exception)

@reloadable(exception_callback=shit_happens)
def dont_stop():
    raise Exception('Deal with it')
```

You can also wait some time before the next respawn

```python
@reloadable(sleep_time=7)  # wait 7 seconds before running `get_message` after a failure 
def get_message():
    # some code...
```

You can always stop reloadable with a `KeyboardInterrupt` exception
(usually triggered by ^C, but not necessarily)

## Tests
`python -m unittest -v tests`

## Installation
`pip install reloadable`
