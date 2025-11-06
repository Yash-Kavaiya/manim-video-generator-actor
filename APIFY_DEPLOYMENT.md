# Apify Actor Deployment Guide

Complete guide for deploying the Manim Actor Video Generator as an Apify Actor.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Deployment Steps](#deployment-steps)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [API Usage](#api-usage)

## Overview

The Manim Actor Video Generator is packaged as an Apify Actor, allowing you to:
- Generate videos in the cloud without local setup
- Scale rendering across multiple compute units
- Access videos via API
- Schedule automated video generation
- Integrate with webhooks and other services

## Prerequisites

### Required

1. **Apify Account**
   - Sign up at [console.apify.com/sign-up](https://console.apify.com/sign-up)
   - Free tier includes compute credits

2. **Apify CLI**
   ```bash
   npm install -g apify-cli
   ```

3. **Git**
   - For version control and deployment

### Optional

- Node.js 16+ (for CLI)
- Docker (for local testing)

## Project Structure

```
manim-video-generator-actor/
├── .actor/                          # Apify configuration
│   ├── actor.json                   # Actor metadata
│   ├── INPUT_SCHEMA.json           # Input configuration schema
│   ├── input.json                  # Default input
│   └── input_examples/             # Example inputs
│       ├── math_lesson.json
│       ├── multi_actor_conversation.json
│       └── custom_scene.json
├── actors/                         # Actor system code
├── scenes/                         # Scene definitions
├── configs/                        # Configuration presets
├── main.py                         # Apify Actor entry point
├── Dockerfile                      # Docker configuration
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

## Deployment Steps

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Yash-Kavaiya/manim-video-generator-actor.git
cd manim-video-generator-actor

# Login to Apify
apify login
```

### Step 2: Test Locally (Optional)

```bash
# Initialize Apify storage
apify init

# Run with default input
apify run

# Run with custom input
apify run --input-file .actor/input_examples/math_lesson.json
```

### Step 3: Deploy to Apify

```bash
# Push to Apify platform
apify push

# The CLI will:
# 1. Build Docker image
# 2. Push to Apify registry
# 3. Create/update Actor
```

### Step 4: Configure Actor

1. Visit [Apify Console](https://console.apify.com/actors)
2. Find your deployed Actor
3. Configure:
   - **Name**: Manim Actor Video Generator
   - **Description**: Generate animated math videos
   - **Categories**: Video, Education, Entertainment
   - **README**: Auto-generated from README.md

### Step 5: Test Run

1. In Apify Console, click "Try it"
2. Use example input or customize
3. Click "Start"
4. Monitor logs and download video when complete

## Configuration

### Input Schema

The Actor accepts configuration via `INPUT_SCHEMA.json`. Key parameters:

#### Required Fields

```json
{
  "sceneType": "SimplePresentation",
  "videoQuality": "medium"
}
```

#### Common Configurations

**Quick Preview (Low Quality)**
```json
{
  "sceneType": "ActorIntroduction",
  "videoQuality": "low",
  "actorStyle": "stick_figure"
}
```

**High-Quality Tutorial**
```json
{
  "sceneType": "MathLesson",
  "videoQuality": "high",
  "actorStyle": "professional",
  "actorPreset": "teacher",
  "enableSubtitles": true,
  "fps": 60
}
```

**Multi-Actor Scene**
```json
{
  "sceneType": "MultiActorScene",
  "videoQuality": "medium",
  "multiActorMode": true,
  "actorStyle": "professional",
  "secondActorStyle": "cartoon",
  "actorColorScheme": "blue",
  "secondActorColorScheme": "orange"
}
```

**Custom Scene**
```json
{
  "sceneType": "CustomScene",
  "videoQuality": "medium",
  "customSceneConfig": {
    "title": "My Equation",
    "equation": "\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}",
    "dialogues": [
      {
        "text": "This is the Gaussian integral",
        "isMath": false,
        "duration": 3
      }
    ]
  },
  "customEquations": [
    "\\int_0^\\infty e^{-x^2} dx"
  ]
}
```

### Environment Variables

Set in Apify Console → Actor → Settings → Environment variables:

- `MANIM_CACHE_DIR`: Cache directory (default: `/tmp/manim_cache`)
- `PYTHONUNBUFFERED`: Enable unbuffered output (default: `1`)

### Compute Units

Estimated compute unit consumption:

| Quality | Duration | Compute Units* |
|---------|----------|----------------|
| Low     | 30s      | ~0.5-1.0      |
| Medium  | 30s      | ~1.0-2.0      |
| High    | 30s      | ~3.0-5.0      |
| Production | 30s   | ~8.0-15.0     |

*Approximate values; actual usage varies by scene complexity

## Testing

### Local Testing with Docker

```bash
# Build Docker image
docker build -t manim-actor .

# Run container
docker run -it \
  -v $(pwd)/storage:/usr/src/app/storage \
  -e APIFY_LOCAL_STORAGE_DIR=/usr/src/app/storage \
  manim-actor
```

### Testing with Apify CLI

```bash
# Test with different inputs
apify run --input '{"sceneType": "SimplePresentation", "videoQuality": "low"}'

# Test custom scene
apify run --input-file .actor/input_examples/custom_scene.json

# Debug mode
apify run --input '{"sceneType": "MathLesson", "debug": true}'
```

### Automated Testing

Create test script (`test_actor.sh`):

```bash
#!/bin/bash

echo "Testing basic scenes..."
for scene in "ActorIntroduction" "SimplePresentation" "MathLesson"; do
  echo "Testing $scene..."
  apify run --input "{\"sceneType\": \"$scene\", \"videoQuality\": \"low\"}"
done

echo "All tests complete!"
```

## Production Deployment

### Version Management

1. **Update Version**
   ```bash
   # Edit .actor/actor.json
   {
     "version": "1.1.0"
   }
   ```

2. **Tag Release**
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

3. **Deploy**
   ```bash
   apify push --version-number 1.1.0
   ```

### Performance Optimization

1. **Memory Settings**
   - Set in Actor Settings → Resources
   - Recommended: 4096 MB for medium quality, 8192 MB for high

2. **Timeout**
   - Recommended: 600 seconds (10 minutes)
   - Adjust based on video complexity

3. **Build Optimization**
   - Use Docker layer caching
   - Minimize image size with `.dockerignore`

### Monitoring

Enable monitoring in Apify Console:
- Set up alerts for failed runs
- Monitor compute unit usage
- Track video generation times

## Troubleshooting

### Common Issues

**1. LaTeX Errors**
```
Error: LaTeX compilation failed
```

**Solution**: Check equation syntax, ensure proper escaping:
```json
{"equation": "\\frac{df}{dx}"}  // Correct
{"equation": "\frac{df}{dx}"}   // Wrong
```

**2. Out of Memory**
```
Error: Container killed (OOM)
```

**Solution**:
- Increase memory allocation
- Reduce video quality
- Use simpler actor style

**3. Timeout**
```
Error: Actor execution timeout
```

**Solution**:
- Increase timeout setting
- Use lower quality for testing
- Simplify scene complexity

**4. Video Not Found**
```
Error: No video file found after generation
```

**Solution**: Check logs for Manim errors, validate input parameters

### Debug Mode

Enable debug mode for verbose logging:

```json
{
  "sceneType": "MathLesson",
  "debug": true
}
```

### Logs

Access logs:
1. Apify Console → Actor → Runs
2. Select run
3. View "Log" tab

## API Usage

### REST API

**Run Actor**
```bash
curl -X POST \
  https://api.apify.com/v2/acts/YOUR_USERNAME~manim-video-generator-actor/runs \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sceneType": "MathLesson",
    "videoQuality": "medium"
  }'
```

**Get Results**
```bash
curl https://api.apify.com/v2/acts/YOUR_USERNAME~manim-video-generator-actor/runs/LAST \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Download Video**
```bash
curl https://api.apify.com/v2/key-value-stores/{storeId}/records/{fileName} \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  --output video.mp4
```

### JavaScript SDK

```javascript
const { ApifyClient } = require('apify-client');

const client = new ApifyClient({
  token: 'YOUR_API_TOKEN',
});

// Run the Actor
const run = await client.actor('YOUR_USERNAME/manim-video-generator-actor').call({
  sceneType: 'MathLesson',
  videoQuality: 'high',
  actorStyle: 'professional',
});

// Get video URL
const dataset = await client.dataset(run.defaultDatasetId).listItems();
const videoUrl = dataset.items[0].videoUrl;

console.log(`Video URL: ${videoUrl}`);
```

### Python SDK

```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_API_TOKEN')

# Run the Actor
run = client.actor('YOUR_USERNAME/manim-video-generator-actor').call(
    run_input={
        'sceneType': 'MathLesson',
        'videoQuality': 'high',
        'actorStyle': 'professional'
    }
)

# Get results
dataset = client.dataset(run['defaultDatasetId'])
items = dataset.list_items().items

video_url = items[0]['videoUrl']
print(f'Video URL: {video_url}')
```

### Webhooks

Set up webhooks for automation:

1. **Actor Settings → Integration → Webhooks**
2. **Add webhook URL**
3. **Select events**: Run succeeded, Run failed
4. **Example payload**:

```json
{
  "actorId": "...",
  "actorRunId": "...",
  "eventType": "ACTOR.RUN.SUCCEEDED",
  "eventData": {
    "status": "SUCCEEDED",
    "defaultKeyValueStoreId": "...",
    "defaultDatasetId": "..."
  }
}
```

## Advanced Features

### Scheduled Runs

Create recurring video generation:

1. **Apify Console → Schedules → Create New**
2. **Configure cron expression**: `0 9 * * *` (daily at 9 AM)
3. **Select Actor and input**
4. **Save**

### Integrations

Connect with other services:

- **Make (Integromat)**: Automate workflows
- **Zapier**: Trigger on events
- **Custom webhooks**: Build custom integrations

## Support

- **Documentation**: [docs.apify.com](https://docs.apify.com/)
- **Community**: [discord.gg/jyEM2PRvMU](https://discord.gg/jyEM2PRvMU)
- **GitHub Issues**: [Project Issues](https://github.com/Yash-Kavaiya/manim-video-generator-actor/issues)

## License

MIT License - see LICENSE file for details.
