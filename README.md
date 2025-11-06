# Manim Actor Video Generator

A comprehensive, modular actor system for creating animated characters in [Manim](https://www.manim.community/) videos. Perfect for educational content creators who want to add engaging, animated presenters to their mathematical and scientific visualizations.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Manim Version](https://img.shields.io/badge/manim-0.18.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Multiple Actor Styles**: Choose from Cartoon, Simple, Stick Figure, or Professional styles
- **Rich Gesture Library**: Pre-built animations for pointing, waving, nodding, celebrating, and more
- **Speech & Thought Bubbles**: Dynamic dialogue system with support for both text and LaTeX math
- **Modular Design**: Easily customize colors, proportions, and behaviors
- **Interactive Animations**: Actors that react to and interact with mathematical content
- **Multi-Actor Support**: Coordinate conversations between multiple characters
- **Simple API**: Clean, intuitive Python interface
- **CLI Tool**: Command-line utility for quick video generation

## Installation

### Prerequisites

- Python 3.9 or higher
- Manim Community Edition 0.18.0 or higher

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Yash-Kavaiya/manim-video-generator-actor.git
cd manim-video-generator-actor

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### Install Manim

If you don't have Manim installed:

```bash
pip install manim

# On Linux, you may also need:
sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg

# On macOS:
brew install cairo pango ffmpeg

# Verify installation
manim --version
```

## Quick Start

### Basic Example

```python
from manim import *
from actors import BaseActor, ActorStyle, SpeechBubble

class MyFirstActor(Scene):
    def construct(self):
        # Create an actor
        actor = BaseActor(style=ActorStyle.CARTOON)
        actor.to_edge(LEFT).to_edge(DOWN)

        # Add to scene
        self.play(FadeIn(actor))
        self.play(actor.wave())

        # Add speech bubble
        bubble = SpeechBubble("Hello, Manim!")
        bubble.attach_to(actor)

        self.play(bubble.grow_animation())
        self.wait(2)
```

Run it:
```bash
manim -pql examples/quick_start.py QuickStart
```

### Using the CLI Tool

```bash
# List all available scenes
python generate.py --list

# Generate a video (low quality, with preview)
python generate.py --scene ActorIntroduction --quality low --preview

# Generate high-quality video
python generate.py --scene MathLesson --quality high

# Production quality
python generate.py --scene MultiActorScene --quality production --preview
```

## Actor Styles

The system includes four distinct actor styles:

### 1. Stick Figure
Minimalist design, fastest to render
```python
actor = BaseActor(style=ActorStyle.STICK_FIGURE)
```

### 2. Simple
Clean geometric shapes, good balance of detail and performance
```python
actor = BaseActor(style=ActorStyle.SIMPLE)
```

### 3. Cartoon
Expressive with larger head, personality-rich
```python
actor = BaseActor(style=ActorStyle.CARTOON)
```

### 4. Professional
Polished silhouette style, ideal for formal presentations
```python
actor = BaseActor(style=ActorStyle.PROFESSIONAL)
```

## Customization

### Custom Colors

```python
actor = BaseActor(
    style=ActorStyle.CARTOON,
    scale_factor=1.2,
    color_scheme={
        "head": PURPLE_D,
        "body": PURPLE_E,
        "arms": PURPLE_D,
        "legs": PURPLE_D,
        "accent": PURPLE_A
    }
)
```

### Using Presets

```python
from configs.actor_config import create_actor_from_config, TEACHER_CONFIG

teacher = create_actor_from_config(TEACHER_CONFIG)
```

Available presets:
- `TEACHER_CONFIG` - Professional blue teacher
- `STUDENT_CONFIG` - Friendly orange student
- `PRESENTER_CONFIG` - Teal presenter
- `STICK_FIGURE_CONFIG` - White stick figure

## Animation Methods

### Basic Gestures

```python
# Wave
self.play(actor.wave())

# Point to object
self.play(actor.point_to(equation))

# Nod
self.play(actor.nod(times=3))

# Shake head
self.play(actor.shake_head())

# Think (hand to chin)
self.play(actor.think())

# Celebrate (arms up)
self.play(actor.celebrate())

# Walk to position
self.play(actor.walk_to(RIGHT * 3))
```

### Expressions

```python
# Change facial expression
self.play(actor.change_expression("happy"))
self.play(actor.change_expression("sad"))
self.play(actor.change_expression("surprised"))
self.play(actor.change_expression("confused"))
self.play(actor.change_expression("neutral"))
```

### Speech Bubbles

```python
from actors import SpeechBubble

# Text bubble
bubble = SpeechBubble("Hello!", is_math=False)
bubble.attach_to(actor)
self.play(bubble.grow_animation())
self.wait(2)
self.play(bubble.shrink_animation())

# Math bubble
math_bubble = SpeechBubble(r"E = mc^2", is_math=True)
math_bubble.attach_to(actor)
self.play(math_bubble.grow_animation())
```

### Thought Bubbles

```python
from actors.speech_bubble import ThoughtBubble

thought = ThoughtBubble("Hmm...", is_math=False)
thought.attach_to(actor)
self.play(thought.grow_animation())
```

## Advanced Usage

### Gesture Library

The `GestureLibrary` provides coordinated animation sequences:

```python
from actors import GestureLibrary

# Point and explain
GestureLibrary.point_and_explain(
    actor,
    equation,
    "This is important!",
    self
)

# React to result
GestureLibrary.react_to_result(
    actor,
    solution,
    reaction="celebrate",
    scene=self
)

# Teaching gesture
GestureLibrary.teaching_gesture(
    actor,
    equation,
    highlight_parts=[part1, part2, part3],
    scene=self
)

# Problem solving sequence
GestureLibrary.problem_solving_sequence(actor, self, think_time=2.0)
```

### Multi-Actor Conversations

```python
from actors import GestureLibrary

teacher = BaseActor(style=ActorStyle.PROFESSIONAL).to_corner(DL)
student = BaseActor(style=ActorStyle.CARTOON).to_corner(DR)

self.play(FadeIn(teacher), FadeIn(student))

dialogues = [
    (1, "Let's learn calculus!", False),
    (2, "What is a derivative?", False),
    (1, r"\frac{df}{dx}", True),
    (2, "I understand now!", False)
]

GestureLibrary.multi_actor_conversation(teacher, student, dialogues, self)
```

## Example Scenes

The project includes several example scenes:

### Basic Examples (`scenes/basic_examples.py`)

1. **ActorIntroduction** - Showcase all actor styles
2. **SimplePresentation** - Actor presents a concept
3. **MathLesson** - Teach the Pythagorean theorem
4. **ActorInteraction** - Interact with animated objects

### Advanced Examples (`scenes/advanced_examples.py`)

1. **ProblemSolving** - Work through a math problem with thinking animations
2. **MultiActorScene** - Two actors have a conversation
3. **InteractiveTutorial** - Comprehensive step-by-step tutorial

Run any example:
```bash
manim -pql scenes/basic_examples.py MathLesson
manim -pql scenes/advanced_examples.py ProblemSolving
```

## Project Structure

```
manim-video-generator-actor/
├── actors/                  # Actor system modules
│   ├── __init__.py
│   ├── base_actor.py       # Core actor class
│   ├── speech_bubble.py    # Dialogue system
│   └── gestures.py         # Gesture library
├── scenes/                  # Example scenes
│   ├── basic_examples.py
│   └── advanced_examples.py
├── configs/                 # Configuration presets
│   └── actor_config.py
├── examples/               # Quick start examples
│   └── quick_start.py
├── assets/                 # SVG assets (optional)
├── generate.py            # CLI tool
├── requirements.txt
├── setup.py
└── README.md
```

## Performance Tips

1. **Use simpler styles for faster rendering**: Stick Figure renders 3x faster than detailed styles
2. **Limit simultaneous actors**: Keep to 2-3 actors per scene for best performance
3. **Preview with low quality**: Use `-ql` flag during development
4. **Cache complex assets**: Use Manim's `cache()` for repeated elements
5. **Optimize LaTeX**: Pre-compile frequently used equations

## Rendering Quality Options

```bash
# Low quality (fast preview, 480p15)
manim -ql scene.py SceneName

# Medium quality (854x480, 30fps)
manim -qm scene.py SceneName

# High quality (1080p60)
manim -qh scene.py SceneName

# Production quality (4K, 60fps)
manim -qk scene.py SceneName

# With preview (-p flag)
manim -pql scene.py SceneName
```

## Creating Custom Actors

Extend the `BaseActor` class for custom behavior:

```python
from actors import BaseActor

class MyCustomActor(BaseActor):
    def custom_gesture(self):
        """Add your custom animation."""
        return Succession(
            self.wave(),
            self.nod(),
            self.celebrate()
        )
```

## Troubleshooting

### Common Issues

**LaTeX errors**: Ensure LaTeX is properly installed
```bash
# Test LaTeX
manim --version
```

**Import errors**: Make sure you're in the project directory
```python
import sys
sys.path.append('..')
from actors import BaseActor
```

**Slow rendering**: Use lower quality for previews
```bash
manim -ql instead of -qh
```

### Getting Help

- Check the [Manim Community Docs](https://docs.manim.community/)
- Join the [Manim Discord](https://discord.gg/manim)
- Open an issue on GitHub

## Contributing

Contributions are welcome! Areas for improvement:

- Additional actor styles
- More gesture animations
- Advanced lip-sync integration
- SVG asset library
- Additional example scenes
- Performance optimizations

## Roadmap

- [ ] Audio synchronization with TTS
- [ ] AI-generated gestures from scripts
- [ ] Rigged skeletal animation system
- [ ] Web-based actor customization tool
- [ ] Plugin system for extensions
- [ ] Multi-language subtitle support

## License

MIT License - see LICENSE file for details

## Credits

Built on top of the amazing [Manim Community Edition](https://www.manim.community/), originally created by Grant Sanderson ([3Blue1Brown](https://www.3blue1brown.com/)).

## Citation

If you use this project in your work, please cite:

```bibtex
@software{manim_actor_generator,
  title = {Manim Actor Video Generator},
  author = {Manim Actor Team},
  year = {2025},
  url = {https://github.com/Yash-Kavaiya/manim-video-generator-actor}
}
```

## Examples Gallery

### Math Tutorial
Create engaging math lessons with step-by-step explanations.

### Multi-Actor Dialogue
Simulate classroom conversations between teachers and students.

### Problem Solving
Show thought processes with thinking animations and eureka moments.

## Getting Started in 5 Minutes

```bash
# 1. Install
pip install manim
git clone https://github.com/Yash-Kavaiya/manim-video-generator-actor.git
cd manim-video-generator-actor

# 2. Run example
python generate.py --scene ActorIntroduction --quality low --preview

# 3. Customize (edit examples/quick_start.py)
manim -pql examples/quick_start.py QuickStart

# 4. Create your own scene!
```

## Support

If you find this project helpful, consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 📝 Contributing examples

---

**Made with ❤️ for the Manim community**