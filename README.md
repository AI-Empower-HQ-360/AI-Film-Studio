# AI-Film-Studio

End-to-end AI Film Studio: script → scenes → shots → video → MP4

## Overview

AI Film Studio is a Python-based pipeline for creating films using AI. It transforms scripts into finished video content through an automated production pipeline.

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from ai_film_studio import FilmPipeline

# Initialize the pipeline
pipeline = FilmPipeline()

# Run the pipeline with a script
output = pipeline.run("Your script here", output_name="my_film")
```

## Project Structure

```
AI-Film-Studio/
├── ai_film_studio/          # Main package
│   ├── __init__.py          # Package initialization
│   ├── pipeline.py          # Main orchestration pipeline
│   ├── script/              # Script parsing and generation
│   │   ├── __init__.py
│   │   ├── parser.py        # Parse scripts into scenes
│   │   └── generator.py     # AI script generation
│   ├── scenes/              # Scene analysis and breakdown
│   │   ├── __init__.py
│   │   ├── analyzer.py      # Analyze scene requirements
│   │   └── breakdown.py     # Break scenes into shots
│   ├── shots/               # Shot generation and composition
│   │   ├── __init__.py
│   │   ├── generator.py     # Generate visual shots
│   │   └── compositor.py    # Compose shots with effects
│   ├── video/               # Video assembly and processing
│   │   ├── __init__.py
│   │   ├── assembler.py     # Assemble shots into video
│   │   └── processor.py     # Video processing and effects
│   ├── output/              # Final export and output
│   │   ├── __init__.py
│   │   └── exporter.py      # Export in various formats
│   └── utils/               # Utilities and helpers
│       ├── __init__.py
│       ├── config.py        # Configuration management
│       └── logger.py        # Logging utilities
├── config/                  # Configuration files
│   └── default.json         # Default configuration
├── docs/                    # Documentation
│   └── README.md            # Documentation overview
├── examples/                # Example scripts
│   └── basic_pipeline.py    # Basic usage example
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_pipeline.py     # Pipeline tests
│   ├── test_script.py       # Script module tests
│   └── test_utils.py        # Utility tests
├── pyproject.toml           # Project configuration
├── LICENSE                  # MIT License
└── README.md                # This file
```

## Pipeline Stages

1. **Script** - Parse or generate film scripts
2. **Scenes** - Analyze scripts and break them into scenes  
3. **Shots** - Generate individual shots using AI
4. **Video** - Assemble shots into a complete video
5. **Output** - Export the final film in various formats (MP4, MOV, etc.)

## Testing

```bash
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.
