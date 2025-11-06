"""
Manim Actor System
A modular actor system for creating animated characters in Manim videos.
"""

from .base_actor import BaseActor, ActorStyle
from .speech_bubble import SpeechBubble
from .gestures import GestureLibrary

__all__ = ["BaseActor", "ActorStyle", "SpeechBubble", "GestureLibrary"]
