import logging
from contextvars import ContextVar
from typing import Any, Dict

_PROTECTED_KEYS = frozenset(
    (
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "id",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "thread",
        "threadName",
        "extra",
        "auth_token",
        "password",
        "stack_info",
    )
)

_data: ContextVar[Dict[Any, Any]] = ContextVar("extra")

_sentinel = object()


class ContextFilter(logging.Filter):
    """
    ContextFilter uses an internal context dictioniary to enrich each
    LogRecord processed.
    """

    def set_entry(self, name: str, value: Any) -> None:
        """
        Sets an entry in the ContextFilter's context dictionary.
        Args:
            name: Key for the value.
            value: Value to set.
        Raises:
            ValueError - if name is in PROTECTED_KEYS.
        """
        if name in _PROTECTED_KEYS:
            raise ValueError("{name} is a protected LogRecord attribute.")
        try:
            data = _data.get()[self]
        except (LookupError, KeyError):
            self.reset()
            data = _data.get()[self]
        data[name] = value

    def set_entries(self, **entries: Any) -> None:
        """
        Sets multiple entries at once.
        Args:
            **entries - key, value
        Raises:
            ValueError - if any of the entries is in PROTECTED_KEYS.
        """
        for key, value in entries.items():
            self.set_entry(key, value)

    def reset(self) -> None:
        """
        Resets the ContextFilter's context dictioniary.
        """
        try:
            data = _data.get()
        except LookupError:
            data = dict()
            _data.set(data)
        data[self] = {}

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            data = _data.get()[self]
        except (LookupError, KeyError):
            return True
        for key, value in data.items():
            original_value = getattr(record, key, _sentinel)
            if original_value is _sentinel:
                setattr(record, key, value)
        return True
