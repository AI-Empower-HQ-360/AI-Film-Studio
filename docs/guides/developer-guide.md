# Developer Guide - AI Film Studio

**Version:** 1.0  
**Last Updated:** 2025-12-31

---

## 🎯 Purpose

This guide provides comprehensive information for developers working on the AI Film Studio project. It covers project structure, coding standards, development workflows, and best practices.

---

## 📁 Project Structure

```
AI-Film-Studio/
├── docs/                          # Documentation
│   ├── MASTER_BLUEPRINT.md        # Complete system blueprint
│   ├── architecture/              # Architecture documents
│   │   ├── system-design.md       # System design details
│   │   └── visual-architecture-diagram.md
│   ├── requirements/              # Requirements documents
│   │   ├── FRD.md                 # Functional requirements
│   │   └── NFR.md                 # Non-functional requirements
│   ├── api/                       # API documentation
│   │   └── README.md              # API overview
│   ├── deployment/                # Deployment guides
│   │   └── local-setup.md         # Local development setup
│   └── guides/                    # Developer guides
│       └── developer-guide.md     # This file
│
├── backend/                       # Backend services (FastAPI/Python)
│   ├── src/                       # Source code
│   │   ├── api/                   # API routes
│   │   ├── config/                # Configuration
│   │   ├── services/              # Business logic
│   │   └── utils/                 # Utilities
│   ├── tests/                     # Unit and integration tests
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Container image
│
├── frontend/                      # Frontend application (Next.js)
│   ├── src/                       # Source code
│   │   ├── app/                   # Next.js App Router pages
│   │   ├── components/            # React components
│   │   ├── lib/                   # Utilities and helpers
│   │   ├── hooks/                 # Custom React hooks
│   │   └── styles/                # Global styles
│   ├── public/                    # Static assets
│   ├── package.json               # Dependencies
│   └── Dockerfile                 # Container image
│
├── worker/                        # AI processing workers
│   ├── src/                       # Source code
│   │   ├── pipelines/             # AI pipelines
│   │   ├── models/                # Model loaders
│   │   └── utils/                 # Utilities
│   ├── tests/                     # Worker tests
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Container image
│
├── infrastructure/                # Infrastructure as Code
│   ├── terraform/                 # Terraform modules
│   │   ├── environments/          # Environment configs
│   │   └── modules/               # Reusable modules
│   └── kubernetes/                # K8s manifests
│
├── scripts/                       # Utility scripts
│   ├── seed_data.py              # Database seeding
│   ├── migrate.sh                # Migration runner
│   └── deploy.sh                 # Deployment script
│
├── .github/                       # GitHub Actions
│   └── workflows/                 # CI/CD pipelines
│
├── docker-compose.yml             # Local development services
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
├── README.md                      # Project README
└── LICENSE                        # MIT License
```

---

## 💻 Development Environment

### **Recommended IDE**

- **VS Code** with extensions:
  - Python
  - Pylance
  - ESLint
  - Prettier
  - Docker
  - GitLens
  - Thunder Client (API testing)

### **Alternative IDEs**

- **PyCharm Professional** (for backend)
- **WebStorm** (for frontend)

---

## 🔧 Coding Standards

### **Python (Backend/Worker)**

**Style Guide:** PEP 8

```python
# Good
def calculate_credit_cost(duration_minutes: int) -> int:
    """
    Calculate credit cost based on video duration.
    
    Args:
        duration_minutes: Video duration in minutes (1-5)
    
    Returns:
        Number of credits required
    
    Raises:
        ValueError: If duration is invalid
    """
    if not 1 <= duration_minutes <= 5:
        raise ValueError("Duration must be between 1 and 5 minutes")
    
    return duration_minutes  # 1 credit per minute

# Bad
def calc_cost(d):
    return d
```

**Tools:**
- **Formatter:** Black (line length: 100)
- **Linter:** Ruff
- **Type Checker:** mypy
- **Import Sorter:** isort

**Configuration (.ruff.toml):**
```toml
line-length = 100
target-version = "py311"

[lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]
```

### **TypeScript/JavaScript (Frontend)**

**Style Guide:** Airbnb + Custom

```typescript
// Good
interface ProjectFormData {
  title: string;
  script: string;
  duration: number;
  voiceId: string;
}

const createProject = async (data: ProjectFormData): Promise<Project> => {
  try {
    const response = await api.post('/projects', data);
    return response.data;
  } catch (error) {
    console.error('Failed to create project:', error);
    throw error;
  }
};

// Bad
function createProject(d) {
  return api.post('/projects', d);
}
```

**Tools:**
- **Formatter:** Prettier
- **Linter:** ESLint
- **Type Checker:** TypeScript compiler

**Configuration (.eslintrc.json):**
```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```

---

## 🧪 Testing

### **Backend Testing**

**Framework:** pytest

```python
# tests/test_user_service.py
import pytest
from src.services.user_service import UserService

@pytest.fixture
def user_service():
    return UserService()

def test_create_user_success(user_service):
    """Test successful user creation."""
    user = user_service.create_user(
        email="test@example.com",
        password="SecurePassword123"
    )
    assert user.email == "test@example.com"
    assert user.id is not None

def test_create_user_duplicate_email(user_service):
    """Test creating user with duplicate email fails."""
    user_service.create_user(email="test@example.com", password="pass")
    
    with pytest.raises(ValueError, match="Email already exists"):
        user_service.create_user(email="test@example.com", password="pass")
```

**Run Tests:**
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/test_user_service.py::test_create_user_success

# Watch mode
pytest-watch
```

### **Frontend Testing**

**Frameworks:** Jest + React Testing Library

```typescript
// components/__tests__/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    
    fireEvent.click(screen.getByText('Click Me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button loading>Click Me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

**Run Tests:**
```bash
# All tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# E2E tests
npm run test:e2e
```

---

## 🔀 Git Workflow

### **Branch Strategy**

```
main (production)
  ├── develop (staging)
  │   ├── feature/user-authentication
  │   ├── feature/video-generation
  │   ├── bugfix/login-error
  │   └── hotfix/critical-bug
```

### **Branch Naming**

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates

**Examples:**
- `feature/youtube-integration`
- `bugfix/credit-deduction-error`
- `hotfix/database-connection-timeout`

### **Commit Messages**

Follow Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructuring
- `test` - Adding tests
- `chore` - Maintenance

**Examples:**
```
feat(auth): add Google OAuth integration

Implement Google OAuth 2.0 flow for user authentication.
- Add OAuth routes
- Update user model
- Add frontend OAuth button

Closes #123
```

```
fix(credits): prevent negative balance

Add validation to ensure credits cannot go below zero.

Fixes #456
```

### **Pull Request Process**

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   ```bash
   # Edit files
   git add .
   git commit -m "feat(scope): description"
   ```

3. **Push to Remote**
   ```bash
   git push origin feature/my-feature
   ```

4. **Create Pull Request**
   - Title: Clear, descriptive
   - Description: What, why, how
   - Link issues: "Closes #123"
   - Add reviewers
   - Add labels

5. **Code Review**
   - Address feedback
   - Push updates
   - Request re-review

6. **Merge**
   - Squash and merge (preferred)
   - Delete branch after merge

---

## 🚀 Development Workflow

### **Daily Workflow**

1. **Pull Latest Changes**
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Develop & Test**
   ```bash
   # Make changes
   npm run dev  # or python src/main.py
   
   # Run tests
   npm test  # or pytest
   
   # Lint code
   npm run lint  # or ruff check .
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push & Create PR**
   ```bash
   git push origin feature/my-feature
   # Create PR on GitHub
   ```

---

## 🐛 Debugging

### **Backend Debugging**

**Using VS Code:**
1. Set breakpoints in code
2. Press F5 or Run > Start Debugging
3. Step through code

**Using Print Statements:**
```python
import logging

logger = logging.getLogger(__name__)

def process_job(job_id: str):
    logger.debug(f"Processing job: {job_id}")
    # ... code ...
    logger.info(f"Job {job_id} completed successfully")
```

### **Frontend Debugging**

**Browser DevTools:**
1. Open Chrome DevTools (F12)
2. Sources tab > Set breakpoints
3. Step through code

**React DevTools:**
1. Install React DevTools extension
2. Inspect component tree
3. Check props and state

### **Network Debugging**

**Backend Logs:**
```bash
# View logs
docker-compose logs -f backend

# Filter logs
docker-compose logs -f backend | grep ERROR
```

**API Testing:**
- Use Thunder Client (VS Code)
- Use Postman
- Use curl:
  ```bash
  curl -X POST http://localhost:8000/api/v1/projects \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title": "Test", "script": "Test script"}'
  ```

---

## 📦 Dependency Management

### **Backend (Python)**

**Add Dependency:**
```bash
pip install package-name
pip freeze > requirements.txt
```

**Update Dependency:**
```bash
pip install --upgrade package-name
pip freeze > requirements.txt
```

### **Frontend (Node.js)**

**Add Dependency:**
```bash
npm install package-name
# or
yarn add package-name
```

**Update Dependency:**
```bash
npm update package-name
# or
yarn upgrade package-name
```

---

## 🔐 Security Best Practices

### **Environment Variables**

- **Never commit** `.env` files
- Use `.env.example` as template
- Store secrets in AWS Secrets Manager (production)

### **API Keys**

- Rotate keys regularly
- Use different keys for each environment
- Limit key permissions (principle of least privilege)

### **Input Validation**

```python
# Good
from pydantic import BaseModel, validator

class ProjectCreate(BaseModel):
    title: str
    script: str
    duration: int
    
    @validator('duration')
    def validate_duration(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Duration must be between 1 and 5 minutes')
        return v
```

### **SQL Injection Prevention**

```python
# Good (using ORM)
user = session.query(User).filter(User.email == email).first()

# Bad (raw SQL)
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

---

## 📊 Performance Optimization

### **Backend Optimization**

1. **Database Queries**
   - Use indexes
   - Avoid N+1 queries
   - Use pagination

2. **Caching**
   - Cache frequently accessed data in Redis
   - Set appropriate TTL

3. **Async Operations**
   - Use async/await for I/O operations
   - Use background tasks for long-running jobs

### **Frontend Optimization**

1. **Code Splitting**
   - Use dynamic imports
   - Lazy load components

2. **Image Optimization**
   - Use Next.js Image component
   - Compress images

3. **Bundle Size**
   - Analyze bundle with `npm run analyze`
   - Remove unused dependencies

---

## 📚 Resources

### **Official Documentation**

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/docs)
- [React](https://react.dev/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [AWS](https://docs.aws.amazon.com/)

### **Learning Resources**

- [Python Best Practices](https://docs.python-guide.org/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [React Patterns](https://reactpatterns.com/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)

### **Internal Documentation**

- [Master Blueprint](../MASTER_BLUEPRINT.md)
- [System Design](../architecture/system-design.md)
- [API Documentation](../api/README.md)
- [Local Setup](../deployment/local-setup.md)

---

## 🤝 Getting Help

### **Communication Channels**

- **Slack:** #ai-film-studio-dev
- **Email:** dev-team@ai-film-studio.com
- **GitHub Issues:** For bugs and feature requests

### **Who to Ask**

- **Backend:** @backend-team
- **Frontend:** @frontend-team
- **DevOps:** @devops-team
- **AI/ML:** @ml-team

---

## ✅ Checklist for New Developers

- [ ] Read [README.md](../../README.md)
- [ ] Read [Master Blueprint](../MASTER_BLUEPRINT.md)
- [ ] Complete [Local Setup](../deployment/local-setup.md)
- [ ] Join Slack channels
- [ ] Set up development environment
- [ ] Run backend locally
- [ ] Run frontend locally
- [ ] Run tests successfully
- [ ] Make first commit
- [ ] Create first pull request
- [ ] Review existing codebase

---

**💡 Pro Tip:** Keep this guide bookmarked and refer to it often!

---

**🎬 Happy Coding!**
