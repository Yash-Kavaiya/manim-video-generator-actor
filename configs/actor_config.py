"""
Actor Configuration System
Centralized configuration for actor appearances and behaviors.
"""

from manim import *
from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class ActorConfig:
    """Configuration for actor appearance and behavior."""

    # Visual settings
    style: str = "cartoon"  # cartoon, simple, stick_figure, professional
    scale_factor: float = 1.0

    # Color scheme
    head_color: str = BLUE
    body_color: str = WHITE
    arms_color: str = BLUE
    legs_color: str = BLUE
    accent_color: str = YELLOW

    # Animation settings
    default_animation_speed: float = 1.0
    idle_bounce_enabled: bool = False

    # Position
    default_position: str = "DL"  # DL, DR, UL, UR, LEFT, RIGHT, etc.

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "style": self.style,
            "scale_factor": self.scale_factor,
            "color_scheme": {
                "head": self.head_color,
                "body": self.body_color,
                "arms": self.arms_color,
                "legs": self.legs_color,
                "accent": self.accent_color
            },
            "animation_speed": self.default_animation_speed,
            "idle_bounce": self.idle_bounce_enabled,
            "position": self.default_position
        }


# Predefined actor configurations

TEACHER_CONFIG = ActorConfig(
    style="professional",
    scale_factor=0.9,
    head_color=BLUE_D,
    body_color=BLUE_E,
    arms_color=BLUE_D,
    legs_color=GREY_BROWN,
    accent_color=BLUE_B,
    default_position="DL"
)

STUDENT_CONFIG = ActorConfig(
    style="cartoon",
    scale_factor=0.85,
    head_color=ORANGE,
    body_color=YELLOW_E,
    arms_color=ORANGE,
    legs_color=ORANGE,
    accent_color=YELLOW,
    default_position="DR"
)

PRESENTER_CONFIG = ActorConfig(
    style="simple",
    scale_factor=1.0,
    head_color=TEAL_D,
    body_color=TEAL_E,
    arms_color=TEAL_D,
    legs_color=TEAL_D,
    accent_color=TEAL_A,
    default_position="LEFT"
)

STICK_FIGURE_CONFIG = ActorConfig(
    style="stick_figure",
    scale_factor=1.2,
    head_color=WHITE,
    body_color=WHITE,
    arms_color=WHITE,
    legs_color=WHITE,
    accent_color=YELLOW,
    default_position="DL"
)


# Preset color schemes

COLOR_SCHEMES = {
    "blue": {
        "head": BLUE_D,
        "body": BLUE_E,
        "arms": BLUE_D,
        "legs": BLUE_D,
        "accent": BLUE_B
    },
    "orange": {
        "head": ORANGE,
        "body": YELLOW_E,
        "arms": ORANGE,
        "legs": ORANGE,
        "accent": YELLOW
    },
    "green": {
        "head": GREEN_D,
        "body": GREEN_E,
        "arms": GREEN_D,
        "legs": GREEN_D,
        "accent": GREEN_B
    },
    "purple": {
        "head": PURPLE_D,
        "body": PURPLE_E,
        "arms": PURPLE_D,
        "legs": PURPLE_D,
        "accent": PURPLE_B
    },
    "red": {
        "head": RED_D,
        "body": RED_E,
        "arms": RED_D,
        "legs": RED_D,
        "accent": RED_B
    },
    "grayscale": {
        "head": GREY_A,
        "body": GREY_B,
        "arms": GREY_A,
        "legs": GREY_A,
        "accent": WHITE
    }
}


def create_actor_from_config(config: ActorConfig):
    """
    Create an actor from a configuration.

    Args:
        config: ActorConfig instance

    Returns:
        Configured actor instance
    """
    from actors import BaseActor, ActorStyle

    # Map string to enum
    style_map = {
        "cartoon": ActorStyle.CARTOON,
        "simple": ActorStyle.SIMPLE,
        "stick_figure": ActorStyle.STICK_FIGURE,
        "professional": ActorStyle.PROFESSIONAL
    }

    actor = BaseActor(
        style=style_map.get(config.style, ActorStyle.CARTOON),
        scale_factor=config.scale_factor,
        color_scheme={
            "head": config.head_color,
            "body": config.body_color,
            "arms": config.arms_color,
            "legs": config.legs_color,
            "accent": config.accent_color
        }
    )

    # Position actor
    position_map = {
        "DL": lambda a: a.to_corner(DL),
        "DR": lambda a: a.to_corner(DR),
        "UL": lambda a: a.to_corner(UL),
        "UR": lambda a: a.to_corner(UR),
        "LEFT": lambda a: a.to_edge(LEFT).to_edge(DOWN),
        "RIGHT": lambda a: a.to_edge(RIGHT).to_edge(DOWN),
        "CENTER": lambda a: a.to_edge(DOWN)
    }

    if config.default_position in position_map:
        position_map[config.default_position](actor)

    return actor


def get_preset_config(preset_name: str) -> ActorConfig:
    """
    Get a preset actor configuration.

    Args:
        preset_name: Name of preset (teacher, student, presenter, stick_figure)

    Returns:
        ActorConfig instance
    """
    presets = {
        "teacher": TEACHER_CONFIG,
        "student": STUDENT_CONFIG,
        "presenter": PRESENTER_CONFIG,
        "stick_figure": STICK_FIGURE_CONFIG
    }

    return presets.get(preset_name.lower(), PRESENTER_CONFIG)
