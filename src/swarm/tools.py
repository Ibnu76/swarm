"""Tool/function decorator for agents."""

from __future__ import annotations
from typing import Callable, Any
import inspect
import json


def tool(func: Callable) -> Callable:
    """Decorator to register a function as an agent tool."""
    func._is_tool = True
    func._tool_schema = _generate_schema(func)
    return func


def _generate_schema(func: Callable) -> dict:
    """Generate OpenAI-compatible function schema from type hints."""
    sig = inspect.signature(func)
    hints = func.__annotations__

    parameters = {"type": "object", "properties": {}, "required": []}

    for name, param in sig.parameters.items():
        if name == "return":
            continue
        prop: dict[str, Any] = {}
        hint = hints.get(name)
        if hint == str:
            prop["type"] = "string"
        elif hint == int:
            prop["type"] = "integer"
        elif hint == float:
            prop["type"] = "number"
        elif hint == bool:
            prop["type"] = "boolean"
        else:
            prop["type"] = "string"

        parameters["properties"][name] = prop
        if param.default is inspect.Parameter.empty:
            parameters["required"].append(name)

    return {
        "name": func.__name__,
        "description": inspect.getdoc(func) or "",
        "parameters": parameters,
    }
