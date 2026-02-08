#!/usr/bin/env python3
"""
Script to run the MCP (Model Context Protocol) server for the Todo AI Chatbot.
This server provides tools for AI agents to interact with the todo system.
"""
import asyncio
import sys
import os
import argparse

# Add the app directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from mcp.main import start_mcp_server

def main():
    parser = argparse.ArgumentParser(description='Run Todo AI MCP Server')
    parser.add_argument('--host', default='localhost', help='Host to bind to (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--ssl', action='store_true', help='Enable SSL')

    args = parser.parse_args()

    # Set environment variables based on arguments
    os.environ.setdefault('MCP_SERVER_HOST', args.host)
    os.environ.setdefault('MCP_SERVER_PORT', str(args.port))
    os.environ.setdefault('MCP_SERVER_SSL', str(args.ssl).lower())

    print(f"Starting Todo AI MCP Server on {args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")

    try:
        asyncio.run(start_mcp_server())
    except KeyboardInterrupt:
        print("\nMCP Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error running MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()