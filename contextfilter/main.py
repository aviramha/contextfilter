import logging
from contextvars import ContextVar
from typing import Any

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


class ContextVarFilter(logging.Filter):
    """
    ContextVarFilter adds given context variables as attributes to each
    LogRecord processed.
    """

    def __init__(self, *args, **kwargs: ContextVar[Any]) -> None:
        """
        Initializes ContextFilter, validates that all keys are not reserved.
        Args:
            **kwargs - Context variables to set on each LogRecord
        """
        super().__init__(*args)
        for key in kwargs:
            if key in _PROTECTED_KEYS:
                raise ValueError(f"{key} is a protected LogRecord attribute")
        self._context_vars = kwargs

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Enriches the record with the context vars only if the attribute
        isn't set.
        """
        for key, value in self._context_vars.items():
            if hasattr(record, key):
                continue
            try:
                setattr(record, key, value.get())
            except LookupError:
                continue
        return True


class ConstContextFilter(logging.Filter):
    """
    ConstContextFilter adds constant variables as attributes to each LogRecord
    processed.
    """

    def __init__(self, *args, **kwargs: Any) -> None:
        """
        Initializes ContextFilter, validates that all keys are not reserved.
        Args:
            **kwargs - Attributes to set on LogRecords
        """
        super().__init__(*args)
        for key in kwargs:
            if key in _PROTECTED_KEYS:
                raise ValueError(f"{key} is a protected LogRecord attribute")
        self._variables = kwargs

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Enriches the record with the variables only if the attribute
        isn't set.
        """
        for key, value in self._variables.items():
            if hasattr(record, key):
                continue
            try:
                setattr(record, key, value)
            except LookupError:
                continue
        return True
