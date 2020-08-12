import logging
from contextvars import ContextVar
from typing import Any, Dict, Hashable

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

_extra: ContextVar[Dict[Any, Any]] = ContextVar("extra")

_sentinel = object()


def set_entry(name: Hashable, value: Any) -> None:
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
        extra_dict = _extra.get()
    except LookupError:
        extra_dict = reset()
    extra_dict[name] = value


def reset() -> Dict[Any, Any]:
    """
    Resets the ContextFilter's context dictioniary.
    Returns:
        The new initialized dictioniary.
    """
    new_dict: Dict[Any, Any] = dict()
    _extra.set(new_dict)
    return new_dict


class ContextFilter(logging.Filter):
    """
    ContextFilter uses an internal context dictioniary to enrich each
    LogRecord processed.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            extra_params = _extra.get()
        except LookupError:
            return True
        for key, value in extra_params.items():
            original_value = getattr(record, key, _sentinel)
            if original_value is _sentinel:
                setattr(record, key, value)
        return True
