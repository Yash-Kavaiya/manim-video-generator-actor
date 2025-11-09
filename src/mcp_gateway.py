"""MCP Gateway for exposing Manim Video Generator tools."""

import json
import logging
from typing import Any, Awaitable, Callable

from mcp.server import Server
from mcp.types import Tool

from .const import ACTOR_STYLES, COLOR_SCHEMES, SCENE_TYPES, VIDEO_QUALITIES

logger = logging.getLogger('apify')


async def create_gateway(
    actor_charge_function: Callable[[str, int], Awaitable[Any]] | None = None,
    tool_whitelist: dict[str, tuple[str, int]] | None = None,
) -> Server:
    """Create an MCP gateway server that exposes Manim video generation tools.

    Args:
        actor_charge_function: Optional function to charge for operations
        tool_whitelist: Optional dict mapping tool names to (event_name, default_count) tuples

    Returns:
        Configured MCP Server instance
    """
    server = Server('manim-video-generator')

    # Define tools for Manim video generation
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available Manim video generation tools."""
        return [
            Tool(
                name='generate_video',
                description='Generate an animated educational video using Manim with customizable actors. '
                'Create professional math and science explanations with interactive animated characters.',
                inputSchema={
                    'type': 'object',
                    'properties': {
                        'sceneType': {
                            'type': 'string',
                            'enum': SCENE_TYPES,
                            'description': 'Type of scene to generate',
                        },
                        'videoQuality': {
                            'type': 'string',
                            'enum': list(VIDEO_QUALITIES.keys()),
                            'default': 'medium',
                            'description': 'Video quality setting',
                        },
                        'actorStyle': {
                            'type': 'string',
                            'enum': ACTOR_STYLES,
                            'default': 'cartoon',
                            'description': 'Style of the animated actor',
                        },
                        'actorColorScheme': {
                            'type': 'string',
                            'enum': COLOR_SCHEMES,
                            'default': 'blue',
                            'description': 'Color scheme for the actor',
                        },
                        'outputFileName': {
                            'type': 'string',
                            'default': 'manim_video',
                            'description': 'Name for the output video file',
                        },
                        'outputFormat': {
                            'type': 'string',
                            'enum': ['mp4', 'mov', 'gif'],
                            'default': 'mp4',
                            'description': 'Output video format',
                        },
                        'customSceneConfig': {
                            'type': 'object',
                            'description': 'Custom configuration for CustomScene type',
                            'properties': {
                                'title': {'type': 'string'},
                                'mainText': {'type': 'string'},
                                'equation': {'type': 'string'},
                                'dialogues': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'text': {'type': 'string'},
                                            'isMath': {'type': 'boolean'},
                                            'duration': {'type': 'number'},
                                        },
                                    },
                                },
                                'showCelebration': {'type': 'boolean'},
                            },
                        },
                        'enableSubtitles': {
                            'type': 'boolean',
                            'default': False,
                            'description': 'Generate subtitle file',
                        },
                        'backgroundColor': {
                            'type': 'string',
                            'default': '#000000',
                            'description': 'Background color (hex)',
                        },
                        'fps': {
                            'type': 'integer',
                            'default': 30,
                            'description': 'Frames per second',
                        },
                        'multiActorMode': {
                            'type': 'boolean',
                            'default': False,
                            'description': 'Enable multiple actors in scene',
                        },
                    },
                    'required': ['sceneType'],
                },
            ),
            Tool(
                name='list_scene_types',
                description='Get a list of all available scene types for Manim video generation',
                inputSchema={'type': 'object', 'properties': {}},
            ),
            Tool(
                name='get_actor_styles',
                description='Get available actor styles and color schemes',
                inputSchema={'type': 'object', 'properties': {}},
            ),
            Tool(
                name='validate_scene_config',
                description='Validate a scene configuration before generating video',
                inputSchema={
                    'type': 'object',
                    'properties': {
                        'sceneType': {'type': 'string'},
                        'config': {'type': 'object'},
                    },
                    'required': ['sceneType', 'config'],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[Any]:
        """Handle tool calls for Manim video generation.

        Args:
            name: Name of the tool being called
            arguments: Arguments for the tool

        Returns:
            List of results from the tool execution
        """
        # Check whitelist if provided
        if tool_whitelist and name not in tool_whitelist:
            raise ValueError(f'Tool {name} is not whitelisted')

        # Charge for tool call if charging is enabled
        if actor_charge_function and tool_whitelist and name in tool_whitelist:
            event_name, count = tool_whitelist[name]
            await actor_charge_function(event_name, count)
            logger.info(f'Charged {count} for {event_name}')

        # Handle different tools
        if name == 'list_scene_types':
            return [
                {
                    'type': 'text',
                    'text': json.dumps(
                        {
                            'sceneTypes': SCENE_TYPES,
                            'descriptions': {
                                'ActorIntroduction': 'Simple introduction scene with an animated actor',
                                'SimplePresentation': 'Basic presentation with actor explaining content',
                                'MathLesson': 'Mathematical lesson with equations and explanations',
                                'ActorInteraction': 'Multiple actors interacting with each other',
                                'ProblemSolving': 'Step-by-step problem solving demonstration',
                                'MultiActorScene': 'Complex scene with multiple animated actors',
                                'InteractiveTutorial': 'Interactive tutorial with questions and answers',
                                'CustomScene': 'Fully customizable scene with your own configuration',
                            },
                        },
                        indent=2,
                    ),
                }
            ]

        elif name == 'get_actor_styles':
            return [
                {
                    'type': 'text',
                    'text': json.dumps(
                        {
                            'actorStyles': ACTOR_STYLES,
                            'colorSchemes': COLOR_SCHEMES,
                            'videoQualities': list(VIDEO_QUALITIES.keys()),
                            'outputFormats': ['mp4', 'mov', 'gif'],
                        },
                        indent=2,
                    ),
                }
            ]

        elif name == 'validate_scene_config':
            scene_type = arguments.get('sceneType')
            config = arguments.get('config', {})

            # Basic validation
            validation_result = {'valid': True, 'errors': [], 'warnings': []}

            if scene_type not in SCENE_TYPES:
                validation_result['valid'] = False
                validation_result['errors'].append(f'Invalid scene type: {scene_type}')

            if scene_type == 'CustomScene' and 'customSceneConfig' not in config:
                validation_result['warnings'].append('CustomScene requires customSceneConfig')

            return [{'type': 'text', 'text': json.dumps(validation_result, indent=2)}]

        elif name == 'generate_video':
            # This would trigger the actual Manim video generation
            # For MCP server, we return instructions on how to use the Actor
            result = {
                'status': 'queued',
                'message': 'Video generation has been queued',
                'input': arguments,
                'note': 'This MCP server provides an interface to the Manim Video Generator Actor. '
                'The actual video generation will be processed asynchronously by the Apify Actor.',
            }

            return [{'type': 'text', 'text': json.dumps(result, indent=2)}]

        else:
            raise ValueError(f'Unknown tool: {name}')

    return server
