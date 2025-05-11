"""
Unit tests for the Sceptre MCP Server.
"""
import pytest
from unittest.mock import patch, MagicMock, call
import subprocess
import json

from sceptre_mcp.server import SceptreMCPServer


class TestSceptreMCPServer:
    """Tests for the Sceptre MCP Server."""
    
    @pytest.fixture
    def server(self):
        """Create a server instance for testing."""
        # Mock subprocess.run within the server initialization
        with patch('subprocess.run') as mock_run:
            mock_process = MagicMock()
            mock_process.stdout = '{"test": "result"}'
            mock_run.return_value = mock_process
            
            server = SceptreMCPServer(project_path="/fake/project/path")
            return server
    
    @pytest.mark.asyncio
    async def test_run_sceptre(self, server):
        """Test that the _run_sceptre function calls the sceptre CLI properly."""
        # Mock subprocess.run for this specific test
        mock_process = MagicMock()
        mock_process.stdout = '{"test": "result"}'
        
        with patch('subprocess.run', return_value=mock_process) as mock_run:
            result = await server._run_sceptre("list stacks", ["--output", "json"])
            
            # Check the command was built and executed correctly
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            
            # Check command contains correct parts
            assert args[0] == ["sceptre", "list", "stacks", "--output", "json"]
            
            # Check environment variables were set
            assert kwargs['env']["SCEPTRE_PROJECT_PATH"] == "/fake/project/path"
            
            # Check subprocess settings
            assert kwargs['check'] is True
            assert kwargs['capture_output'] is True
            assert kwargs['text'] is True
            
            # Check result parsing
            assert result == {"test": "result"}
    
    @pytest.mark.asyncio
    async def test_get_template(self, server):
        """Test that get_template calls run_sceptre with correct args."""
        with patch.object(server, '_run_sceptre') as mock_run_sceptre:
            mock_run_sceptre.return_value = {"Resources": {}}
            await server._get_template("dev/network/vpc.yaml")
            mock_run_sceptre.assert_called_once_with(
                "dump template", 
                ["dev/network/vpc.yaml", "--output", "json"]
            )
    
    @pytest.mark.asyncio
    async def test_get_outputs(self, server):
        """Test that get_outputs calls run_sceptre with correct args."""
        with patch.object(server, '_run_sceptre') as mock_run_sceptre:
            mock_run_sceptre.return_value = {"Outputs": {}}
            await server._get_outputs("dev/network/vpc.yaml")
            mock_run_sceptre.assert_called_once_with(
                "list outputs", 
                ["dev/network/vpc.yaml", "--output", "json"]
            )
    
    @pytest.mark.asyncio
    async def test_cli_execution_error(self, server):
        """Test handling of CLI execution errors."""
        # Mock subprocess.run to raise CalledProcessError
        error = subprocess.CalledProcessError(1, ["sceptre"], stderr="Error message")
        
        with patch('subprocess.run', side_effect=error) as mock_run:
            result = await server._run_sceptre("invalid command")
            
            # Check error was properly caught and formatted
            assert "error" in result
            assert "Error message" in result["error"]
    
    @pytest.mark.asyncio
    async def test_json_parse_error(self, server):
        """Test handling of JSON parse errors."""
        # Mock subprocess.run to return invalid JSON
        mock_process = MagicMock()
        mock_process.stdout = 'Not valid JSON'
        
        with patch('subprocess.run', return_value=mock_process) as mock_run:
            result = await server._run_sceptre("list stacks", ["--output", "json"])
            
            # Check result is raw output when JSON parsing fails
            assert result == "Not valid JSON"
