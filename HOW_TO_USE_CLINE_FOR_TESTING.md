# How to Use Cline AI for Testing

## Quick Start

### 1. Open Cline Chat in VS Code

**Method 1: Command Palette**
- Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (Mac)
- Type "Cline: Open Chat"
- Press Enter

**Method 2: Sidebar**
- Click the Cline icon in the VS Code sidebar
- Or use the keyboard shortcut (if configured)

### 2. Ask Cline to Run Tests

Here are example prompts you can use:

#### **Run All Tests**
```
Run all tests in the project
```

#### **Run Frontend Tests**
```
Run the frontend unit tests using npm test
```

#### **Run Backend Tests**
```
Run the backend tests using pytest
```

#### **Run E2E Tests**
```
Run the Playwright end-to-end tests
```

#### **Run Tests with Coverage**
```
Run tests with coverage report
```

#### **Fix Failing Tests**
```
The tests are failing. Can you analyze the test failures and fix them?
```

#### **Write New Tests**
```
Write unit tests for the CharacterEngine class
```

#### **Debug Test Issues**
```
The test in tests/unit/test_character_engine.py is failing. Help me debug it.
```

## Example Conversations

### Example 1: Running Frontend Tests

**You:**
```
Run the frontend tests in watch mode
```

**Cline will:**
- Execute: `cd frontend && npm test`
- Show test results in the terminal
- Help interpret any failures

### Example 2: Running Backend Tests

**You:**
```
Run pytest for the backend and show me the results
```

**Cline will:**
- Execute: `pytest tests/ -v`
- Display test output
- Highlight any failures

### Example 3: Fixing Test Failures

**You:**
```
The test test_create_character is failing. Can you fix it?
```

**Cline will:**
- Read the test file
- Read the source code being tested
- Identify the issue
- Propose fixes
- Apply the fix if you approve

### Example 4: Writing New Tests

**You:**
```
Write comprehensive tests for the WritingEngine class
```

**Cline will:**
- Analyze the `WritingEngine` class
- Understand its methods and functionality
- Generate test cases covering:
  - Happy paths
  - Edge cases
  - Error handling
- Create the test file with proper structure

## Available Test Commands

### Frontend (Next.js)
```bash
# Unit tests
npm test                    # Watch mode
npm run test:run           # Run once
npm run test:coverage      # With coverage
npm run test:ui            # UI mode

# E2E tests
npm run test:e2e           # Run Playwright tests
npm run test:e2e:ui        # Interactive UI
npm run test:e2e:production # Test deployed site
```

### Backend (Python)
```bash
# All tests
pytest                     # Run all tests
pytest -v                  # Verbose
pytest -q                  # Quiet

# Specific tests
pytest tests/unit/         # Unit tests only
pytest tests/integration/  # Integration tests
pytest tests/e2e/          # E2E tests

# With options
pytest --cov               # Coverage
pytest -x                  # Stop on first failure
pytest -k "test_name"      # Run specific test
```

## Tips for Better Results

### 1. Be Specific
❌ "Run tests"
✅ "Run the frontend unit tests in the frontend directory"

### 2. Provide Context
❌ "Fix this test"
✅ "The test `test_create_character` in `tests/unit/test_character_engine.py` is failing because it expects a method that doesn't exist"

### 3. Ask for Explanations
```
Can you explain why this test is failing?
```

### 4. Request Multiple Actions
```
Run all tests, show me the failures, and then fix them
```

### 5. Ask for Test Coverage
```
What parts of the codebase are not covered by tests?
```

## Advanced Usage

### Ask Cline to Analyze Test Coverage
```
Analyze test coverage and suggest areas that need more tests
```

### Ask Cline to Optimize Tests
```
The tests are running slowly. Can you optimize them?
```

### Ask Cline to Refactor Tests
```
Refactor these tests to follow best practices
```

### Ask Cline to Create Test Fixtures
```
Create reusable test fixtures for the character engine tests
```

## Troubleshooting

### Cline Not Responding?
1. Check if Cline extension is installed and enabled
2. Verify you have an API key configured (if required)
3. Check VS Code output panel for errors

### Tests Not Running?
1. Make sure you're in the correct directory
2. Verify dependencies are installed (`npm install` or `pip install -r requirements.txt`)
3. Check if test files exist

### Need Help with Test Syntax?
Ask Cline:
```
How do I write a test for async functions in pytest?
```

```
How do I mock an API call in a React component test?
```

## Quick Reference

| Task | Prompt |
|------|--------|
| Run all tests | "Run all tests" |
| Run frontend tests | "Run npm test in the frontend directory" |
| Run backend tests | "Run pytest tests/" |
| Run E2E tests | "Run Playwright E2E tests" |
| Fix failing test | "Fix the failing test in [file path]" |
| Write new test | "Write tests for [class/function name]" |
| Explain test failure | "Why is this test failing?" |
| Improve test coverage | "Suggest tests to improve coverage" |

## Example Workflow

1. **Start Development**
   ```
   I'm working on the CharacterEngine. Run the tests to see current status.
   ```

2. **See Failures**
   ```
   The test is failing. Can you explain why?
   ```

3. **Fix Issues**
   ```
   Fix the failing test by updating the implementation
   ```

4. **Verify Fix**
   ```
   Run the tests again to confirm the fix works
   ```

5. **Add Coverage**
   ```
   Write additional tests for edge cases
   ```

---

**Note:** Cline AI works best when you provide clear, specific instructions. The more context you give, the better Cline can help you!
