# contextfilter
![Version](https://img.shields.io/pypi/v/contextfilter)
![License](https://img.shields.io/pypi/l/contextfilter)
![Tests](https://github.com/aviramha/contextfilter/workflows/Test%20Contextfilter/badge.svg?branch=develop)

Small, helper library for logging contextual information using contextvars in Python 3.7.

## Installation
Using pip
```
$ pip install contextfilter
```

## Usage
```py
import logging
from contextvars import ContextVar
from contextfilter import ContextVarFilter, ConstContextFilter

request_id: ContextVar[int] = ContextVar('request_id')
logger = logging.getLogger("test")
cf = ContextFilter(request_id=request_id)
request_id.set(3)
logger.addFilter(cf)
logger.info("test")
# Log record will contain the attribute request_id with value 3

cf = ConstContextFilter(some_const=1)
logger.addFilter(cf)
logger.info("test")
# Log record will contain the attribute some_const with value 1.

```

## Contributing

To work on the `contextfilter` codebase, you'll want to fork the project and clone it locally and install the required dependencies via [poetry](https://poetry.eustace.io):

```sh
$ git clone git@github.com:{USER}/contextfilter.git
$ make install
```

To run tests and linters use command below:

```sh
$ make lint && make test
```

If you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:

```sh
$ make lint-black
```

## License

`contextfilter` is licensed under the MIT license. See the license file for details.

# Latest changes

## 0.3.0 (2020-8-14)
- Renamed `ContextFilter` to `ContextVarFilter` - Revamped the API - It now accepts ContextVars created by caller. Suggestion for design by @bentheiii
- Added `ConstContextFilter` which adds constant attributes to the log record.
- Fixed #5