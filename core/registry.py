"""Registry module for managing agent registration and discovery.

This module provides a decorator-based registration system for agents, allowing
them to be discovered and instantiated dynamically throughout the application.
"""

from collections.abc import Callable
from typing import Any, Protocol, TypeVar


class AgentProtocol(Protocol):
    """Protocol defining the required interface for agent classes."""

    description: str


T = TypeVar("T", bound=AgentProtocol)

AGENT_REGISTRY: dict[str, dict[str, Any]] = {}


def agent(name: str) -> Callable[[type[T]], type[T]]:
    """Register an agent class with the global registry.

    Args:
    ----
        name: The unique identifier for the agent in the registry

    Returns:
    -------
        A decorator function that registers the agent class

    Raises:
    ------
        ValueError: If the agent class is missing a description attribute

    """

    def decorator(cls: type[T]) -> type[T]:
        if not hasattr(cls, "description"):
            raise ValueError(
                f"Agent class {cls.__name__} must have a 'description' class variable"
            )
        AGENT_REGISTRY[name] = {"instance": cls(), "description": cls.description}
        return cls

    return decorator
