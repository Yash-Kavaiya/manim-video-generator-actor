"""Configuration constants for the MCP Server Actor."""

# Session timeout in seconds - after this period of inactivity, session will be terminated
SESSION_TIMEOUT_SECS = 300  # 5 minutes

# Tool whitelist for the Manim Video Generator MCP server
# Maps tool names to (event_name, default_count) tuples for charging
# Each tool call will charge the specified event with the given count
TOOL_WHITELIST = {
    'generate_video': ('GENERATE_VIDEO', 1),
    'list_scene_types': ('LIST_SCENES', 1),
    'get_actor_styles': ('GET_STYLES', 1),
    'validate_scene_config': ('VALIDATE_CONFIG', 1),
}

# Available scene types
SCENE_TYPES = [
    'ActorIntroduction',
    'SimplePresentation',
    'MathLesson',
    'ActorInteraction',
    'ProblemSolving',
    'MultiActorScene',
    'InteractiveTutorial',
    'CustomScene'
]

# Available actor styles
ACTOR_STYLES = [
    'cartoon',
    'stick',
    'realistic',
    'minimal'
]

# Available color schemes
COLOR_SCHEMES = [
    'blue',
    'red',
    'green',
    'purple',
    'orange',
    'custom'
]

# Video quality settings
VIDEO_QUALITIES = {
    'low': '-ql',
    'medium': '-qm',
    'high': '-qh',
    'production': '-qk'
}
