#!/usr/bin/env python3
"""
Test script to verify that the MCP server can be imported and initialized properly.
This verifies the basic functionality without starting the actual server.
"""
import asyncio
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_mcp_initialization():
    """
    Test that MCP server can be imported and initialized without errors.
    """
    print("Testing MCP server initialization...")

    try:
        # Test importing the main server components
        from app.mcp.server.server import mcp_server, get_server
        print("[OK] Successfully imported MCP server components")

        # Test getting the server instance
        server = get_server()
        assert server is not None
        print("[OK] Successfully retrieved server instance")

        # Test that tools are registered
        from app.mcp.tools import (
            ADD_TASK_TOOL,
            LIST_TASKS_TOOL,
            UPDATE_TASK_TOOL,
            DELETE_TASK_TOOL,
            COMPLETE_TASK_TOOL
        )
        print("[OK] Successfully imported all MCP tools")

        # Verify tool properties
        tools = [
            ("add_task", ADD_TASK_TOOL),
            ("list_tasks", LIST_TASKS_TOOL),
            ("update_task", UPDATE_TASK_TOOL),
            ("delete_task", DELETE_TASK_TOOL),
            ("complete_task", COMPLETE_TASK_TOOL)
        ]

        for name, tool in tools:
            assert hasattr(tool, 'name'), f"{name} missing name"
            assert hasattr(tool, 'description'), f"{name} missing description"
            assert hasattr(tool, 'inputSchema'), f"{name} missing inputSchema"
            print(f"[OK] Verified {name} tool properties")

        # Test configuration import
        from app.mcp.config import settings, get_config_summary
        print("[OK] Successfully imported MCP configuration")

        # Test getting config summary
        config_summary = get_config_summary()
        assert isinstance(config_summary, dict)
        print("[OK] Successfully retrieved configuration summary")

        print("\nAll MCP initialization tests passed!")
        print("The MCP server can be properly imported and initialized.")
        return True

    except Exception as e:
        print(f"\nError during MCP initialization test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_functions():
    """
    Test that tool handler functions are properly defined.
    """
    print("\nTesting MCP tool handler functions...")

    try:
        from app.mcp.tools import (
            handle_add_task,
            handle_list_tasks,
            handle_update_task,
            handle_delete_task,
            handle_complete_task
        )

        # Verify they are callable
        assert callable(handle_add_task)
        assert callable(handle_list_tasks)
        assert callable(handle_update_task)
        assert callable(handle_delete_task)
        assert callable(handle_complete_task)

        print("[OK] All tool handler functions are properly defined")
        return True

    except Exception as e:
        print(f"Error testing tool functions: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Testing MCP Server Setup\n")

    success1 = test_mcp_initialization()
    success2 = test_tool_functions()

    if success1 and success2:
        print("\nAll tests passed! MCP server is ready for use.")
        sys.exit(0)
    else:
        print("\nSome tests failed. Please check the implementation.")
        sys.exit(1)