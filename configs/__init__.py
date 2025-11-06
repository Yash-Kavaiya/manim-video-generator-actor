"""
Configuration Module
Actor configuration presets and utilities.
"""

from .actor_config import (
    ActorConfig,
    TEACHER_CONFIG,
    STUDENT_CONFIG,
    PRESENTER_CONFIG,
    STICK_FIGURE_CONFIG,
    COLOR_SCHEMES,
    create_actor_from_config,
    get_preset_config
)

__all__ = [
    "ActorConfig",
    "TEACHER_CONFIG",
    "STUDENT_CONFIG",
    "PRESENTER_CONFIG",
    "STICK_FIGURE_CONFIG",
    "COLOR_SCHEMES",
    "create_actor_from_config",
    "get_preset_config"
]
