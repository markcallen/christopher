"""Tests for the MathServer class that handles mathematical expression evaluation."""

import pytest

from mcp_servers.math_server import MathServer


@pytest.fixture
def math_server():
    """Create a MathServer instance for testing."""
    return MathServer()


@pytest.mark.asyncio
async def test_math_server_basic_operations(math_server):
    """Test basic arithmetic operations."""
    test_cases = [
        ("2 + 2", "Result: 4.0"),
        ("10 - 5", "Result: 5.0"),
        ("3 * 4", "Result: 12.0"),
        ("15 / 3", "Result: 5.0"),
        ("2 ** 3", "Result: 8.0"),
        ("-5", "Result: -5.0"),
    ]

    for expression, expected in test_cases:
        result = await math_server.send_request(expression)
        assert result == expected


@pytest.mark.asyncio
async def test_math_server_complex_expressions(math_server):
    """Test more complex mathematical expressions."""
    test_cases = [
        ("2 + 3 * 4", "Result: 14.0"),  # Tests operator precedence
        ("(2 + 3) * 4", "Result: 20.0"),  # Tests parentheses
        ("10 - 5 * 2 + 3", "Result: 3.0"),  # Tests multiple operations
    ]

    for expression, expected in test_cases:
        result = await math_server.send_request(expression)
        assert result == expected


@pytest.mark.asyncio
async def test_math_server_error_handling(math_server):
    """Test error handling for invalid expressions."""
    test_cases = [
        (
            "2 + ",
            ("Error evaluating expression: invalid syntax (<unknown>, line 1)"),
        ),
        ("abc", "Error evaluating expression: Unsupported node type: Name"),
        ("1j", "Error evaluating expression: Complex numbers are not supported"),
    ]

    for expression, expected in test_cases:
        result = await math_server.send_request(expression)
        assert result == expected, f"Expected '{expected}' but got '{result}'"


@pytest.mark.asyncio
async def test_math_server_unsupported_operations(math_server):
    """Test handling of unsupported operations."""
    test_cases = [
        ("2 % 3", "Error evaluating expression: Unsupported operation: Mod"),
        ("2 // 3", "Error evaluating expression: Unsupported operation: FloorDiv"),
        ("~2", "Error evaluating expression: Unsupported operation: Invert"),
    ]

    for expression, expected in test_cases:
        result = await math_server.send_request(expression)
        assert result == expected, f"Expected '{expected}' but got '{result}'"
