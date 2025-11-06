"""
Gesture Library
Pre-built gesture animations and interaction utilities.
"""

from manim import *
from typing import Callable, List
import numpy as np


class GestureLibrary:
    """
    Library of common gestures and interactions for actors.

    Provides:
    - Pre-built gesture sequences
    - Interaction helpers (pointing, following, reacting)
    - Timing utilities for synchronized animations
    """

    @staticmethod
    def point_and_explain(
        actor,
        target: Mobject,
        explanation_text: str,
        scene,
        is_math: bool = False,
        wait_time: float = 2.0
    ):
        """
        Point to target and show explanation bubble.

        Args:
            actor: The actor performing the gesture
            target: What to point at
            explanation_text: Text/math to display
            scene: Scene to add animations to
            is_math: Whether explanation is mathematical
            wait_time: How long to display
        """
        from .speech_bubble import SpeechBubble

        # Create speech bubble
        bubble = SpeechBubble(explanation_text, is_math=is_math).attach_to(actor)

        # Sequence
        scene.play(actor.point_to(target))
        scene.play(bubble.grow_animation())
        scene.wait(wait_time)
        scene.play(bubble.shrink_animation())

    @staticmethod
    def react_to_result(
        actor,
        result: Mobject,
        reaction: str,
        scene
    ):
        """
        React to a mathematical result.

        Args:
            actor: The actor reacting
            result: The result mobject
            reaction: "happy", "surprised", "confused", "celebrate"
            scene: Scene to add animations to
        """
        if reaction == "celebrate":
            scene.play(
                actor.celebrate(),
                actor.change_expression("happy")
            )
        elif reaction == "surprised":
            scene.play(
                actor.change_expression("surprised"),
                actor.animate.scale(1.1)
            )
            scene.wait(0.5)
            scene.play(actor.animate.scale(1/1.1))
        elif reaction == "confused":
            scene.play(
                actor.change_expression("confused"),
                actor.shake_head()
            )
        else:  # happy
            scene.play(
                actor.change_expression("happy"),
                actor.nod()
            )

    @staticmethod
    def follow_mobject(
        actor,
        target: Mobject,
        scene,
        duration: float = 2.0
    ):
        """
        Make actor's head follow a moving mobject.

        Args:
            actor: The actor
            target: Mobject to follow
            scene: Scene
            duration: How long to follow
        """
        def update_head(mob, dt):
            # Calculate angle to target
            actor_pos = mob.get_center()
            target_pos = target.get_center()
            direction = target_pos - actor_pos

            # Rotate head slightly toward target
            angle = np.arctan2(direction[1], direction[0])
            # Limit rotation
            max_angle = PI / 6
            angle = np.clip(angle, -max_angle, max_angle)

        actor.head_group.add_updater(update_head)
        scene.wait(duration)
        actor.head_group.remove_updater(update_head)

    @staticmethod
    def presentation_sequence(
        actor,
        scene,
        entry_side: str = "LEFT"
    ):
        """
        Standard presentation entry sequence.

        Args:
            actor: The actor
            scene: Scene
            entry_side: "LEFT", "RIGHT", "BOTTOM"
        """
        # Position actor off-screen
        if entry_side == "LEFT":
            actor.to_edge(LEFT, buff=-2)
            target_pos = LEFT * 3 + DOWN * 2
        elif entry_side == "RIGHT":
            actor.to_edge(RIGHT, buff=-2)
            target_pos = RIGHT * 3 + DOWN * 2
        else:  # BOTTOM
            actor.to_edge(DOWN, buff=-2)
            target_pos = DOWN * 2

        # Entry sequence
        scene.play(
            actor.walk_to(target_pos),
            run_time=1.5
        )
        scene.play(actor.wave())
        scene.play(actor.change_expression("happy"))

    @staticmethod
    def teaching_gesture(
        actor,
        equation: Mobject,
        highlight_parts: List[Mobject],
        scene
    ):
        """
        Gesture sequence for teaching/explaining equations.

        Args:
            actor: The actor
            equation: The equation to explain
            highlight_parts: Parts to highlight in sequence
            scene: Scene
        """
        # Point to equation
        scene.play(actor.point_to(equation))
        scene.wait(0.5)

        # Highlight each part
        for part in highlight_parts:
            scene.play(
                Indicate(part, color=YELLOW),
                actor.point_to(part)
            )
            scene.wait(0.5)

        # Nod in agreement
        scene.play(
            actor.change_expression("happy"),
            actor.nod()
        )

    @staticmethod
    def problem_solving_sequence(
        actor,
        scene,
        think_time: float = 2.0
    ):
        """
        Show actor thinking through a problem.

        Args:
            actor: The actor
            scene: Scene
            think_time: How long to show thinking
        """
        from .speech_bubble import ThoughtBubble

        # Look confused
        scene.play(actor.change_expression("confused"))
        scene.play(actor.think())

        # Show thought bubble with question mark
        thought = ThoughtBubble("?", is_math=False).attach_to(actor)
        scene.play(thought.grow_animation())
        scene.wait(think_time)

        # Eureka moment
        scene.play(thought.shrink_animation())
        scene.play(
            actor.change_expression("surprised"),
            actor.animate.scale(1.15)
        )
        scene.wait(0.3)
        scene.play(actor.animate.scale(1/1.15))

        # Show solution thought
        solution_thought = ThoughtBubble("!", is_math=False).attach_to(actor)
        scene.play(solution_thought.grow_animation())
        scene.play(actor.change_expression("happy"))
        scene.wait(1)
        scene.play(solution_thought.shrink_animation())

    @staticmethod
    def comparison_gesture(
        actor,
        left_obj: Mobject,
        right_obj: Mobject,
        scene,
        prefer_left: bool = True
    ):
        """
        Compare two objects with gestures.

        Args:
            actor: The actor
            left_obj: Left object to compare
            right_obj: Right object to compare
            scene: Scene
            prefer_left: Which side actor prefers
        """
        # Point to left
        scene.play(actor.point_to(left_obj))
        scene.wait(0.5)

        # Point to right
        scene.play(actor.point_to(right_obj))
        scene.wait(0.5)

        # Show preference
        if prefer_left:
            scene.play(
                actor.point_to(left_obj),
                actor.change_expression("happy")
            )
            scene.play(actor.nod())
        else:
            scene.play(
                actor.point_to(right_obj),
                actor.change_expression("happy")
            )
            scene.play(actor.nod())

    @staticmethod
    def emphasize_point(
        actor,
        target: Mobject,
        scene,
        emphasis_type: str = "point"
    ):
        """
        Emphasize a point with dramatic gesture.

        Args:
            actor: The actor
            target: What to emphasize
            scene: Scene
            emphasis_type: "point", "celebrate", "wave"
        """
        if emphasis_type == "point":
            scene.play(
                actor.point_to(target),
                Circumscribe(target, color=YELLOW, run_time=2)
            )
        elif emphasis_type == "celebrate":
            scene.play(
                actor.celebrate(),
                Flash(target, color=YELLOW, flash_radius=0.5)
            )
        elif emphasis_type == "wave":
            scene.play(
                actor.wave(),
                Wiggle(target)
            )

    @staticmethod
    def create_idle_updater(actor) -> Callable:
        """
        Create an idle animation updater for subtle movement.

        Args:
            actor: The actor

        Returns:
            Updater function that can be added to actor
        """
        import time
        start_time = time.time()

        def idle_update(mob, dt):
            current_time = time.time() - start_time
            # Subtle breathing effect
            breath_scale = 1 + 0.02 * np.sin(2 * PI * current_time / 2)
            mob.scale(breath_scale / mob.height * actor.height)

        return idle_update

    @staticmethod
    def multi_actor_conversation(
        actor1,
        actor2,
        dialogues: List[tuple],
        scene
    ):
        """
        Coordinate conversation between two actors.

        Args:
            actor1: First actor
            actor2: Second actor
            dialogues: List of (actor_num, text, is_math) tuples
            scene: Scene
        """
        from .speech_bubble import SpeechBubble

        for actor_num, text, is_math in dialogues:
            current_actor = actor1 if actor_num == 1 else actor2
            other_actor = actor2 if actor_num == 1 else actor1

            # Current actor speaks
            bubble = SpeechBubble(text, is_math=is_math).attach_to(current_actor)

            # Current actor turns to other
            scene.play(
                current_actor.change_expression("happy"),
                bubble.grow_animation()
            )

            # Other actor nods
            scene.play(other_actor.nod())
            scene.wait(1.5)

            scene.play(bubble.shrink_animation())
            scene.wait(0.3)
