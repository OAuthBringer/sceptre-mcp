"""
Main entry point for the Sceptre MCP server.
"""

import argparse
import os
from sceptre_mcp.server import SceptreMCPServer

def main():
    """
    Run the Sceptre MCP server with command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Sceptre MCP Server")
    parser.add_argument(
        "--project-path", 
        help="Path to the Sceptre project (defaults to current directory)"
    )
    parser.add_argument(
        "--host", 
        default="localhost",
        help="Host to bind the server to (if using HTTP transport)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to bind the server to (if using HTTP transport)"
    )
    parser.add_argument(
        "--transport", 
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol to use"
    )
    
    args = parser.parse_args()
    
    # Create and run the server
    server = SceptreMCPServer(project_path=args.project_path)
    
    if args.transport in ["sse", "streamable-http"]:
        server.run(transport=args.transport, host=args.host, port=args.port)
    else:
        server.run(transport="stdio")

if __name__ == "__main__":
    main()
