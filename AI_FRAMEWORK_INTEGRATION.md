# AI Framework Integration - All 14 Engines

## Overview

All 14 AI engines in the AI Film Studio now have integrated AI framework support, providing unified access to OpenAI, Anthropic, Stability AI, and ElevenLabs services.

## Unified AI Framework

**Location**: `src/services/ai_framework.py`

The `AIFramework` class provides a centralized interface for all AI services:

- **Text Generation**: For Writing, Dialogues, Screenplay engines
- **Image Generation**: For Image Creation, Character, Marketing engines
- **Voice Synthesis**: For Voice Modulation, Character engines
- **Content Analysis**: For Director, Pre-Production engines
- **Structured Data Extraction**: For Pre-Production, Production Management
- **Video Generation**: For Production Layer, Marketing engines

## Engine Integration Status

### ✅ 1. Writing Engine (`src/engines/writing_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Text generation for script creation
- **Provider**: OpenAI GPT-4 (default), Anthropic Claude (fallback)
- **Usage**: Enhanced `generate_script()` method uses AI framework for intelligent script generation

### ✅ 2. Character Engine (`src/engines/character_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Image generation, voice synthesis, character analysis
- **Provider**: Stability AI, OpenAI DALL-E, ElevenLabs
- **Usage**: Character creation, image generation, voice synthesis

### ✅ 3. Image Creation Engine (`src/engines/image_creation_engine.py`)
- **AI Framework**: Integrated (already had direct service integration, now uses unified framework)
- **Capabilities**: Comprehensive image generation for all age groups, genders, cultures, animals
- **Provider**: Stability AI, OpenAI DALL-E
- **Usage**: Enhanced prompt building, multi-parameter image generation

### ✅ 4. Director Engine (`src/engines/director_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Shot composition analysis, scene direction
- **Provider**: OpenAI GPT-4, Anthropic Claude
- **Usage**: AI-powered shot planning and scene direction

### ✅ 5. Screenplay Engine (`src/engines/screenplay_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Screenplay formatting, dialogue generation
- **Provider**: OpenAI GPT-4, Anthropic Claude
- **Usage**: AI-assisted screenplay creation and formatting

### ✅ 6. Voice Modulation Engine (`src/engines/voice_modulation_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Voice synthesis with age-group and gender-specific modulation
- **Provider**: ElevenLabs
- **Usage**: Voice synthesis with pitch, speed, emotion, accent control

### ✅ 7. Movement Engine (`src/engines/movement_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Movement and animation analysis
- **Provider**: OpenAI GPT-4 (for movement analysis)
- **Usage**: AI-powered movement and gesture generation

### ✅ 8. Dialogues Engine (`src/engines/dialogues_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Dialogue generation, conversation management
- **Provider**: OpenAI GPT-4, Anthropic Claude
- **Usage**: AI-generated dialogues with emotion and style control

### ✅ 9. Pre-Production Engine (`src/engines/preproduction_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Script breakdown, budget estimation, schedule analysis
- **Provider**: OpenAI GPT-4, Anthropic Claude
- **Usage**: AI-powered script analysis and production planning

### ✅ 10. Production Management (`src/engines/production_management.py`)
- **AI Framework**: Integrated
- **Capabilities**: Project analysis, asset management, timeline optimization
- **Provider**: OpenAI GPT-4, Anthropic Claude
- **Usage**: AI-assisted production management and optimization

### ✅ 11. Production Layer (`src/engines/production_layer.py`)
- **AI Framework**: Integrated
- **Capabilities**: Video generation, shot matching, gap filling
- **Provider**: Stability AI (video generation)
- **Usage**: AI-powered video generation and production assistance

### ✅ 12. Post-Production Engine (`src/engines/postproduction_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Audio mixing, video composition, subtitle generation
- **Provider**: Multiple (voice, music, video services)
- **Usage**: AI-powered post-production workflows

### ✅ 13. Marketing Engine (`src/engines/marketing_engine.py`)
- **AI Framework**: Integrated
- **Capabilities**: Trailer generation, poster creation, thumbnail generation
- **Provider**: Stability AI, OpenAI DALL-E
- **Usage**: AI-generated marketing assets

### ✅ 14. Enterprise Platform (`src/engines/enterprise_platform.py`)
- **AI Framework**: Not required (platform management layer)
- **Note**: Enterprise platform manages multi-tenancy and usage tracking, doesn't require direct AI integration

## AI Framework Features

### 1. Text Generation
```python
# For Writing, Dialogues, Screenplay engines
text = await ai_framework.generate_text(
    prompt="Generate a script...",
    provider="openai",
    model="gpt-4",
    max_tokens=4000,
    temperature=0.7
)
```

### 2. Image Generation
```python
# For Image Creation, Character, Marketing engines
image = await ai_framework.generate_image(
    prompt="A character image...",
    provider="stability",
    width=1024,
    height=1024
)
```

### 3. Voice Synthesis
```python
# For Voice Modulation, Character engines
audio = await ai_framework.synthesize_voice(
    text="Hello world",
    voice_id="voice_123",
    provider="elevenlabs",
    emotion="happy",
    speed=1.0
)
```

### 4. Content Analysis
```python
# For Director, Pre-Production engines
analysis = await ai_framework.analyze_content(
    content="Scene description...",
    analysis_type="shot_composition",
    provider="openai"
)
```

### 5. Structured Data Extraction
```python
# For Pre-Production, Production Management
data = await ai_framework.extract_structured_data(
    content="Script content...",
    schema={"scenes": "list", "characters": "list"},
    provider="openai"
)
```

### 6. Video Generation
```python
# For Production Layer, Marketing engines
video = await ai_framework.generate_video(
    prompt="Video description...",
    provider="stability",
    duration=5
)
```

## Environment Variables

The AI framework automatically initializes services based on available API keys:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
STABILITY_AI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
```

## Usage Pattern

All engines follow the same pattern:

```python
class MyEngine:
    def __init__(self):
        # Initialize AI Framework
        try:
            from src.services.ai_framework import get_ai_framework
            self.ai_framework = get_ai_framework()
        except ImportError:
            self.ai_framework = None
            logger.warning("AI Framework not available, using fallback")
    
    def my_method(self):
        if self.ai_framework:
            # Use AI framework
            result = await self.ai_framework.generate_text(...)
        else:
            # Fallback logic
            result = "fallback"
```

## Benefits

1. **Unified Interface**: All engines use the same AI framework interface
2. **Provider Flexibility**: Easy to switch between OpenAI, Anthropic, Stability AI, ElevenLabs
3. **Fallback Support**: Graceful degradation when AI services are unavailable
4. **Centralized Configuration**: Single point of configuration for all AI services
5. **Testing Support**: Easy to mock AI framework for testing
6. **Scalability**: Framework handles async operations and error handling

## Next Steps

1. **Enhanced Integration**: Each engine can now leverage AI framework methods in their core functionality
2. **Provider Selection**: Engines can intelligently select providers based on task requirements
3. **Cost Optimization**: Framework can route requests to cost-effective providers
4. **Caching**: Framework can implement caching for repeated requests
5. **Rate Limiting**: Centralized rate limiting and retry logic

## Testing

All engines maintain backward compatibility with existing tests. The AI framework gracefully handles missing API keys and provides fallback behavior for testing environments.
