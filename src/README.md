# Manim Video Generator MCP Server

This directory contains the MCP (Model Context Protocol) server implementation for the Manim Video Generator Actor.

## Overview

The MCP server exposes Manim video generation capabilities as MCP tools that can be called from any MCP-compatible client (VS Code, Claude Desktop, etc.).

## Architecture

```
src/
├── __init__.py           # Package initialization
├── __main__.py           # Entry point for MCP server mode
├── const.py              # Configuration constants
├── models.py             # Data models
├── event_store.py        # Event storage for session management
├── mcp_gateway.py        # MCP tool definitions
└── server.py             # Proxy server implementation
```

## Available Tools

### 1. generate_video
Generate an animated educational video using Manim with customizable actors.

**Parameters:**
- `sceneType` (required): Type of scene to generate
- `videoQuality`: Quality setting (low/medium/high/production)
- `actorStyle`: Style of animated actor (cartoon/stick/realistic/minimal)
- `actorColorScheme`: Color scheme for actor
- `outputFileName`: Name for output video file
- `outputFormat`: Video format (mp4/mov/gif)
- `customSceneConfig`: Custom configuration for CustomScene type
- `enableSubtitles`: Generate subtitle file
- `backgroundColor`: Background color (hex)
- `fps`: Frames per second
- `multiActorMode`: Enable multiple actors

**Cost:** $0.10 per video generation

### 2. list_scene_types
Get a list of all available scene types for Manim video generation.

**Cost:** $0.001 per call

### 3. get_actor_styles
Get available actor styles and color schemes.

**Cost:** $0.001 per call

### 4. validate_scene_config
Validate a scene configuration before generating video.

**Parameters:**
- `sceneType` (required): Scene type to validate
- `config` (required): Configuration object

**Cost:** $0.002 per validation

## Configuration

### Session Timeout
Sessions automatically terminate after 5 minutes of inactivity (configurable via `SESSION_TIMEOUT_SECS` environment variable).

### Tool Whitelist
Only whitelisted tools can be called. The whitelist is defined in `const.py` with associated charging events.

### Charging
The server uses Apify's pay-per-event model. Events are defined in `.actor/pay_per_event.json`.

## Usage

### Running Locally
```bash
APIFY_META_ORIGIN=STANDBY python -m src
```

### Client Configuration
Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "manim-video-generator": {
      "type": "http",
      "url": "https://your-actor-url/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_APIFY_TOKEN"
      }
    }
  }
}
```

### Example Tool Call
```json
{
  "tool": "generate_video",
  "arguments": {
    "sceneType": "MathLesson",
    "videoQuality": "medium",
    "actorStyle": "cartoon",
    "actorColorScheme": "blue",
    "outputFileName": "my_math_lesson"
  }
}
```

## Environment Variables

- `APIFY_META_ORIGIN`: Must be set to "STANDBY" for MCP server mode
- `ACTOR_STANDBY_URL`: URL where the server is accessible
- `ACTOR_STANDBY_PORT`: Port to bind (default: 5001)
- `SESSION_TIMEOUT_SECS`: Session inactivity timeout (default: 300)

## Development

The server supports both:
1. **Native MCP mode**: Tools defined directly in `mcp_gateway.py` (current setup)
2. **Proxy mode**: Can wrap external stdio/SSE/HTTP MCP servers

To add new tools:
1. Add tool definition in `mcp_gateway.py`
2. Add to `TOOL_WHITELIST` in `const.py`
3. Add charging event to `.actor/pay_per_event.json`

## Transport

The server uses **Streamable HTTP** transport, which:
- Supports session resumption
- Handles network interruptions gracefully
- Works with OAuth authentication
- Compatible with Apify platform

## Learn More

- [MCP Documentation](https://mcp.apify.com/)
- [Apify Actors](https://docs.apify.com/platform/actors)
- [Manim Documentation](https://docs.manim.community/)
