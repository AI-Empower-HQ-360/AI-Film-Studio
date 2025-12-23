# Contributing to AI Film Studio

Thank you for your interest in contributing to AI Film Studio! This document provides guidelines and instructions for contributing to the project.

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/AI-Film-Studio.git
cd AI-Film-Studio

# Add upstream remote
git remote add upstream https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install pre-commit hooks (once available)
# pre-commit install
```

### 3. Create a Branch

```bash
# Update your fork with upstream changes
git fetch upstream
git checkout main
git merge upstream/main

# Create a new branch for your feature
git checkout -b feature/your-feature-name
```

## 📝 Making Changes

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Write descriptive variable and function names
- Keep functions small and focused
- Add docstrings to all public functions and classes

### Example:

```python
def parse_screenplay(script_path: str, format: str = "fountain") -> dict:
    """
    Parse a screenplay file and extract scene information.
    
    Args:
        script_path: Path to the screenplay file
        format: Format of the screenplay (fountain, fdx, txt)
        
    Returns:
        Dictionary containing parsed scenes and metadata
        
    Raises:
        FileNotFoundError: If script_path does not exist
        ValueError: If format is not supported
    """
    # Implementation here
    pass
```

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(script-parser): add support for Fountain format

Implement parser for Fountain screenplay format with scene detection
and character extraction.

Closes #123
```

```
fix(video-assembler): correct frame rate calculation

Fixed issue where frame rate was incorrectly calculated for variable
FPS inputs, causing video sync issues.

Fixes #456
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_film_studio --cov-report=html

# Run specific test file
pytest tests/test_script_parser.py

# Run specific test
pytest tests/test_script_parser.py::test_parse_fountain_format
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

```python
def test_parse_fountain_format():
    """Test parsing a Fountain format screenplay."""
    # Arrange
    script_path = "tests/fixtures/sample.fountain"
    
    # Act
    result = parse_screenplay(script_path, format="fountain")
    
    # Assert
    assert len(result["scenes"]) > 0
    assert "characters" in result
    assert result["format"] == "fountain"
```

## 📚 Documentation

### Docstrings

Use Google-style docstrings:

```python
def generate_frames(scene: Scene, style: str = "realistic") -> List[Image]:
    """
    Generate image frames for a scene.
    
    Args:
        scene: Scene object containing description and metadata
        style: Visual style for generation (realistic, cartoon, anime, etc.)
        
    Returns:
        List of generated PIL Image objects
        
    Raises:
        APIError: If image generation API fails
        
    Example:
        >>> scene = Scene(description="A sunny beach")
        >>> frames = generate_frames(scene, style="realistic")
        >>> len(frames)
        10
    """
    pass
```

### README and Docs

- Update README.md if adding new features
- Add examples for new functionality
- Update ROADMAP.md if changing development plans
- Create tutorials in docs/ for complex features

## 🔍 Review Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with main branch

### Submitting a Pull Request

1. Push your branch to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a pull request on GitHub
   - Use a descriptive title
   - Reference related issues
   - Describe changes in detail
   - Add screenshots/videos if applicable

3. Wait for review
   - Address reviewer feedback
   - Make requested changes
   - Keep discussion professional

### PR Template

```markdown
## Description
Brief description of changes

## Related Issues
Fixes #123
Related to #456

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

## 🐛 Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Verify it's reproducible in the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. Use input file '...'
3. See error

**Expected behavior**
What you expected to happen

**Actual behavior**
What actually happened

**Screenshots/Logs**
Add relevant output or logs

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- AI Film Studio version: [e.g., 0.1.0]

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Suggesting Features

1. Check existing feature requests
2. Open a new issue with "Feature Request" label
3. Describe the feature and use case
4. Discuss implementation approach

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it could be implemented

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## 🎯 Areas for Contribution

### High Priority
- Core pipeline components (Phase 2)
- Testing infrastructure
- Documentation and examples
- Performance optimization

### Good First Issues
- Documentation improvements
- Example scripts
- Bug fixes
- Test coverage improvements

### Advanced Contributions
- AI model integration
- Video processing algorithms
- Web interface development
- Cloud deployment setup

## 📞 Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: Open an issue with bug template
- **Features**: Open an issue with feature request template
- **Chat**: Join our community discussions

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

Thank you for contributing to AI Film Studio! 🎬
