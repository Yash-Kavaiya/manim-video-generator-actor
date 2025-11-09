# Use Apify Python base image
FROM apify/actor-python:3.11

# Install system dependencies required for Manim
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/app

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Apify SDK
RUN pip install --no-cache-dir apify

# Copy all project files
COPY . ./

# Create output directory for videos
RUN mkdir -p /usr/src/app/storage/key_value_stores/default

# Set environment variables
ENV MANIM_CACHE_DIR=/tmp/manim_cache
ENV PYTHONUNBUFFERED=1

# Support both MCP server mode and regular actor mode
# MCP server mode is activated when APIFY_META_ORIGIN=STANDBY
# Regular actor mode is used otherwise
CMD ["/bin/sh", "-c", "if [ \"$APIFY_META_ORIGIN\" = \"STANDBY\" ]; then python -u -m src; else python -u main.py; fi"]
