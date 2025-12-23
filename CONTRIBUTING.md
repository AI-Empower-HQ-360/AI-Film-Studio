# Contributing to AI Film Studio Hub

Thank you for your interest in contributing to AI Film Studio Hub! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/AI-Film-Studio.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages
7. Push and create a pull request

## 🏗️ Project Structure

- `backend/` - FastAPI backend service
- `worker/` - Python GPU worker pipeline
- `frontend/` - Next.js frontend application
- `docs/` - Documentation (if added)

## 💻 Development Setup

### Option 1: Docker (Recommended)
```bash
./start.sh
```

### Option 2: Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

**Worker:**
```bash
cd worker
pip install -r requirements.txt
cp .env.example .env
celery -A celery_app worker --loglevel=info
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused

### TypeScript/React
- Use functional components with hooks
- Follow Airbnb style guide
- Use meaningful variable names
- Add comments for complex logic

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run lint
npm run build
```

### Worker
```bash
cd worker
# Add tests and run with pytest
```

## 📚 Documentation

- Update README.md for significant changes
- Add docstrings to new functions
- Update API documentation if changing endpoints
- Include examples in comments

## 🐛 Bug Reports

When reporting bugs, include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, Node version)
- Screenshots if applicable

## ✨ Feature Requests

When requesting features:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any mockups or examples

## 🔄 Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation as needed
3. Add tests for new features
4. Ensure all tests pass
5. Update CHANGELOG.md (if exists)
6. Request review from maintainers

### PR Title Format
- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `refactor: Refactor code`
- `test: Add tests`
- `chore: Update dependencies`

## 🎯 Areas for Contribution

### High Priority
- [ ] Add comprehensive test coverage
- [ ] Improve error handling
- [ ] Add monitoring and logging
- [ ] Optimize GPU memory usage
- [ ] Add more AI models

### Medium Priority
- [ ] Add user dashboard
- [ ] Implement project templates
- [ ] Add video editing features
- [ ] Improve UI/UX
- [ ] Add analytics

### Low Priority
- [ ] Add social sharing
- [ ] Multi-language support
- [ ] Theme customization
- [ ] Export to different formats

## 🔒 Security

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Report security vulnerabilities privately
- Follow security best practices

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Communication

- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Pull Requests for code contributions

## 🙏 Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

Thank you for contributing to AI Film Studio Hub! 🎬
