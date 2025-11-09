# MCP Server Setup Complete ✅

## Summary

The Manim Video Generator Actor has been successfully enhanced with a complete MCP (Model Context Protocol) server implementation. The actor now supports **two modes of operation**:

1. **Regular Actor Mode** - Direct video generation via Apify platform
2. **MCP Server Mode** - Expose video generation tools via MCP protocol

## What Was Implemented

### 1. Core MCP Server Infrastructure (`src/`)

#### `src/__main__.py` - Entry Point
- Main entry point for MCP server mode
- Initializes Apify Actor in STANDBY mode
- Configures proxy server with charging enabled
- Provides client configuration examples

#### `src/server.py` - Proxy Server (432 lines)
- Starlette/Uvicorn-based HTTP server
- Streamable HTTP transport support
- Session management with inactivity timeout (5 min default)
- OAuth authorization server integration
- Browser-friendly HTML interface
- Middleware for path rewriting

#### `src/mcp_gateway.py` - Tool Definitions (238 lines)
- Defines 4 MCP tools:
  - `generate_video` - Full video generation with customization
  - `list_scene_types` - List available scene types
  - `get_actor_styles` - Get actor styles and color schemes
  - `validate_scene_config` - Validate configuration before generation
- Tool charging integration
- Tool whitelist enforcement

#### `src/event_store.py` - Event Storage
- In-memory event store for session persistence
- Supports connection resumption
- Event cleanup on session deletion

#### `src/models.py` - Data Models
- ServerType enum (STDIO/SSE/HTTP)
- RemoteServerParameters model
- Type definitions for server configuration

#### `src/const.py` - Configuration
- Session timeout configuration
- Tool whitelist with charging mappings
- Scene types, actor styles, color schemes
- Video quality settings

### 2. Charging Configuration

#### `.actor/pay_per_event.json`
Defines pricing for MCP operations:
- `GENERATE_VIDEO`: $0.10 per video
- `LIST_SCENES`: $0.001 per call
- `GET_STYLES`: $0.001 per call
- `VALIDATE_CONFIG`: $0.002 per call

### 3. Updated Infrastructure

#### `Dockerfile`
- Added conditional CMD to support both modes
- Checks `APIFY_META_ORIGIN` environment variable
- Routes to `python -m src` for STANDBY mode
- Routes to `main.py` for regular actor mode

#### `requirements.txt`
Added MCP dependencies:
- `mcp>=1.0.0` - MCP protocol implementation
- `uvicorn>=0.27.0` - ASGI server
- `starlette>=0.36.0` - Web framework
- `httpx>=0.26.0` - Async HTTP client
- `pydantic>=2.0.0` - Data validation

### 4. Documentation

#### `src/README.md` (140 lines)
Comprehensive documentation covering:
- Architecture overview
- Available tools and parameters
- Cost structure
- Configuration options
- Usage examples
- Client setup instructions
- Development guidelines

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│         MCP Client (VS Code, Claude, etc.)      │
└────────────────────┬────────────────────────────┘
                     │ Streamable HTTP
                     │ + OAuth Token
                     ↓
┌─────────────────────────────────────────────────┐
│              Apify Actor (STANDBY)              │
│  ┌───────────────────────────────────────────┐  │
│  │        src/server.py (Starlette)          │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │  StreamableHTTPSessionManager       │  │  │
│  │  │  - Session tracking                 │  │  │
│  │  │  - Event store                      │  │  │
│  │  │  - Timeout handling                 │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────────────────┬───────────────────────┘  │
│                      │                          │
│  ┌───────────────────▼───────────────────────┐  │
│  │     src/mcp_gateway.py (MCP Server)       │  │
│  │  - Tool definitions                       │  │
│  │  - Request handling                       │  │
│  │  - Charging integration                   │  │
│  └───────────────────┬───────────────────────┘  │
│                      │                          │
│  ┌───────────────────▼───────────────────────┐  │
│  │      Apify Actor.charge()                 │  │
│  │      (Pay-per-event billing)              │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## How It Works

### Mode Selection
The Docker container automatically selects the appropriate mode:
- **STANDBY mode**: When `APIFY_META_ORIGIN=STANDBY` → Runs MCP server
- **Normal mode**: Otherwise → Runs regular Apify Actor

### MCP Server Flow
1. Client connects to `https://actor-url/mcp`
2. Server creates a session with unique ID
3. Client sends tool call requests
4. Server validates against whitelist
5. Server charges via `Actor.charge()`
6. Tool handler executes and returns results
7. Session expires after 5 minutes of inactivity

### Session Management
- Each client connection gets a unique session ID
- Sessions track last activity timestamp
- Automatic cleanup after timeout
- Support for connection resumption via event store

## Usage

### Client Configuration

Add to your MCP client configuration file:

```json
{
  "mcpServers": {
    "manim-video-generator": {
      "type": "http",
      "url": "https://your-actor-standby-url/mcp",
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
    "videoQuality": "high",
    "actorStyle": "cartoon",
    "actorColorScheme": "blue",
    "outputFileName": "pythagorean_theorem",
    "customSceneConfig": {
      "title": "Pythagorean Theorem",
      "equation": "a^2 + b^2 = c^2",
      "showCelebration": true
    }
  }
}
```

### Environment Variables

Configure the server with these environment variables:
- `APIFY_META_ORIGIN` - Set to "STANDBY" for MCP mode
- `ACTOR_STANDBY_URL` - Public URL of the actor
- `ACTOR_STANDBY_PORT` - Port to bind (default: 5001)
- `SESSION_TIMEOUT_SECS` - Inactivity timeout (default: 300)

## Testing Locally

Run the MCP server locally:

```bash
# Set environment variables
export APIFY_META_ORIGIN=STANDBY
export ACTOR_STANDBY_URL=http://localhost:5001
export ACTOR_STANDBY_PORT=5001

# Run the server
python -m src
```

## Deployment

The actor is ready to deploy to Apify platform:
1. All code is committed to branch `claude/complete-mcp-server-actor-011CUxTj6t549EfLRvkcuHBR`
2. Docker configuration supports both modes
3. Pay-per-event configuration is in place
4. OAuth integration is configured

## Key Features

✅ **Streamable HTTP Transport** - Reliable, resumable connections
✅ **Session Management** - Automatic timeout and cleanup
✅ **Pay-per-Event Billing** - Integrated charging for each tool
✅ **Tool Whitelist** - Security and cost control
✅ **OAuth Support** - Apify platform authentication
✅ **Browser Interface** - HTML page for easy testing
✅ **Dual Mode** - Regular actor OR MCP server
✅ **Type Safety** - Pydantic models throughout
✅ **Comprehensive Docs** - In-code and standalone documentation

## Files Changed

```
 .actor/pay_per_event.json |  24 +++
 Dockerfile                |  10 +-
 requirements.txt          |   7 +
 src/README.md             | 140 +++++++++++++++
 src/__init__.py           |   3 +
 src/__main__.py           | 107 ++++++++++++
 src/const.py              |  52 ++++++
 src/event_store.py        |  49 ++++++
 src/mcp_gateway.py        | 238 +++++++++++++++++++++++++
 src/models.py             |  25 +++
 src/server.py             | 432 ++++++++++++++++++++++++++++++++++++++++++++++
 11 files changed, 1085 insertions(+), 2 deletions(-)
```

## Next Steps

1. **Test the MCP Server**: Deploy to Apify and test with an MCP client
2. **Adjust Pricing**: Review and adjust pay-per-event prices as needed
3. **Add More Tools**: Extend with additional video generation capabilities
4. **Monitor Usage**: Track tool usage and charging metrics
5. **Documentation**: Update main README.md with MCP server information

## Resources

- [MCP Documentation](https://mcp.apify.com/)
- [Apify Actors](https://docs.apify.com/platform/actors)
- [Streamable HTTP Transport](https://spec.modelcontextprotocol.io/specification/basic/transports/#http-with-sse)
- [Pay-per-Event Billing](https://docs.apify.com/platform/actors/development/actor-definition/actor-json#pay-per-event)

---

**Status**: ✅ Complete and ready for deployment
**Branch**: `claude/complete-mcp-server-actor-011CUxTj6t549EfLRvkcuHBR`
**Commit**: Pushed successfully to remote
