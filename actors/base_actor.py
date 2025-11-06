"""
Base Actor Class
Defines the core actor with modular anatomy and animation capabilities.
"""

from manim import *
from enum import Enum
from typing import Dict, Optional, Tuple


class ActorStyle(Enum):
    """Actor visual styles."""
    CARTOON = "cartoon"
    SIMPLE = "simple"
    STICK_FIGURE = "stick_figure"
    PROFESSIONAL = "professional"


class BaseActor(VGroup):
    """
    A modular actor for Manim animations with customizable appearance,
    gestures, and interactions.

    Features:
    - Modular anatomy (head, body, arms, legs)
    - Multiple visual styles
    - Gesture system for pointing, waving, nodding
    - Expression changes
    - Interactive behaviors with scene elements
    """

    def __init__(
        self,
        style: ActorStyle = ActorStyle.CARTOON,
        color_scheme: Dict[str, str] = None,
        scale_factor: float = 1.0,
        **kwargs
    ):
        """
        Initialize the actor.

        Args:
            style: Visual style of the actor
            color_scheme: Dictionary of colors for different parts
            scale_factor: Overall size multiplier
        """
        super().__init__(**kwargs)

        self.style = style
        self.scale_factor = scale_factor
        self.color_scheme = color_scheme or self._default_color_scheme()
        self.current_expression = "neutral"

        # Create anatomy
        self._create_anatomy()
        self.scale(scale_factor)

        # Store references to body parts for animations
        self.head_group = self[0]
        self.body_part = self[1]
        self.left_arm = self[2]
        self.right_arm = self[3]
        self.left_leg = self[4]
        self.right_leg = self[5]

    def _default_color_scheme(self) -> Dict[str, str]:
        """Return default color scheme."""
        return {
            "head": BLUE,
            "body": WHITE,
            "arms": BLUE,
            "legs": BLUE,
            "accent": YELLOW
        }

    def _create_anatomy(self):
        """Create the actor's body parts based on style."""
        if self.style == ActorStyle.STICK_FIGURE:
            self._create_stick_figure()
        elif self.style == ActorStyle.SIMPLE:
            self._create_simple_actor()
        elif self.style == ActorStyle.CARTOON:
            self._create_cartoon_actor()
        elif self.style == ActorStyle.PROFESSIONAL:
            self._create_professional_actor()

    def _create_stick_figure(self):
        """Create a simple stick figure actor."""
        # Head
        head = Circle(radius=0.3, color=self.color_scheme["head"], fill_opacity=1)

        # Eyes
        left_eye = Dot(point=head.get_center() + LEFT * 0.1 + UP * 0.05, radius=0.03)
        right_eye = Dot(point=head.get_center() + RIGHT * 0.1 + UP * 0.05, radius=0.03)

        # Mouth (simple arc)
        mouth = Arc(
            radius=0.15,
            start_angle=-PI/3,
            angle=2*PI/3,
            color=BLACK
        ).move_to(head.get_center() + DOWN * 0.1)

        head_group = VGroup(head, left_eye, right_eye, mouth)

        # Body
        body = Line(
            head.get_bottom(),
            head.get_bottom() + DOWN * 1.2,
            color=self.color_scheme["body"],
            stroke_width=6
        )

        # Arms
        arm_start = body.get_top() + DOWN * 0.2
        left_arm = Line(
            arm_start,
            arm_start + LEFT * 0.5 + DOWN * 0.4,
            color=self.color_scheme["arms"],
            stroke_width=5
        )
        right_arm = Line(
            arm_start,
            arm_start + RIGHT * 0.5 + DOWN * 0.4,
            color=self.color_scheme["arms"],
            stroke_width=5
        )

        # Legs
        leg_start = body.get_bottom()
        left_leg = Line(
            leg_start,
            leg_start + LEFT * 0.3 + DOWN * 0.8,
            color=self.color_scheme["legs"],
            stroke_width=5
        )
        right_leg = Line(
            leg_start,
            leg_start + RIGHT * 0.3 + DOWN * 0.8,
            color=self.color_scheme["legs"],
            stroke_width=5
        )

        self.add(head_group, body, left_arm, right_arm, left_leg, right_leg)

    def _create_simple_actor(self):
        """Create a simple geometric actor."""
        # Head
        head = Circle(radius=0.4, color=self.color_scheme["head"], fill_opacity=0.8)

        # Eyes
        left_eye = Dot(point=head.get_center() + LEFT * 0.15 + UP * 0.08, radius=0.05, color=BLACK)
        right_eye = Dot(point=head.get_center() + RIGHT * 0.15 + UP * 0.08, radius=0.05, color=BLACK)

        # Smile
        smile = Arc(
            radius=0.2,
            start_angle=-PI/3,
            angle=2*PI/3,
            color=BLACK,
            stroke_width=3
        ).move_to(head.get_center() + DOWN * 0.1)

        head_group = VGroup(head, left_eye, right_eye, smile)

        # Body (rounded rectangle)
        body = RoundedRectangle(
            width=0.8,
            height=1.2,
            corner_radius=0.2,
            color=self.color_scheme["body"],
            fill_opacity=0.8
        ).next_to(head, DOWN, buff=0.1)

        # Arms (rounded rectangles)
        left_arm = RoundedRectangle(
            width=0.2,
            height=0.7,
            corner_radius=0.1,
            color=self.color_scheme["arms"],
            fill_opacity=0.8
        ).next_to(body, LEFT, buff=0.05).shift(DOWN * 0.2)

        right_arm = RoundedRectangle(
            width=0.2,
            height=0.7,
            corner_radius=0.1,
            color=self.color_scheme["arms"],
            fill_opacity=0.8
        ).next_to(body, RIGHT, buff=0.05).shift(DOWN * 0.2)

        # Legs (rounded rectangles)
        left_leg = RoundedRectangle(
            width=0.25,
            height=0.8,
            corner_radius=0.1,
            color=self.color_scheme["legs"],
            fill_opacity=0.8
        ).next_to(body, DOWN, buff=0.05).shift(LEFT * 0.15)

        right_leg = RoundedRectangle(
            width=0.25,
            height=0.8,
            corner_radius=0.1,
            color=self.color_scheme["legs"],
            fill_opacity=0.8
        ).next_to(body, DOWN, buff=0.05).shift(RIGHT * 0.15)

        self.add(head_group, body, left_arm, right_arm, left_leg, right_leg)

    def _create_cartoon_actor(self):
        """Create a cartoon-style actor with more personality."""
        # Larger head for cartoon proportions
        head = Circle(radius=0.5, color=self.color_scheme["head"], fill_opacity=1, stroke_width=2)

        # Cartoon eyes (larger)
        left_eye_white = Circle(radius=0.12, color=WHITE, fill_opacity=1).move_to(
            head.get_center() + LEFT * 0.18 + UP * 0.1
        )
        left_pupil = Circle(radius=0.06, color=BLACK, fill_opacity=1).move_to(
            left_eye_white.get_center()
        )

        right_eye_white = Circle(radius=0.12, color=WHITE, fill_opacity=1).move_to(
            head.get_center() + RIGHT * 0.18 + UP * 0.1
        )
        right_pupil = Circle(radius=0.06, color=BLACK, fill_opacity=1).move_to(
            right_eye_white.get_center()
        )

        # Cartoon smile
        smile = Arc(
            radius=0.25,
            start_angle=-PI/3,
            angle=2*PI/3,
            color=BLACK,
            stroke_width=4
        ).move_to(head.get_center() + DOWN * 0.15)

        head_group = VGroup(head, left_eye_white, left_pupil, right_eye_white, right_pupil, smile)

        # Smaller body for cartoon proportions
        body = RoundedRectangle(
            width=0.7,
            height=1.0,
            corner_radius=0.3,
            color=self.color_scheme["body"],
            fill_opacity=1,
            stroke_width=2
        ).next_to(head, DOWN, buff=0.1)

        # Arms with hands
        left_arm = RoundedRectangle(
            width=0.15,
            height=0.6,
            corner_radius=0.075,
            color=self.color_scheme["arms"],
            fill_opacity=1
        ).next_to(body, LEFT, buff=0.05).shift(DOWN * 0.1)

        right_arm = RoundedRectangle(
            width=0.15,
            height=0.6,
            corner_radius=0.075,
            color=self.color_scheme["arms"],
            fill_opacity=1
        ).next_to(body, RIGHT, buff=0.05).shift(DOWN * 0.1)

        # Legs with feet
        left_leg = RoundedRectangle(
            width=0.2,
            height=0.7,
            corner_radius=0.1,
            color=self.color_scheme["legs"],
            fill_opacity=1
        ).next_to(body, DOWN, buff=0.05).shift(LEFT * 0.12)

        right_leg = RoundedRectangle(
            width=0.2,
            height=0.7,
            corner_radius=0.1,
            color=self.color_scheme["legs"],
            fill_opacity=1
        ).next_to(body, DOWN, buff=0.05).shift(RIGHT * 0.12)

        self.add(head_group, body, left_arm, right_arm, left_leg, right_leg)

    def _create_professional_actor(self):
        """Create a more professional/realistic silhouette-style actor."""
        # Head with hair
        head = Circle(radius=0.35, color=self.color_scheme["head"], fill_opacity=1)
        hair = Ellipse(
            width=0.8,
            height=0.4,
            color=self.color_scheme["accent"],
            fill_opacity=1
        ).move_to(head.get_top() + UP * 0.1)

        # Professional features
        left_eye = Ellipse(
            width=0.08,
            height=0.04,
            color=BLACK,
            fill_opacity=1
        ).move_to(head.get_center() + LEFT * 0.12 + UP * 0.05)

        right_eye = Ellipse(
            width=0.08,
            height=0.04,
            color=BLACK,
            fill_opacity=1
        ).move_to(head.get_center() + RIGHT * 0.12 + UP * 0.05)

        # Subtle smile
        smile = Arc(
            radius=0.15,
            start_angle=-PI/4,
            angle=PI/2,
            color=BLACK,
            stroke_width=2
        ).move_to(head.get_center() + DOWN * 0.12)

        head_group = VGroup(head, hair, left_eye, right_eye, smile)

        # Professional attire (suit-like)
        body = RoundedRectangle(
            width=0.9,
            height=1.3,
            corner_radius=0.15,
            color=self.color_scheme["body"],
            fill_opacity=1
        ).next_to(head, DOWN, buff=0.05)

        # Suit jacket detail
        jacket_line = Line(
            body.get_top(),
            body.get_bottom(),
            color=self.color_scheme["accent"],
            stroke_width=3
        )

        body = VGroup(body, jacket_line)

        # Arms in professional pose
        left_arm = RoundedRectangle(
            width=0.18,
            height=0.8,
            corner_radius=0.09,
            color=self.color_scheme["arms"],
            fill_opacity=1
        ).next_to(body, LEFT, buff=0.02).shift(DOWN * 0.2)

        right_arm = RoundedRectangle(
            width=0.18,
            height=0.8,
            corner_radius=0.09,
            color=self.color_scheme["arms"],
            fill_opacity=1
        ).next_to(body, RIGHT, buff=0.02).shift(DOWN * 0.2)

        # Professional legs
        left_leg = RoundedRectangle(
            width=0.25,
            height=0.9,
            corner_radius=0.1,
            color=self.color_scheme["legs"],
            fill_opacity=1
        ).next_to(body, DOWN, buff=0.02).shift(LEFT * 0.15)

        right_leg = RoundedRectangle(
            width=0.25,
            height=0.9,
            corner_radius=0.1,
            color=self.color_scheme["legs"],
            fill_opacity=1
        ).next_to(body, DOWN, buff=0.02).shift(RIGHT * 0.15)

        self.add(head_group, body, left_arm, right_arm, left_leg, right_leg)

    # Animation Methods

    def wave(self) -> Animation:
        """Create a waving animation."""
        original_angle = self.right_arm.get_angle()
        return Succession(
            Rotate(self.right_arm, angle=PI/4, about_point=self.right_arm.get_top()),
            Rotate(self.right_arm, angle=-PI/6, about_point=self.right_arm.get_top()),
            Rotate(self.right_arm, angle=PI/6, about_point=self.right_arm.get_top()),
            Rotate(self.right_arm, angle=-PI/4, about_point=self.right_arm.get_top()),
        )

    def point_to(self, target: Mobject, run_time: float = 1.0) -> Animation:
        """
        Point to a target mobject.

        Args:
            target: The mobject to point at
            run_time: Animation duration
        """
        # Calculate angle to target
        actor_pos = self.right_arm.get_center()
        target_pos = target.get_center()

        # Store original arm
        original_arm = self.right_arm.copy()

        # Create pointing arm
        pointing_arm = Line(
            self.right_arm.get_top(),
            target_pos,
            color=self.right_arm.get_color(),
            stroke_width=self.right_arm.get_stroke_width()
        )

        return Succession(
            Transform(self.right_arm, pointing_arm, run_time=run_time/2),
            Wait(run_time/2),
        )

    def nod(self, times: int = 2) -> Animation:
        """
        Create a nodding animation.

        Args:
            times: Number of nods
        """
        nod_sequence = []
        for _ in range(times):
            nod_sequence.extend([
                self.head_group.animate.shift(DOWN * 0.1),
                self.head_group.animate.shift(UP * 0.1),
            ])
        return Succession(*nod_sequence)

    def shake_head(self, times: int = 2) -> Animation:
        """
        Create a head-shaking animation.

        Args:
            times: Number of shakes
        """
        shake_sequence = []
        for _ in range(times):
            shake_sequence.extend([
                self.head_group.animate.shift(LEFT * 0.1),
                self.head_group.animate.shift(RIGHT * 0.2),
                self.head_group.animate.shift(LEFT * 0.1),
            ])
        return Succession(*shake_sequence)

    def change_expression(self, expression: str) -> Animation:
        """
        Change the actor's facial expression.

        Args:
            expression: "happy", "sad", "surprised", "neutral", "confused"
        """
        self.current_expression = expression

        # Get the mouth (last element in head_group)
        old_mouth = self.head_group[-1]

        # Create new mouth based on expression
        if expression == "happy":
            new_mouth = Arc(
                radius=0.2,
                start_angle=-PI/3,
                angle=2*PI/3,
                color=BLACK,
                stroke_width=3
            ).move_to(old_mouth.get_center())
        elif expression == "sad":
            new_mouth = Arc(
                radius=0.2,
                start_angle=PI + PI/3,
                angle=2*PI/3,
                color=BLACK,
                stroke_width=3
            ).move_to(old_mouth.get_center())
        elif expression == "surprised":
            new_mouth = Circle(
                radius=0.1,
                color=BLACK,
                fill_opacity=1
            ).move_to(old_mouth.get_center())
        elif expression == "confused":
            new_mouth = Line(
                LEFT * 0.15,
                RIGHT * 0.15,
                color=BLACK,
                stroke_width=3
            ).move_to(old_mouth.get_center())
        else:  # neutral
            new_mouth = Line(
                LEFT * 0.15,
                RIGHT * 0.15,
                color=BLACK,
                stroke_width=2
            ).move_to(old_mouth.get_center())

        return Transform(old_mouth, new_mouth)

    def idle_bounce(self) -> Animation:
        """Create a subtle idle bouncing animation."""
        return Succession(
            self.animate.shift(UP * 0.05).set_run_time(0.5),
            self.animate.shift(DOWN * 0.05).set_run_time(0.5),
        )

    def walk_to(self, position: np.ndarray, run_time: float = 2.0) -> Animation:
        """
        Walk to a position with leg animation.

        Args:
            position: Target position
            run_time: Animation duration
        """
        # Simple walk animation with leg movement
        walk_cycle = AnimationGroup(
            self.animate.move_to(position).set_run_time(run_time),
            Succession(
                Rotate(self.left_leg, angle=PI/6, about_point=self.left_leg.get_top(), run_time=run_time/4),
                Rotate(self.left_leg, angle=-PI/6, about_point=self.left_leg.get_top(), run_time=run_time/4),
                Rotate(self.left_leg, angle=PI/6, about_point=self.left_leg.get_top(), run_time=run_time/4),
                Rotate(self.left_leg, angle=-PI/6, about_point=self.left_leg.get_top(), run_time=run_time/4),
            ),
        )
        return walk_cycle

    def think(self) -> Animation:
        """Create a thinking animation (hand to chin)."""
        return Succession(
            self.right_arm.animate.shift(UP * 0.3 + LEFT * 0.2),
            Wait(1),
            self.right_arm.animate.shift(DOWN * 0.3 + RIGHT * 0.2),
        )

    def celebrate(self) -> Animation:
        """Create a celebration animation (arms up)."""
        return AnimationGroup(
            Rotate(self.left_arm, angle=PI/3, about_point=self.left_arm.get_bottom()),
            Rotate(self.right_arm, angle=-PI/3, about_point=self.right_arm.get_bottom()),
            self.animate.scale(1.1),
        )
