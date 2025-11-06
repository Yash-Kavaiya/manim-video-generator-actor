#!/usr/bin/env python3
"""
Manim Actor Video Generator - Apify Actor Entry Point

This is the main entry point for the Apify Actor that generates
animated math videos using the Manim library.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apify import Actor
from actors import BaseActor, ActorStyle, SpeechBubble, GestureLibrary
from actors.speech_bubble import ThoughtBubble
from configs import (
    TEACHER_CONFIG,
    STUDENT_CONFIG,
    PRESENTER_CONFIG,
    STICK_FIGURE_CONFIG,
    COLOR_SCHEMES,
    create_actor_from_config
)


class ManimActorGenerator:
    """Main generator class for Apify Actor."""

    def __init__(self, input_data: Dict[str, Any], actor_instance: Actor):
        """
        Initialize generator with input data.

        Args:
            input_data: Input configuration from Apify
            actor_instance: Apify Actor instance for logging and storage
        """
        self.input = input_data
        self.actor = actor_instance
        self.scene_type = input_data.get('sceneType', 'SimplePresentation')
        self.quality = input_data.get('videoQuality', 'medium')
        self.output_dir = Path('/usr/src/app/storage/key_value_stores/default')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_quality_flags(self) -> str:
        """Map quality setting to Manim flags."""
        quality_map = {
            'low': '-ql',
            'medium': '-qm',
            'high': '-qh',
            'production': '-qk'
        }
        return quality_map.get(self.quality, '-qm')

    def get_scene_file(self) -> str:
        """Determine which scene file to use."""
        basic_scenes = ['ActorIntroduction', 'SimplePresentation', 'MathLesson', 'ActorInteraction']
        advanced_scenes = ['ProblemSolving', 'MultiActorScene', 'InteractiveTutorial']

        if self.scene_type in basic_scenes:
            return 'scenes/basic_examples.py'
        elif self.scene_type in advanced_scenes:
            return 'scenes/advanced_examples.py'
        elif self.scene_type == 'CustomScene':
            return self.create_custom_scene()
        else:
            return 'scenes/basic_examples.py'

    def create_custom_scene(self) -> str:
        """Create a custom scene file based on input configuration."""
        custom_config = self.input.get('customSceneConfig', {})
        actor_style = self.input.get('actorStyle', 'cartoon')
        color_scheme = self.input.get('actorColorScheme', 'blue')

        # Generate custom scene Python code
        scene_code = f'''"""
Custom generated scene from Apify Actor input.
"""

from manim import *
import sys
sys.path.append('..')
from actors import BaseActor, ActorStyle, SpeechBubble

class CustomScene(Scene):
    """Dynamically generated custom scene."""

    def construct(self):
        # Create actor
        actor = BaseActor(
            style=ActorStyle.{actor_style.upper()},
            scale_factor=1.0
        )
        actor.to_edge(LEFT).to_edge(DOWN)

        # Title
        title = Text("{custom_config.get('title', 'Custom Video')}", font_size=40).to_edge(UP)

        # Entry
        self.play(FadeIn(actor, shift=RIGHT))
        self.play(Write(title))
        self.play(actor.wave())
        self.wait(0.5)

        # Main content
        main_text = Text("{custom_config.get('mainText', 'Hello!')}", font_size=36)
        self.play(
            Write(main_text),
            actor.point_to(main_text)
        )
        self.wait(2)
        self.play(FadeOut(main_text))

        # Equation
        equation_str = r"{custom_config.get('equation', 'E = mc^2')}"
        equation = MathTex(equation_str, font_size=50)
        self.play(
            Write(equation),
            actor.point_to(equation)
        )
        self.wait(2)

        # Dialogues
        dialogues = {json.dumps(custom_config.get('dialogues', []))}
        for dialogue in dialogues:
            text = dialogue.get('text', '')
            is_math = dialogue.get('isMath', False)
            duration = dialogue.get('duration', 2)

            bubble = SpeechBubble(text, is_math=is_math).attach_to(actor)
            self.play(bubble.grow_animation())
            self.wait(duration)
            self.play(bubble.shrink_animation())
            self.wait(0.3)

        # Celebration if enabled
        if {str(custom_config.get('showCelebration', True)).lower()}:
            self.play(
                actor.celebrate(),
                actor.change_expression("happy")
            )
            self.wait(2)
'''

        # Write custom scene file
        custom_file = Path('custom_scene_generated.py')
        custom_file.write_text(scene_code)

        return str(custom_file)

    async def generate_video(self) -> Optional[Path]:
        """
        Generate video using Manim.

        Returns:
            Path to generated video file or None if failed
        """
        await self.actor.log.info(f'Starting video generation for scene: {self.scene_type}')
        await self.actor.log.info(f'Quality: {self.quality}')

        try:
            # Determine scene file
            if self.scene_type == 'CustomScene':
                scene_file = self.create_custom_scene()
                scene_class = 'CustomScene'
            else:
                scene_file = self.get_scene_file()
                scene_class = self.scene_type

            # Build manim command
            quality_flag = self.get_quality_flags()
            output_format = self.input.get('outputFormat', 'mp4')

            cmd = [
                'manim',
                quality_flag,
                '--format', output_format,
                '--media_dir', str(self.output_dir.parent),
                scene_file,
                scene_class
            ]

            await self.actor.log.info(f'Running command: {" ".join(cmd)}')

            # Run manim
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                await self.actor.log.info('Video generated successfully!')

                # Find the generated video
                video_files = list(self.output_dir.parent.rglob(f'*.{output_format}'))
                if video_files:
                    # Get the most recent video file
                    latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
                    await self.actor.log.info(f'Found video: {latest_video}')
                    return latest_video
                else:
                    await self.actor.log.error('No video file found after generation')
                    return None
            else:
                error_msg = stderr.decode('utf-8') if stderr else 'Unknown error'
                await self.actor.log.error(f'Manim failed: {error_msg}')
                return None

        except Exception as e:
            await self.actor.log.exception(f'Error generating video: {str(e)}')
            return None

    async def save_output(self, video_path: Path):
        """
        Save video to Apify key-value store and metadata to dataset.

        Args:
            video_path: Path to generated video file
        """
        try:
            # Read video file
            video_data = video_path.read_bytes()

            # Get output filename
            output_name = self.input.get('outputFileName', 'manim_actor_video')
            output_format = self.input.get('outputFormat', 'mp4')
            final_name = f'{output_name}.{output_format}'

            # Save to key-value store
            await self.actor.set_value(final_name, video_data, content_type=f'video/{output_format}')
            await self.actor.log.info(f'Video saved as: {final_name}')

            # Get file size
            file_size = video_path.stat().st_size
            file_size_mb = round(file_size / (1024 * 1024), 2)

            # Create metadata
            metadata = {
                'fileName': final_name,
                'videoUrl': f'https://api.apify.com/v2/key-value-stores/{{storeId}}/records/{final_name}',
                'sceneType': self.scene_type,
                'quality': self.quality,
                'actorStyle': self.input.get('actorStyle', 'cartoon'),
                'actorColorScheme': self.input.get('actorColorScheme', 'blue'),
                'outputFormat': output_format,
                'fileSizeMB': file_size_mb,
                'fps': self.input.get('fps', 30),
                'backgroundColor': self.input.get('backgroundColor', '#000000'),
                'multiActorMode': self.input.get('multiActorMode', False),
                'generatedAt': video_path.stat().st_mtime
            }

            # Save metadata to dataset
            await self.actor.push_data(metadata)
            await self.actor.log.info('Metadata saved to dataset')

            # Generate subtitles if enabled
            if self.input.get('enableSubtitles', False):
                await self.generate_subtitles(video_path, output_name)

        except Exception as e:
            await self.actor.log.exception(f'Error saving output: {str(e)}')

    async def generate_subtitles(self, video_path: Path, base_name: str):
        """
        Generate subtitle file for the video.

        Args:
            video_path: Path to video file
            base_name: Base name for subtitle file
        """
        try:
            # For now, create a simple placeholder subtitle file
            # In a real implementation, you would extract actual speech/text timing
            subtitle_content = """1
00:00:00,000 --> 00:00:05,000
Generated with Manim Actor Video Generator

2
00:00:05,000 --> 00:00:10,000
Visit apify.com for more information
"""

            subtitle_file = f'{base_name}.srt'
            await self.actor.set_value(subtitle_file, subtitle_content, content_type='text/plain')
            await self.actor.log.info(f'Subtitles saved as: {subtitle_file}')

        except Exception as e:
            await self.actor.log.exception(f'Error generating subtitles: {str(e)}')


async def main():
    """Main entry point for Apify Actor."""
    async with Actor() as actor:
        # Get input
        actor_input = await actor.get_input() or {}

        await actor.log.info('Manim Actor Video Generator started')
        await actor.log.info(f'Input: {json.dumps(actor_input, indent=2)}')

        # Validate required inputs
        if 'sceneType' not in actor_input:
            await actor.log.error('Missing required input: sceneType')
            await actor.fail('sceneType is required')
            return

        try:
            # Create generator
            generator = ManimActorGenerator(actor_input, actor)

            # Generate video
            video_path = await generator.generate_video()

            if video_path:
                # Save output
                await generator.save_output(video_path)
                await actor.log.info('Actor completed successfully!')
            else:
                await actor.fail('Failed to generate video')

        except Exception as e:
            await actor.log.exception(f'Actor failed with error: {str(e)}')
            await actor.fail(str(e))


if __name__ == '__main__':
    asyncio.run(main())
