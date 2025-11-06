"""
Basic Example Scenes
Simple demonstrations of actor capabilities.
"""

from manim import *
import sys
sys.path.append('..')
from actors import BaseActor, ActorStyle, SpeechBubble, GestureLibrary


class ActorIntroduction(Scene):
    """
    Introduce all actor styles.

    Run with: manim -pql scenes/basic_examples.py ActorIntroduction
    """

    def construct(self):
        title = Text("Manim Actor System", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Show different actor styles
        styles = [
            (ActorStyle.STICK_FIGURE, "Stick Figure"),
            (ActorStyle.SIMPLE, "Simple"),
            (ActorStyle.CARTOON, "Cartoon"),
            (ActorStyle.PROFESSIONAL, "Professional")
        ]

        for i, (style, name) in enumerate(styles):
            actor = BaseActor(style=style, scale_factor=0.8)
            actor.to_edge(DOWN).shift(LEFT * 4 + RIGHT * 2.5 * i)

            label = Text(name, font_size=20).next_to(actor, DOWN)

            self.play(
                FadeIn(actor),
                Write(label)
            )
            self.play(actor.wave())

            if i < len(styles) - 1:
                self.wait(0.3)

        self.wait(2)


class SimplePresentation(Scene):
    """
    Actor presents a simple concept.

    Run with: manim -pql scenes/basic_examples.py SimplePresentation
    """

    def construct(self):
        # Create actor
        actor = BaseActor(style=ActorStyle.CARTOON, scale_factor=1.0)
        actor.to_edge(LEFT).to_edge(DOWN)

        # Entry
        self.play(FadeIn(actor, shift=RIGHT))
        self.play(actor.wave())

        # Greeting
        greeting = SpeechBubble("Hello! Let's learn together!", is_math=False)
        greeting.attach_to(actor)

        self.play(greeting.grow_animation())
        self.wait(2)
        self.play(greeting.shrink_animation())

        # Show concept
        concept = Text("Manim is awesome!", font_size=40).to_edge(UP)
        self.play(
            Write(concept),
            actor.point_to(concept)
        )
        self.wait(1)

        # React
        self.play(
            actor.celebrate(),
            actor.change_expression("happy")
        )
        self.wait(2)


class MathLesson(Scene):
    """
    Actor teaches a mathematical concept.

    Run with: manim -pql scenes/basic_examples.py MathLesson
    """

    def construct(self):
        # Create teacher actor
        teacher = BaseActor(
            style=ActorStyle.PROFESSIONAL,
            scale_factor=0.9,
            color_scheme={
                "head": BLUE_D,
                "body": BLUE_E,
                "arms": BLUE_D,
                "legs": GREY_BROWN,
                "accent": BLUE_B
            }
        )
        teacher.to_corner(DL)

        # Title
        title = Text("The Pythagorean Theorem", font_size=40).to_edge(UP)

        # Entry
        self.play(FadeIn(teacher, shift=UP))
        self.play(Write(title))
        self.wait(0.5)

        # Introduction
        intro_bubble = SpeechBubble(
            "Let me explain an important theorem!",
            is_math=False
        ).attach_to(teacher)

        self.play(
            intro_bubble.grow_animation(),
            teacher.change_expression("happy")
        )
        self.wait(2)
        self.play(intro_bubble.shrink_animation())

        # Show equation
        equation = MathTex(r"a^2 + b^2 = c^2", font_size=60).shift(RIGHT * 2)

        self.play(
            Write(equation),
            teacher.point_to(equation)
        )
        self.wait(1)

        # Explain parts
        parts = [equation[0][0:2], equation[0][4:6], equation[0][8:10]]
        labels = ["a squared", "b squared", "c squared"]

        for part, label in zip(parts, labels):
            bubble = SpeechBubble(f"This is {label}", is_math=False).attach_to(teacher)

            self.play(
                Indicate(part, color=YELLOW),
                teacher.point_to(part),
                bubble.grow_animation()
            )
            self.wait(1.5)
            self.play(bubble.shrink_animation())

        # Conclusion
        self.play(
            teacher.celebrate(),
            teacher.change_expression("happy"),
            Circumscribe(equation, color=GREEN)
        )
        self.wait(2)


class ActorInteraction(Scene):
    """
    Actor interacts with animated objects.

    Run with: manim -pql scenes/basic_examples.py ActorInteraction
    """

    def construct(self):
        # Create actor
        actor = BaseActor(style=ActorStyle.CARTOON, scale_factor=1.0)
        actor.to_corner(DR)

        self.play(FadeIn(actor))
        self.play(actor.wave())

        # Create moving circle
        circle = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        circle.to_edge(LEFT)

        circle_label = Text("Watch this!", font_size=30).next_to(circle, UP)

        self.play(
            Create(circle),
            Write(circle_label)
        )

        # Actor points to circle
        self.play(actor.point_to(circle))

        # Move circle
        self.play(
            circle.animate.shift(RIGHT * 4),
            circle_label.animate.shift(RIGHT * 4),
            run_time=2
        )

        # Actor reacts
        surprised_bubble = SpeechBubble("Wow! It moved!", is_math=False).attach_to(actor)

        self.play(
            actor.change_expression("surprised"),
            surprised_bubble.grow_animation()
        )
        self.wait(2)
        self.play(surprised_bubble.shrink_animation())

        # Transform circle
        square = Square(side_length=1, color=RED, fill_opacity=0.5).move_to(circle)

        self.play(
            Transform(circle, square),
            FadeOut(circle_label)
        )

        # Actor celebrates
        self.play(
            actor.celebrate(),
            actor.change_expression("happy")
        )

        celebration_bubble = SpeechBubble("Amazing!", is_math=False).attach_to(actor)
        self.play(celebration_bubble.grow_animation())
        self.wait(2)
