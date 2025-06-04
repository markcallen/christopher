"""Test suite for the CLI module.

This module contains tests for the command-line interface functionality,
including conversation flows, exit commands, and error handling.
"""

from unittest.mock import AsyncMock, patch

import pytest

from cli.cli import main


@pytest.fixture
def mock_inquirer():
    """Mock the inquirer module to simulate user input.

    Returns
    -------
        Mock: A mock object that simulates the inquirer module's behavior.

    """
    with patch("cli.cli.inquirer") as mock:
        mock.text = AsyncMock()
        yield mock


@pytest.fixture
def mock_core_functions():
    """Mock the core functions that interact with the LLM.

    Returns
    -------
        tuple: A tuple containing mocked load_agents and run_with_langgraph functions.

    """
    with (
        patch("cli.cli.load_agents") as mock_load,
        patch("cli.cli.run_with_langgraph", new_callable=AsyncMock) as mock_run,
    ):
        yield mock_load, mock_run


@pytest.mark.asyncio
async def test_cli_basic_conversation(mock_inquirer, mock_core_functions):
    """Test a basic conversation flow in the CLI.

    Args:
    ----
        mock_inquirer: Mocked inquirer module for simulating user input.
        mock_core_functions: Tuple of mocked core functions
        (load_agents, run_with_langgraph).

    """
    mock_load, mock_run = mock_core_functions

    # Set up the mock responses
    mock_inquirer.text.side_effect = ["Hello", "How are you?", "exit"]
    mock_run.return_value = "I'm doing well, thank you!"

    # Run the main function
    await main()

    # Verify the interactions
    assert mock_load.call_count == 1
    assert mock_run.call_count == 2

    # Verify the correct messages were passed to run_with_langgraph
    mock_run.assert_any_call("Hello")
    mock_run.assert_any_call("How are you?")


@pytest.mark.asyncio
async def test_cli_exit_immediately(mock_inquirer, mock_core_functions):
    """Test that the CLI exits immediately when 'exit' is entered.

    Args:
    ----
        mock_inquirer: Mocked inquirer module for simulating user input.
        mock_core_functions: Tuple of mocked core functions
        (load_agents, run_with_langgraph).

    """
    mock_load, mock_run = mock_core_functions

    # Set up the mock to return 'exit' immediately
    mock_inquirer.text.return_value = "exit"

    # Run the main function
    await main()

    # Verify the interactions
    assert mock_load.call_count == 1
    assert mock_run.call_count == 0


@pytest.mark.asyncio
async def test_cli_quit_command(mock_inquirer, mock_core_functions):
    """Test that the CLI exits when 'quit' is entered.

    Args:
    ----
        mock_inquirer: Mocked inquirer module for simulating user input.
        mock_core_functions: Tuple of mocked core functions
        (load_agents, run_with_langgraph).

    """
    mock_load, mock_run = mock_core_functions

    # Set up the mock to return 'quit'
    mock_inquirer.text.return_value = "quit"

    # Run the main function
    await main()

    # Verify the interactions
    assert mock_load.call_count == 1
    assert mock_run.call_count == 0


@pytest.mark.asyncio
async def test_cli_error_handling(mock_inquirer, mock_core_functions):
    """Test that the CLI handles errors from run_with_langgraph gracefully.

    Args:
    ----
        mock_inquirer: Mocked inquirer module for simulating user input.
        mock_core_functions: Tuple of mocked core functions
        (load_agents, run_with_langgraph).

    """
    mock_load, mock_run = mock_core_functions

    # Set up the mock responses
    mock_inquirer.text.side_effect = ["Hello", "exit"]
    mock_run.side_effect = Exception("Test error")

    # Run the main function
    await main()

    # Verify the interactions
    assert mock_load.call_count == 1
    assert mock_run.call_count == 1
