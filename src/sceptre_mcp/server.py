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
        
        # Define and register the tools and resources directly in __init__

        @self.server.tool(name="sceptre_project_path", description="Set sceptre project path")
        async def help(path: Optional[str] = None) -> Any:
            self.project_path = path
            return self.project_path
 
        @self.server.tool(name="sceptre_help", description="Sceptre Help for any command or CLI as a whole")
        async def help(command: Optional[str] = None) -> Any:
            if command:
                return await run_sceptre(command, ["--help"])
            return await run_sceptre("--help")

        @self.server.tool(name="sceptre_launch", description="Launch a stack. DANGER! THere be dragons here, use at your own risk!")
        async def launch(args: Optional[List[str]] = None) -> Any:
            return await run_sceptre("launch", args)
           
        @self.server.tool(name="sceptre", description="Run any Sceptre command except (launch)")
        async def run_sceptre(command: str, args: Optional[List[str]] = None) -> Any:
            """
            Run any Sceptre CLI command.
            
            Args:
                command: The Sceptre command (e.g., "list stacks")
                args: Optional list of additional arguments
            """

            if "launch" in command:
                return "Launch is a dangerous operation that is not generically supported.  Use the explicit launch tool with your own trust policy"

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
        
        # Assign to instance variable to keep reference
        self._run_sceptre = run_sceptre
        
        @self.server.resource(uri="stack://{stack_path}/template")
        async def get_template(stack_path: str) -> Dict[str, Any]:
            """Get template for a stack."""
            args = [stack_path, "--output", "json"]
            return await run_sceptre("dump template", args)
        
        # Assign to instance variable
        self._get_template = get_template
        
        @self.server.resource(uri="stack://{stack_path}/outputs")
        async def get_outputs(stack_path: str) -> Dict[str, Any]:
            """Get outputs for a stack."""
            args = [stack_path, "--output", "json"]
            return await run_sceptre("list outputs", args)
        
        # Assign to instance variable
        self._get_outputs = get_outputs
    
    def run(self, **kwargs):
        """Run the server."""
        self.server.run(**kwargs)
