"""Main entry point for the MCP Server Actor."""

import os

from apify import Actor

from .const import SESSION_TIMEOUT_SECS, TOOL_WHITELIST
from .models import ServerType
from .server import ProxyServer

# Actor configuration
STANDBY_MODE = os.environ.get('APIFY_META_ORIGIN') == 'STANDBY'
# Bind to all interfaces (0.0.0.0) as this is running in a containerized environment (Apify Actor)
# The container's network is isolated, so this is safe
HOST = '0.0.0.0'  # noqa: S104 - Required for container networking at Apify platform
PORT = (Actor.is_at_home() and int(os.environ.get('ACTOR_STANDBY_PORT') or '5001')) or 5001
SERVER_NAME = 'manim-video-generator'  # Name of the MCP server, without spaces

# CONFIGURATION SECTION ------------------------------------------------------------
# This MCP server exposes Manim video generation tools directly
# It doesn't wrap an external MCP server - it IS the MCP server
# The tools are defined in mcp_gateway.py

server_type = ServerType.STDIO  # Using STDIO type for internal MCP gateway
MCP_SERVER_PARAMS = None  # No external server params needed - we define the tools directly

# ------------------------------------------------------------------------------

session_timeout_secs = int(os.getenv('SESSION_TIMEOUT_SECS', SESSION_TIMEOUT_SECS))


async def main() -> None:
    """Run the MCP Server Actor.

    This function:
    1. Initializes the Actor
    2. Creates and starts the proxy server with Manim tools
    3. Configures charging for MCP operations using Actor.charge

    CHARGING STRATEGY:
    The Manim Video Generator MCP server charges for:
    - generate_video: $0.10 per video generation (GENERATE_VIDEO event)
    - list_scene_types: $0.001 per listing (LIST_SCENES event)
    - get_actor_styles: $0.001 per listing (GET_STYLES event)
    - validate_scene_config: $0.002 per validation (VALIDATE_CONFIG event)

    Charging events are defined in .actor/pay_per_event.json
    """
    async with Actor:
        url = os.environ.get('ACTOR_STANDBY_URL', HOST)
        if not STANDBY_MODE:
            msg = (
                'Actor is not designed to run in the NORMAL mode. Use MCP server URL to connect to the server.\n'
                f'Connect to {url}/mcp to establish a connection.\n'
                'Learn more at https://mcp.apify.com/'
            )
            Actor.log.info(msg)
            await Actor.exit(status_message=msg)
            return

        try:
            # Create and start the server with charging enabled
            Actor.log.info('Starting Manim Video Generator MCP server')
            Actor.log.info('Add the following configuration to your MCP client to use Streamable HTTP transport:')
            Actor.log.info(
                f"""
                {{
                    "mcpServers": {{
                        "{SERVER_NAME}": {{
                            "url": "{url}/mcp",
                            "headers": {{
                                "Authorization": "Bearer YOUR_APIFY_TOKEN"
                            }}
                        }}
                    }}
                }}
                """
            )

            # Note: We're not connecting to an external MCP server
            # Instead, the MCP gateway (mcp_gateway.py) defines the tools directly
            # The ProxyServer will create the MCP server from the gateway
            # For this setup, we don't need actual server params,
            # but the architecture supports both patterns

            # Pass Actor.charge to enable charging for MCP operations
            # The proxy server will use this to charge for different operations
            proxy_server = ProxyServer(
                SERVER_NAME,
                MCP_SERVER_PARAMS,
                HOST,
                PORT,
                server_type,
                actor_charge_function=Actor.charge,
                tool_whitelist=TOOL_WHITELIST,
                session_timeout_secs=session_timeout_secs,
            )
            await proxy_server.start()
        except Exception as e:
            Actor.log.exception(f'Server failed to start: {e}')
            await Actor.exit()
            raise


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
