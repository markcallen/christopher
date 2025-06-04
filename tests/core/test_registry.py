"""Tests for the agent registry module."""

import pytest

from core.registry import AGENT_REGISTRY, agent


class TestAgent:
    """Test agent class for registry testing."""

    description = "A test agent for unit testing"


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear the agent registry before and after each test."""
    AGENT_REGISTRY.clear()
    yield
    AGENT_REGISTRY.clear()


def test_agent_registration():
    """Test successful registration of an agent."""
    # Register a test agent
    decorated_agent = agent("test_agent")(TestAgent)

    # Verify the agent was registered correctly
    assert "test_agent" in AGENT_REGISTRY
    assert isinstance(AGENT_REGISTRY["test_agent"]["instance"], TestAgent)
    assert (
        AGENT_REGISTRY["test_agent"]["description"] == "A test agent for unit testing"
    )

    # Verify the decorator returns the original class
    assert decorated_agent is TestAgent


def test_agent_registration_missing_description():
    """Test that registering an agent without a description raises ValueError."""

    class InvalidAgent:
        pass

    # Attempt to register an agent without a description
    with pytest.raises(ValueError, match="must have a 'description' class variable"):
        agent("invalid_agent")(InvalidAgent)

    # Verify the agent was not registered
    assert "invalid_agent" not in AGENT_REGISTRY


def test_multiple_agent_registration():
    """Test registering multiple agents in the registry."""

    class AnotherAgent:
        description = "Another test agent"

    # Register multiple agents
    agent("agent1")(TestAgent)
    agent("agent2")(AnotherAgent)

    # Verify both agents were registered
    assert len(AGENT_REGISTRY) == 2
    assert "agent1" in AGENT_REGISTRY
    assert "agent2" in AGENT_REGISTRY
    assert isinstance(AGENT_REGISTRY["agent1"]["instance"], TestAgent)
    assert isinstance(AGENT_REGISTRY["agent2"]["instance"], AnotherAgent)
    assert AGENT_REGISTRY["agent1"]["description"] == "A test agent for unit testing"
    assert AGENT_REGISTRY["agent2"]["description"] == "Another test agent"
