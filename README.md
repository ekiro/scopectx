# scopectx [![PyPI](https://img.shields.io/pypi/pyversions/scopectx.svg)](https://pypi.python.org/pypi/scopectx/) [![Build Status](https://travis-ci.org/ekiro/scopectx.svg?branch=master)](https://travis-ci.org/ekiro/scopectx)
Simple scoped context library. scopectx allows you to use context object
attached to some specific execution scope (see usage examples). 
Just like `threading.local`, but for `with` block.

# Installation

    pip install scopectx
    
# Usage examples

Simplest possible usage

```python
from scopectx import Context

ctx = Context()

def some_function(s):
    assert ctx['hello'] == s
    
def nested_context():
    with ctx:
        ctx['hello'] = 'kiro'
        some_function('kiro')
    
with ctx:
    ctx['hello'] = 'world'
    some_function('world')
    nested_context()
    assert ctx['hello'] == 'world'
```

Request context in some web framework:

```python
# my_framework/app.py

from scopectx import Context

request_ctx = Context()

def _handle_request(app, request):
    f = app.get_handler(request)
    with request_ctx:
        request_ctx['db_session'] = DbSession()  # one request = one DbSession
        respoonse = f(request.content)
        request_ctx['db_session'].close()
    return response



# my_project/my_fancy_resource.py

from my_framework.app import request_ctx

def index_handler(content):
    request_ctx['some_variable'] = 'some_value'
    some_fancy_function_also_using_db_session()    
    request_ctx['db_session'].drop_the_base()
    return "hello world"

```

## Documentation

### scopectx.Context

Base context class, creates new data for every `with` block.

### scopectx.MultiLevelContext

Just like `Context`, but in nested `with` block, it returns value from an
 outer block, instead of rising `KeyError` (in case you will not overwrite it,
 and it's defined somewhere upper):

```python
from scopectx import MultiLevelContext

ctx = MultiLevelContext()


def nested():
    with ctx:
        try:
            print(ctx['sth'])  # will raise KeyError
        except KeyError:
            pass
        print(ctx['hello'])  # 'world'
        ctx['hello'] = 'kiro'
        print(ctx['hello'])  # 'kiro'


with ctx:
    ctx['hello'] = 'world'
    print(ctx['hello'])  # 'world'
    nested()
    print(ctx['hello'])  # still 'world'
```
