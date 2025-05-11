# Sceptre MCP Server

## Overview
A server that exposes Sceptre's AWS CloudFormation management capabilities through the Model Context Protocol (MCP). This project integrates Sceptre's opinionated configuration management approach with the FastMCP framework to enable LLMs to interact with CloudFormation stacks.

## Problem Statement
Sceptre provides an excellent opinionated framework for AWS CloudFormation management in Python. This project ports its core functionality to the Model Context Protocol, allowing LLMs to manage AWS infrastructure with the same structured approach.

## Key Features
- Exposes Sceptre's CloudFormation management capabilities as an MCP server
- Maintains Sceptre's opinionated configuration approach
- Provides a clean integration between FastMCP and Sceptre libraries
- Includes comprehensive test coverage

## Development Status
🚧 **Under Construction** 🚧

This project is in active development following the Iterative Engineering Protocol (IEP).

## Architecture
The project integrates two primary components:
1. **Sceptre** - Python-based CloudFormation management framework
2. **FastMCP** - Pythonic implementation of the Model Context Protocol (v2.3.3)

## MCP Interface
The server will expose Sceptre functionality through:
- **Tools** - Actions for stack creation, updates, deletion, and status checks
- **Resources** - Access to templates, config, and stack outputs
- **Prompts** - Templates for common infrastructure operations

## Getting Started
*(Coming soon)*

## Development
This project follows the Iterative Engineering Protocol (IEP), emphasizing:
- Test-first implementation
- Iterative component development
- Comprehensive verification

### Development Environment
*(Coming soon)*

## License
*(TBD)*