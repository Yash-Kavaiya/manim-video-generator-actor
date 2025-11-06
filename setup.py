"""
Setup script for Manim Actor Video Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="manim-actor-generator",
    version="1.0.0",
    author="Manim Actor Team",
    description="A modular actor system for creating animated characters in Manim videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yash-Kavaiya/manim-video-generator-actor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "manim>=0.18.0",
        "numpy>=1.21.0",
        "pillow>=9.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
        ],
        "audio": [
            "gTTS>=2.3.0",
            "pyttsx3>=2.90",
        ],
    },
    entry_points={
        "console_scripts": [
            "manim-actor=generate:main",
        ],
    },
)
