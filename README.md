# AI Film Studio

End-to-end AI Film Studio: script → scenes → shots → video → MP4

## 🎬 Vision

Transform written scripts into complete video productions using artificial intelligence. This project aims to democratize film production by automating the creative and technical processes involved in bringing stories to visual life.

## 🌟 Features (Planned)

- **📝 Script Parsing**: Support for multiple screenplay formats (Fountain, FDX, plain text)
- **🎭 Scene Breakdown**: Intelligent scene decomposition with visual element extraction
- **📸 Shot Planning**: Automated camera angle and movement planning
- **🎨 Frame Generation**: AI-powered image generation for each shot
- **🎥 Video Assembly**: Seamless frame-to-video conversion with transitions
- **🔊 Audio Integration**: Voice synthesis and background music (future)
- **💾 Multiple Formats**: Export to MP4, WebM, and other video formats

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- FFmpeg installed on your system
- API keys for AI services (OpenAI, Stable Diffusion, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### Basic Usage

```bash
# Generate a video from a script
python -m ai_film_studio generate script.txt --output video.mp4

# Interactive mode
python -m ai_film_studio interactive

# Generate only frames
python -m ai_film_studio frames script.txt --output-dir ./frames
```

## 📁 Project Structure

```
AI-Film-Studio/
├── src/
│   ├── ai_film_studio/
│   │   ├── __init__.py
│   │   ├── script_parser.py      # Parse screenplay formats
│   │   ├── scene_analyzer.py     # Break down scenes
│   │   ├── shot_planner.py       # Plan camera shots
│   │   ├── frame_generator.py    # Generate images
│   │   ├── video_assembler.py    # Create video
│   │   └── pipeline.py            # Orchestrate workflow
├── tests/
│   ├── test_script_parser.py
│   ├── test_scene_analyzer.py
│   └── ...
├── examples/
│   ├── short_film.fountain
│   ├── commercial.txt
│   └── outputs/
├── docs/
│   ├── user_guide.md
│   ├── api_reference.md
│   └── tutorials/
├── requirements.txt
├── pyproject.toml
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── LICENSE
└── .env.example
```

## 🛠️ Technology Stack

- **Python 3.10+**: Core programming language
- **OpenAI GPT-4**: Script analysis and scene understanding
- **Stable Diffusion**: Image generation for frames
- **FFmpeg**: Video processing and assembly
- **MoviePy**: Python video editing
- **Click**: CLI framework
- **Rich**: Beautiful terminal output
- **PyTest**: Testing framework

## 📋 Development Status

This project is currently in the **planning phase**. See [ROADMAP.md](ROADMAP.md) for detailed development timeline.

### Current Phase: Foundation
- [x] Repository setup
- [x] License and documentation
- [x] Development roadmap
- [ ] Project structure creation
- [ ] Dependency setup
- [ ] Basic configuration system

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📖 Improve documentation
- 🔧 Submit pull requests
- 🎨 Share generated content
- 💬 Join discussions

## 📖 Documentation

- [Roadmap](ROADMAP.md) - Development timeline and features
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [User Guide](docs/user_guide.md) - How to use the tool
- [API Reference](docs/api_reference.md) - Code documentation

## 🎯 Use Cases

- **Independent Filmmakers**: Quickly visualize scripts and storyboards
- **Content Creators**: Generate social media videos from text
- **Educators**: Create educational videos and animations
- **Marketing Teams**: Produce commercial concepts rapidly
- **Writers**: Visualize scenes while writing
- **Game Developers**: Generate cutscene previews

## ⚠️ Limitations

- AI-generated content may require human review and editing
- Quality depends on input script detail and AI model capabilities
- Processing time varies based on video length and complexity
- Costs associated with AI API usage
- Character consistency across scenes is challenging

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Stability AI for Stable Diffusion
- The open-source community for tools and libraries

## 📞 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues)
- **Discussions**: [Join the conversation](https://github.com/AI-Empower-HQ-360/AI-Film-Studio/discussions)

## 🗺️ Roadmap Highlights

1. **Phase 1 (Weeks 1-2)**: Project foundation and structure
2. **Phase 2 (Weeks 3-6)**: Core components (parsing, scene breakdown, frame generation)
3. **Phase 3 (Weeks 7-8)**: Pipeline integration and optimization
4. **Phase 4 (Weeks 9-10)**: Testing, documentation, and polish
5. **Phase 5 (Week 11+)**: Advanced features (audio, web UI, collaboration)

See [ROADMAP.md](ROADMAP.md) for complete details.

---

⭐ **Star this repository** if you find it interesting!

🔔 **Watch this repository** to stay updated on development progress!
