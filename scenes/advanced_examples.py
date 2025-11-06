"""
Advanced Example Scenes
Complex demonstrations with multiple actors and interactions.
"""

from manim import *
import sys
sys.path.append('..')
from actors import BaseActor, ActorStyle, SpeechBubble, GestureLibrary
from actors.speech_bubble import ThoughtBubble


class ProblemSolving(Scene):
    """
    Actor works through a problem with thinking animations.

    Run with: manim -pql scenes/advanced_examples.py ProblemSolving
    """

    def construct(self):
        # Create student actor
        student = BaseActor(
            style=ActorStyle.SIMPLE,
            scale_factor=0.9,
            color_scheme={
                "head": TEAL_D,
                "body": TEAL_E,
                "arms": TEAL_D,
                "legs": TEAL_D,
                "accent": TEAL_A
            }
        )
        student.to_corner(DL)

        # Show problem
        title = Text("Solving a Problem", font_size=40).to_edge(UP)
        problem = MathTex(r"x^2 - 5x + 6 = 0", font_size=50).shift(UP)

        self.play(
            FadeIn(student, shift=UP),
            Write(title)
        )
        self.wait(0.5)

        self.play(Write(problem))
        self.play(student.point_to(problem))
        self.wait(0.5)

        # Show confusion
        confused_bubble = SpeechBubble("Hmm... how do I solve this?", is_math=False).attach_to(student)
        self.play(
            student.change_expression("confused"),
            confused_bubble.grow_animation()
        )
        self.wait(1.5)
        self.play(confused_bubble.shrink_animation())

        # Think
        self.play(student.think())

        thought = ThoughtBubble(r"(x-2)(x-3) = 0", is_math=True).attach_to(student)
        self.play(thought.grow_animation())
        self.wait(2)

        # Show factored form
        factored = MathTex(r"(x-2)(x-3) = 0", font_size=50).next_to(problem, DOWN, buff=0.5)

        self.play(
            Write(factored),
            student.point_to(factored)
        )
        self.wait(1)
        self.play(thought.shrink_animation())

        # Eureka moment
        self.play(
            student.change_expression("surprised"),
            student.animate.scale(1.1)
        )
        self.wait(0.3)
        self.play(student.animate.scale(1/1.1))

        eureka_bubble = SpeechBubble("I've got it!", is_math=False).attach_to(student)
        self.play(eureka_bubble.grow_animation())
        self.wait(1)
        self.play(eureka_bubble.shrink_animation())

        # Show solutions
        solution = MathTex(r"x = 2 \text{ or } x = 3", font_size=50).next_to(factored, DOWN, buff=0.5)

        self.play(
            Write(solution),
            student.point_to(solution)
        )

        # Celebrate
        self.play(
            student.celebrate(),
            student.change_expression("happy"),
            Circumscribe(solution, color=GREEN, run_time=2)
        )

        success_bubble = SpeechBubble("Success!", is_math=False).attach_to(student)
        self.play(success_bubble.grow_animation())
        self.wait(2)


class MultiActorScene(Scene):
    """
    Two actors have a conversation.

    Run with: manim -pql scenes/advanced_examples.py MultiActorScene
    """

    def construct(self):
        # Create two actors
        teacher = BaseActor(
            style=ActorStyle.PROFESSIONAL,
            scale_factor=0.8,
            color_scheme={
                "head": BLUE_D,
                "body": BLUE_E,
                "arms": BLUE_D,
                "legs": GREY_BROWN,
                "accent": BLUE_B
            }
        )
        teacher.to_corner(DL)

        student = BaseActor(
            style=ActorStyle.CARTOON,
            scale_factor=0.8,
            color_scheme={
                "head": ORANGE,
                "body": YELLOW_E,
                "arms": ORANGE,
                "legs": ORANGE,
                "accent": YELLOW
            }
        )
        student.to_corner(DR)

        # Title
        title = Text("A Math Conversation", font_size=40).to_edge(UP)

        # Entry
        self.play(
            FadeIn(teacher, shift=RIGHT),
            FadeIn(student, shift=LEFT),
            Write(title)
        )
        self.play(teacher.wave(), student.wave())
        self.wait(0.5)

        # Conversation using gesture library
        dialogues = [
            (1, "Let's explore calculus!", False),
            (2, "What is a derivative?", False),
            (1, r"\frac{df}{dx}", True),
            (2, "I understand now!", False)
        ]

        GestureLibrary.multi_actor_conversation(
            teacher,
            student,
            dialogues,
            self
        )

        # Both celebrate
        self.play(
            teacher.celebrate(),
            student.celebrate(),
            teacher.change_expression("happy"),
            student.change_expression("happy")
        )
        self.wait(2)


class InteractiveTutorial(Scene):
    """
    Comprehensive tutorial showing various features.

    Run with: manim -pql scenes/advanced_examples.py InteractiveTutorial
    """

    def construct(self):
        # Create actor
        guide = BaseActor(
            style=ActorStyle.CARTOON,
            scale_factor=0.9
        )
        guide.to_edge(LEFT).to_edge(DOWN)

        # Title
        title = Text("Interactive Math Tutorial", font_size=40).to_edge(UP)

        self.play(
            FadeIn(guide, shift=RIGHT),
            Write(title)
        )
        self.play(guide.wave())
        self.wait(0.5)

        # Section 1: Introduction to equation
        intro = SpeechBubble("Let's solve an equation!", is_math=False).attach_to(guide)
        self.play(intro.grow_animation())
        self.wait(1.5)
        self.play(intro.shrink_animation())

        equation = MathTex(r"2x + 3 = 7", font_size=50).shift(RIGHT * 2 + UP)
        self.play(
            Write(equation),
            guide.point_to(equation)
        )
        self.wait(1)

        # Section 2: Step 1 - Subtract 3
        step1_bubble = SpeechBubble("First, subtract 3 from both sides", is_math=False).attach_to(guide)
        self.play(step1_bubble.grow_animation())
        self.wait(2)
        self.play(step1_bubble.shrink_animation())

        step1 = MathTex(r"2x = 4", font_size=50).next_to(equation, DOWN, buff=0.5)
        arrow1 = Arrow(equation.get_bottom(), step1.get_top(), buff=0.1, color=YELLOW)

        self.play(
            Create(arrow1),
            Write(step1),
            guide.point_to(step1)
        )
        self.wait(1)

        # Section 3: Step 2 - Divide by 2
        step2_bubble = SpeechBubble("Now divide both sides by 2", is_math=False).attach_to(guide)
        self.play(step2_bubble.grow_animation())
        self.wait(2)
        self.play(step2_bubble.shrink_animation())

        solution = MathTex(r"x = 2", font_size=50, color=GREEN).next_to(step1, DOWN, buff=0.5)
        arrow2 = Arrow(step1.get_bottom(), solution.get_top(), buff=0.1, color=YELLOW)

        self.play(
            Create(arrow2),
            Write(solution),
            guide.point_to(solution)
        )
        self.wait(1)

        # Section 4: Verification
        verify_bubble = SpeechBubble("Let's verify: 2(2) + 3 = 7", is_math=False).attach_to(guide)
        self.play(verify_bubble.grow_animation())
        self.wait(2)

        # Highlight verification
        self.play(
            Circumscribe(solution, color=GREEN, run_time=2),
            Flash(solution, color=GREEN)
        )
        self.play(verify_bubble.shrink_animation())

        # Section 5: Celebration
        self.play(
            guide.celebrate(),
            guide.change_expression("happy")
        )

        success = SpeechBubble("Perfect! You solved it!", is_math=False).attach_to(guide)
        self.play(success.grow_animation())
        self.wait(2)

        # Ending
        self.play(
            FadeOut(success),
            guide.wave()
        )
        self.wait(1)
