"""
MCP Server Main Entry Point
Starts the Model Context Protocol server for the Todo AI Chatbot.
"""
import asyncio
import os
from mcp.server import Server
from .server.server import mcp_server
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8080"))
MCP_SERVER_SSL = os.getenv("MCP_SERVER_SSL", "false").lower() == "true"

async def start_mcp_server():
    """
    Start the MCP server.
    """
    logger.info(f"Starting Todo AI MCP Server on {MCP_SERVER_HOST}:{MCP_SERVER_PORT}")

    try:
        # Start the server
        await mcp_server.run(
            host=MCP_SERVER_HOST,
            port=MCP_SERVER_PORT,
            ssl=MCP_SERVER_SSL
        )
    except KeyboardInterrupt:
        logger.info("MCP Server shutdown requested")
    except Exception as e:
        logger.error(f"Error starting MCP server: {e}")
        raise


if __name__ == "__main__":
    # Run the server
    asyncio.run(start_mcp_server())