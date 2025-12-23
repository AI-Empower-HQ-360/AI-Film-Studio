# Getting Started with AI Film Studio

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio
```

### Step 2: Set Up Python Environment

We recommend using Python 3.10 or higher.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install the package in development mode
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Step 4: Configure API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=sk-...
STABILITY_API_KEY=sk-...
ELEVENLABS_API_KEY=...
```

Or use the setup command:
```bash
ai-film-studio setup
```

## Basic Usage

### Generate a Video

```bash
ai-film-studio generate examples/short_film.txt --output my_film.mp4
```

### Generate Only Frames

```bash
ai-film-studio frames examples/short_film.txt --output-dir ./my_frames
```

### Analyze a Script

```bash
ai-film-studio analyze examples/short_film.txt
```

### Specify Visual Style

```bash
ai-film-studio generate script.txt --output video.mp4 --style cartoon
```

Available styles:
- `realistic` (default)
- `cartoon`
- `anime`
- `cinematic`
- `noir`

## Command-Line Options

### Generate Command

```bash
ai-film-studio generate [OPTIONS] SCRIPT_PATH
```

Options:
- `--output, -o`: Output video file path (default: output.mp4)
- `--style, -s`: Visual style (default: realistic)
- `--config, -c`: Custom configuration file path

### Frames Command

```bash
ai-film-studio frames [OPTIONS] SCRIPT_PATH
```

Options:
- `--output-dir, -o`: Output directory for frames (default: ./frames)
- `--style, -s`: Visual style
- `--config, -c`: Configuration file path

### Analyze Command

```bash
ai-film-studio analyze [OPTIONS] SCRIPT_PATH
```

Options:
- `--config, -c`: Configuration file path

## Configuration

### Configuration File

Create a YAML configuration file:

```yaml
api_keys:
  openai: sk-your-key
  stability: sk-your-key
  elevenlabs: your-key

output_dir: ./output
cache_dir: ./cache

models:
  text_model: gpt-4
  image_model: stable-diffusion-xl
  voice_model: eleven_monolingual_v1

video:
  fps: 24
  resolution: 1920x1080
  format: mp4
  codec: libx264
```

Use it with:
```bash
ai-film-studio generate script.txt --config config.yaml
```

### Environment Variables

You can set these environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `STABILITY_API_KEY`: Your Stability AI API key
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `OUTPUT_DIR`: Default output directory
- `CACHE_DIR`: Cache directory for generated content

## Writing Scripts

### Supported Formats

- Plain text (.txt)
- Fountain screenplay format (.fountain) [coming soon]
- Final Draft XML (.fdx) [coming soon]

### Script Structure

A good script for AI Film Studio should include:

1. **Scene headings**: Clearly mark scene changes
2. **Visual descriptions**: Describe what should be seen
3. **Character actions**: Describe movements and expressions
4. **Dialogue**: What characters say (optional)

Example:
```
INT. COFFEE SHOP - DAY

A cozy coffee shop with warm lighting. EMMA sits at a table
with a laptop, looking thoughtful.

EMMA
I need to finish this today.

She types rapidly on the keyboard.
```

### Tips for Better Results

1. **Be specific**: Include details about lighting, atmosphere, colors
2. **One scene at a time**: Break your script into clear scenes
3. **Describe visually**: Focus on what can be seen, not just told
4. **Keep it simple**: Complex scenes with many elements are harder to generate
5. **Consistent characters**: Describe characters the same way throughout

## Troubleshooting

### Common Issues

**Error: "API key not found"**
- Make sure you've set up your `.env` file or configuration
- Check that API keys are valid and not expired

**Error: "Script file not found"**
- Verify the file path is correct
- Use absolute paths if relative paths don't work

**Generation takes too long**
- Large scripts take longer to process
- Consider generating frames first to preview
- Check your API rate limits

**Poor quality output**
- Try different visual styles
- Refine your script descriptions
- Ensure good lighting descriptions in scenes

## Next Steps

- Explore example scripts in `examples/`
- Read the [API Reference](api_reference.md)
- Check the [Roadmap](../ROADMAP.md) for upcoming features
- Join discussions on GitHub

## Getting Help

- Check [GitHub Issues](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)
- Read the [FAQ](faq.md)
- Join [Discussions](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/discussions)
