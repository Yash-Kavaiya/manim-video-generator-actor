"""Data models for the MCP Server Actor."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ServerType(str, Enum):
    """Type of MCP server to connect to."""

    STDIO = 'stdio'
    SSE = 'sse'
    HTTP = 'http'


class RemoteServerParameters(BaseModel):
    """Parameters for connecting to a remote MCP server (SSE or HTTP)."""

    url: str = Field(..., description='URL of the remote MCP server')
    headers: dict[str, str] = Field(default_factory=dict, description='Optional headers for authentication')


# Type alias for server parameters - can be either stdio or remote
ServerParameters = Any  # StdioServerParameters | RemoteServerParameters
