"""Tests for the configuration module."""

from core.config import CONFIG


def test_config_structure():
    """Test that the CONFIG dictionary has the expected structure."""
    # Verify the required keys exist
    assert "mcp_servers" in CONFIG
    assert "agents" in CONFIG

    # Verify the types of the values
    assert isinstance(CONFIG["mcp_servers"], list)
    assert isinstance(CONFIG["agents"], list)


def test_mcp_servers_content():
    """Test the content of mcp_servers configuration."""
    assert "math" in CONFIG["mcp_servers"]
    assert len(CONFIG["mcp_servers"]) == 1


def test_agents_content():
    """Test the content of agents configuration."""
    expected_agents = ["weather", "math", "writing", "programming"]
    assert all(agent in CONFIG["agents"] for agent in expected_agents)
    assert len(CONFIG["agents"]) == len(expected_agents)
    # Verify no unexpected agents are present
    assert set(CONFIG["agents"]) == set(expected_agents)
