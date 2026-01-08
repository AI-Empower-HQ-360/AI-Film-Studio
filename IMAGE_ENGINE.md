# Image Creation Engine

The Image Creation Engine is a comprehensive system for generating Hollywood-level AI film images with character and location consistency.

## Overview

This engine handles:
- **Keyframe generation** for each shot
- **Character consistency** across shots
- **Location consistency** with time/weather variants
- **Style-aware prompting** (cinematic, anime, noir, etc.)
- **Multi-model routing** (SDXL, DALL-E, Leonardo.ai, etc.)

## Architecture

```
Script → Scene Graph → Shot Planner → Image Creation Engine → Video Engine → Composition
```

### Core Components

1. **Prompt Builder** (`src/services/prompt_builder.py`)
   - Generates rich prompts from shot metadata
   - Incorporates character, location, style, and camera details
   - Template-based prompt construction

2. **Model Router** (`src/services/model_router.py`)
   - Routes requests to appropriate AI models
   - Style-based model selection
   - Fallback chain for reliability
   - Supports: SDXL, DALL-E, Leonardo.ai, Stable Diffusion

3. **Character Consistency** (`src/services/character_consistency.py`)
   - Maintains character appearance across shots
   - Embedding/LoRA support
   - Reference image injection
   - Seed locking

4. **Location Consistency** (`src/services/location_consistency.py`)
   - Keeps backgrounds coherent
   - Time of day and weather variants
   - Location templates and embeddings

5. **Image Engine** (`src/services/image_engine.py`)
   - Main orchestrator
   - Coordinates all components
   - Batch processing support
   - Generation validation

6. **Image Generator Worker** (`pipeline/image_generator.py`)
   - Asynchronous job processing
   - Queue management
   - Output handling

## Data Models

Located in `src/models/`:

- **Character** (`character.py`) - Character definitions with visual attributes
- **Location** (`location.py`) - Location definitions with environment data
- **Shot** (`shot.py`) - Shot metadata with composition details
- **Asset** (`asset.py`) - Generated media assets

## Usage Examples

### Basic Shot Generation

```python
from src.models.shot import Shot
from src.models.character import Character
from src.models.location import Location
from src.services.image_engine import ImageEngine

# Create models
shot = Shot(
    scene_id="scene_001",
    shot_number=1,
    shot_type="close-up",
    description="Character walking through forest",
    style="cinematic",
    lighting="golden-hour",
    mood="peaceful"
)

character = Character(
    name="Radha",
    description="Divine character",
    appearance={
        "hair": "long black hair",
        "eyes": "dark brown eyes"
    },
    attire={
        "style": "traditional Indian",
        "colors": ["red", "gold"]
    }
)

location = Location(
    name="Vrindavan Forest",
    description="Sacred forest with flower fields",
    location_type="exterior",
    time_of_day="dusk"
)

# Generate image
engine = ImageEngine()
request = engine.generate_shot_image(
    shot=shot,
    characters=[character],
    location=location
)

print(request["parameters"]["prompt"])
```

### Using the Worker

```python
import asyncio
from pipeline.image_generator import ImageGeneratorWorker

async def generate_images():
    worker = ImageGeneratorWorker()
    
    # Add jobs
    job_id = await worker.add_job(
        shot=shot,
        characters=[character],
        location=location,
        priority=1
    )
    
    # Process queue
    await worker.process_queue()
    
    # Check status
    status = worker.get_queue_status()
    print(status)

asyncio.run(generate_images())
```

### Batch Processing

```python
# Process multiple shots
shots = [shot1, shot2, shot3]
characters_map = {"char_001": character1, "char_002": character2}
locations_map = {"loc_001": location1}

requests = engine.process_shot_batch(
    shots=shots,
    characters_map=characters_map,
    locations_map=locations_map
)
```

## Configuration

Set environment variables in `.env`:

```bash
# API Keys
STABILITY_API_KEY=your_stability_key
OPENAI_API_KEY=your_openai_key
LEONARDO_API_KEY=your_leonardo_key

# Default Settings
DEFAULT_MODEL_PROVIDER=sdxl
DEFAULT_GENERATION_STEPS=50
DEFAULT_CFG_SCALE=7.5

# Image Settings
IMAGE_DEFAULT_WIDTH=1024
IMAGE_DEFAULT_HEIGHT=576
```

## Prompt Templates

Located in `pipeline/prompts/templates.py`:

- Shot type templates (wide, close-up, etc.)
- Style templates (cinematic, anime, etc.)
- Lighting templates (golden-hour, dramatic, etc.)
- Camera angle templates
- Mood templates
- Character action templates
- Location type templates

## Model Clients

Located in `services/model_clients/`:

- `base_client.py` - Base client interface
- `sdxl_client.py` - Stable Diffusion XL
- `dalle_client.py` - DALL-E
- `leonardo_client.py` - Leonardo.ai

Add new clients by extending `BaseModelClient`.

## Testing

Run tests:

```bash
# All tests
pytest tests/

# Image engine tests only
pytest tests/test_image_engine.py -v

# Specific test
pytest tests/test_image_engine.py::TestImageEngine::test_generate_shot_image -v
```

## Integration with Film Pipeline

The Image Creation Engine integrates into the full pipeline:

1. **Script Processing** → Generates scene structure
2. **Scene Graph** → Defines relationships
3. **Shot Planner** → Creates shot metadata
4. **Image Creation Engine** → Generates keyframes (YOU ARE HERE)
5. **Video Engine** → Animates keyframes
6. **Audio Engine** → Adds voice/music
7. **Composition** → Final MP4

## Next Steps

To integrate with actual AI providers:

1. Add API keys to environment
2. Implement actual API calls in model clients
3. Add image storage (S3, etc.)
4. Set up database for asset tracking
5. Configure webhook callbacks for async generation

## Contributing

When adding features:

1. Add models to `src/models/`
2. Add services to `src/services/`
3. Add tests to `tests/`
4. Update this README
5. Run all tests before committing

## Support

For issues or questions, see the main repository README or open an issue.
