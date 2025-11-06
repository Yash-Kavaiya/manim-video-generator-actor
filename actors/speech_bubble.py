"""
Speech Bubble System
Dynamic speech bubbles for actor dialogue and narration.
"""

from manim import *
from typing import Optional


class SpeechBubble(VGroup):
    """
    A customizable speech bubble that can contain text or math expressions.

    Features:
    - Auto-sizing based on content
    - Pointer arrow to actor
    - Fade in/out animations
    - Support for both Text and MathTex
    """

    def __init__(
        self,
        content: str,
        is_math: bool = False,
        direction: np.ndarray = UP,
        bubble_color: str = WHITE,
        text_color: str = BLACK,
        max_width: float = 5.0,
        **kwargs
    ):
        """
        Initialize speech bubble.

        Args:
            content: Text or LaTeX math to display
            is_math: Whether content is mathematical
            direction: Direction bubble points (UP, DOWN, LEFT, RIGHT)
            bubble_color: Background color of bubble
            text_color: Text color
            max_width: Maximum width of bubble
        """
        super().__init__(**kwargs)

        # Create text content
        if is_math:
            self.text = MathTex(content, color=text_color)
        else:
            self.text = Text(content, color=text_color, font_size=24)

        # Scale if too wide
        if self.text.width > max_width:
            self.text.scale(max_width / self.text.width)

        # Create bubble background with padding
        padding = 0.3
        bubble_width = self.text.width + 2 * padding
        bubble_height = self.text.height + 2 * padding

        self.bubble = RoundedRectangle(
            width=bubble_width,
            height=bubble_height,
            corner_radius=0.2,
            color=bubble_color,
            fill_opacity=0.95,
            stroke_width=2,
            stroke_color=BLACK
        )

        # Create pointer
        pointer_size = 0.3
        if direction[1] > 0:  # UP
            pointer = Polygon(
                self.bubble.get_bottom(),
                self.bubble.get_bottom() + DOWN * pointer_size + LEFT * 0.15,
                self.bubble.get_bottom() + DOWN * pointer_size + RIGHT * 0.15,
                color=bubble_color,
                fill_opacity=0.95,
                stroke_width=2,
                stroke_color=BLACK
            )
        elif direction[1] < 0:  # DOWN
            pointer = Polygon(
                self.bubble.get_top(),
                self.bubble.get_top() + UP * pointer_size + LEFT * 0.15,
                self.bubble.get_top() + UP * pointer_size + RIGHT * 0.15,
                color=bubble_color,
                fill_opacity=0.95,
                stroke_width=2,
                stroke_color=BLACK
            )
        elif direction[0] < 0:  # LEFT
            pointer = Polygon(
                self.bubble.get_right(),
                self.bubble.get_right() + RIGHT * pointer_size + UP * 0.15,
                self.bubble.get_right() + RIGHT * pointer_size + DOWN * 0.15,
                color=bubble_color,
                fill_opacity=0.95,
                stroke_width=2,
                stroke_color=BLACK
            )
        else:  # RIGHT
            pointer = Polygon(
                self.bubble.get_left(),
                self.bubble.get_left() + LEFT * pointer_size + UP * 0.15,
                self.bubble.get_left() + LEFT * pointer_size + DOWN * 0.15,
                color=bubble_color,
                fill_opacity=0.95,
                stroke_width=2,
                stroke_color=BLACK
            )

        self.pointer = pointer

        # Assemble bubble
        self.add(self.bubble, self.pointer, self.text)

        # Center text on bubble
        self.text.move_to(self.bubble.get_center())

    def attach_to(self, actor, buff: float = 0.5):
        """
        Position bubble relative to actor.

        Args:
            actor: The actor mobject to attach to
            buff: Distance from actor
        """
        # Position above actor's head
        self.next_to(actor.head_group, UP, buff=buff)
        return self

    def grow_animation(self, run_time: float = 0.5) -> Animation:
        """Create a growing animation for the bubble."""
        return Succession(
            GrowFromCenter(self.bubble, run_time=run_time * 0.4),
            GrowFromCenter(self.pointer, run_time=run_time * 0.3),
            FadeIn(self.text, run_time=run_time * 0.3)
        )

    def shrink_animation(self, run_time: float = 0.3) -> Animation:
        """Create a shrinking animation for the bubble."""
        return Succession(
            FadeOut(self.text, run_time=run_time * 0.3),
            ShrinkToCenter(self.pointer, run_time=run_time * 0.3),
            ShrinkToCenter(self.bubble, run_time=run_time * 0.4)
        )

    def pulse_animation(self, scale_factor: float = 1.1, run_time: float = 0.5) -> Animation:
        """Create a pulsing animation for emphasis."""
        return Succession(
            self.animate.scale(scale_factor).set_run_time(run_time / 2),
            self.animate.scale(1 / scale_factor).set_run_time(run_time / 2)
        )


class ThoughtBubble(VGroup):
    """
    A thought bubble variant with circular bubbles instead of pointer.
    """

    def __init__(
        self,
        content: str,
        is_math: bool = False,
        bubble_color: str = WHITE,
        text_color: str = BLACK,
        max_width: float = 5.0,
        **kwargs
    ):
        """Initialize thought bubble."""
        super().__init__(**kwargs)

        # Create text content
        if is_math:
            self.text = MathTex(content, color=text_color)
        else:
            self.text = Text(content, color=text_color, font_size=24)

        # Scale if too wide
        if self.text.width > max_width:
            self.text.scale(max_width / self.text.width)

        # Create cloud-like bubble
        padding = 0.3
        bubble_width = self.text.width + 2 * padding
        bubble_height = self.text.height + 2 * padding

        # Main bubble
        self.bubble = Ellipse(
            width=bubble_width,
            height=bubble_height,
            color=bubble_color,
            fill_opacity=0.95,
            stroke_width=2,
            stroke_color=BLACK
        )

        # Thought bubble circles
        circle1 = Circle(radius=0.15, color=bubble_color, fill_opacity=0.95, stroke_width=2, stroke_color=BLACK)
        circle2 = Circle(radius=0.1, color=bubble_color, fill_opacity=0.95, stroke_width=2, stroke_color=BLACK)
        circle3 = Circle(radius=0.05, color=bubble_color, fill_opacity=0.95, stroke_width=2, stroke_color=BLACK)

        self.circles = VGroup(circle1, circle2, circle3)

        # Position circles
        circle1.next_to(self.bubble, DOWN + LEFT, buff=0.1)
        circle2.next_to(circle1, DOWN + LEFT, buff=0.05)
        circle3.next_to(circle2, DOWN + LEFT, buff=0.03)

        # Assemble
        self.add(self.bubble, self.circles, self.text)
        self.text.move_to(self.bubble.get_center())

    def attach_to(self, actor, buff: float = 0.5):
        """Position thought bubble relative to actor."""
        self.next_to(actor.head_group, UP + RIGHT, buff=buff)
        return self

    def grow_animation(self, run_time: float = 0.7) -> Animation:
        """Create a growing animation."""
        return Succession(
            AnimationGroup(
                FadeIn(self.circles[2], run_time=run_time * 0.2),
                FadeIn(self.circles[1], run_time=run_time * 0.3),
                FadeIn(self.circles[0], run_time=run_time * 0.4),
            ),
            GrowFromCenter(self.bubble, run_time=run_time * 0.5),
            FadeIn(self.text, run_time=run_time * 0.2)
        )

    def shrink_animation(self, run_time: float = 0.5) -> Animation:
        """Create a shrinking animation."""
        return Succession(
            FadeOut(self.text, run_time=run_time * 0.2),
            ShrinkToCenter(self.bubble, run_time=run_time * 0.3),
            FadeOut(self.circles, run_time=run_time * 0.5)
        )
