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
from contextfilter import ContextFilter, set_entry, set_entries

logger = logging.getLogger("test")
cf = ContextFilter()
logger.addFilter(cf)
cf.set_entry("request_id", 3)
# or
cf.set_entries(request_id=3)
logger.info("test")
# Log record will contain the attribute request_id with value 3
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

## 0.3.0 (2020-8-13)
- You can now use multiple `ContextFilter`s in same runtime. All functions moved to be under the `ContextFilter`'s instance.
- `reset` returns nothing now