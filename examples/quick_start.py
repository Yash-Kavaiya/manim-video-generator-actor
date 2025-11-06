"""
Quick Start Example
A minimal example to get started with Manim actors.

Run with: manim -pql examples/quick_start.py QuickStart
"""

from manim import *
import sys
sys.path.append('..')
from actors import BaseActor, ActorStyle, SpeechBubble


class QuickStart(Scene):
    """
    Minimal example showing basic actor usage.
    """

    def construct(self):
        # Create an actor
        actor = BaseActor(style=ActorStyle.CARTOON)
        actor.to_edge(LEFT).to_edge(DOWN)

        # Add actor to scene
        self.play(FadeIn(actor))

        # Make actor wave
        self.play(actor.wave())

        # Add speech bubble
        bubble = SpeechBubble("Hello, Manim!", is_math=False)
        bubble.attach_to(actor)

        self.play(bubble.grow_animation())
        self.wait(2)

        # Cleanup
        self.play(
            bubble.shrink_animation(),
            FadeOut(actor)
        )


class CustomActor(Scene):
    """
    Example with custom colors and style.
    """

    def construct(self):
        # Create actor with custom colors
        my_actor = BaseActor(
            style=ActorStyle.SIMPLE,
            scale_factor=1.2,
            color_scheme={
                "head": PURPLE_D,
                "body": PURPLE_E,
                "arms": PURPLE_D,
                "legs": PURPLE_D,
                "accent": PURPLE_A
            }
        )
        my_actor.to_corner(DR)

        self.play(FadeIn(my_actor, shift=UP))
        self.play(my_actor.celebrate())
        self.wait(2)


class SimpleEquation(Scene):
    """
    Actor explains a simple equation.
    """

    def construct(self):
        # Create teacher
        teacher = BaseActor(style=ActorStyle.PROFESSIONAL, scale_factor=0.9)
        teacher.to_corner(DL)

        # Show equation
        equation = MathTex(r"E = mc^2", font_size=60)

        self.play(FadeIn(teacher))
        self.play(Write(equation))

        # Point to equation
        self.play(teacher.point_to(equation))

        # Explain
        explanation = SpeechBubble(
            "Einstein's famous equation!",
            is_math=False
        ).attach_to(teacher)

        self.play(explanation.grow_animation())
        self.wait(2)

        # Celebrate
        self.play(
            explanation.shrink_animation(),
            teacher.celebrate()
        )
        self.wait(1)
