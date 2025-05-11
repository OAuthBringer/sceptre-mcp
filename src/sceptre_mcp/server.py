"""
Sceptre MCP Server - A dead simple wrapper around the Sceptre CLI.
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Any

from fastmcp import FastMCP


class SceptreMCPServer:
    """Wrapper around Sceptre CLI commands."""

    def __init__(self, project_path: Optional[str] = None):
        """Initialize with project path."""
        self.project_path = project_path or os.getcwd()
        self.server = FastMCP("SceptreMCP")
        
        # Register a single tool that can handle any Sceptre command
        self.server.tool(name="run_sceptre", description="Run any Sceptre command")(self.run_sceptre)
        
        # Templates and outputs as resources
        self.server.resource(uri="stack://{stack_path}/template")(self.get_template)
        self.server.resource(uri="stack://{stack_path}/outputs")(self.get_outputs)
    
    async def run_sceptre(self, command: str, args: Optional[List[str]] = None) -> Any:
        """
        Run any Sceptre CLI command.
        
        Args:
            command: The Sceptre command (e.g., "list stacks")
            args: Optional list of additional arguments
        """
        args = args or []
        env = os.environ.copy()
        env["SCEPTRE_PROJECT_PATH"] = self.project_path
        
        # Build command
        full_cmd = ["sceptre"] + command.split() + args
        
        try:
            # Run command
            result = subprocess.run(
                full_cmd,
                env=env,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Try to parse JSON, fall back to text
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return result.stdout.strip()
                
        except subprocess.CalledProcessError as e:
            return {"error": e.stderr.strip() or str(e)}
    
    async def get_template(self, stack_path: str) -> Dict[str, Any]:
        """Get template for a stack."""
        return await self.run_sceptre("dump template", [stack_path, "--output", "json"])
    
    async def get_outputs(self, stack_path: str) -> Dict[str, Any]:
        """Get outputs for a stack."""
        return await self.run_sceptre("list outputs", [stack_path, "--output", "json"])
    
    def run(self, **kwargs):
        """Run the server."""
        self.server.run(**kwargs)
