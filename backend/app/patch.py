
import sys
from typing import ForwardRef
import pydantic.typing

# Monkeypatch pydantic 1.x for Python 3.13 compatibility
if sys.version_info >= (3, 13):
    _original_evaluate_forwardref = pydantic.typing.evaluate_forwardref

    def _patched_evaluate_forwardref(type_, globalns, localns):
        if isinstance(type_, ForwardRef):
             # Python 3.13 requires recursive_guard as keyword arg
             return type_._evaluate(globalns, localns, recursive_guard=set())
        return _original_evaluate_forwardref(type_, globalns, localns)

    pydantic.typing.evaluate_forwardref = _patched_evaluate_forwardref
