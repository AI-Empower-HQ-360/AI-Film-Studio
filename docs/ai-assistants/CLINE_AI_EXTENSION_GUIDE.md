# Cline AI Extension - Testing & Usage Guide

**AI Coding Assistant Extension for Cursor/VS Code**

---

## 🎯 What is Cline?

**Cline** is an AI coding assistant extension that provides:
- **Code completion** and suggestions
- **Code generation** from natural language
- **Code explanation** and documentation
- **Refactoring** assistance
- **Bug fixing** and debugging help

---

## 📦 Installation

### **In Cursor/VS Code:**

1. Open Extensions panel (`Ctrl+Shift+X` or `Cmd+Shift+X`)
2. Search for **"Cline"** or **"AI Cline"**
3. Click **Install**
4. Restart Cursor/VS Code

### **Or via Command Line:**

```bash
code --install-extension your-cline-extension-id
```

---

## ⚙️ Configuration

### **1. API Key Setup**

Cline typically uses:
- **OpenAI API** (GPT-4, GPT-3.5)
- **Anthropic Claude API**
- **Or other AI providers**

**Configure in Settings:**
```json
{
  "cline.apiKey": "your-api-key-here",
  "cline.model": "gpt-4",
  "cline.provider": "openai"
}
```

### **2. Workspace Settings**

Create `.vscode/settings.json`:

```json
{
  "cline.enabled": true,
  "cline.autoSuggest": true,
  "cline.maxTokens": 2000,
  "cline.temperature": 0.7,
  "cline.language": "en"
}
```

---

## 🧪 Testing Cline Extension

### **Test 1: Code Completion**

1. Open any Python/TypeScript file
2. Start typing a comment or function
3. Cline should suggest completions
4. Press `Tab` or `Enter` to accept

**Example:**
```python
# Write a function to create a character
# Cline should suggest: def create_character(...)
```

### **Test 2: Code Generation**

1. Type a comment describing what you want
2. Press `Ctrl+Space` (or Cline's shortcut)
3. Cline generates code based on your description

**Example:**
```python
# Generate a function to validate email addresses
# Cline generates: def validate_email(email: str) -> bool: ...
```

### **Test 3: Code Explanation**

1. Select code block
2. Right-click → **"Explain Code"** (or Cline command)
3. Cline explains what the code does

### **Test 4: Refactoring**

1. Select code
2. Right-click → **"Refactor"** (or Cline command)
3. Cline suggests improvements

---

## 🔍 Testing Checklist

### **Basic Functionality:**
- [ ] Extension installs without errors
- [ ] API key is accepted
- [ ] Code completion works
- [ ] Code generation works
- [ ] Code explanation works
- [ ] Refactoring suggestions appear

### **Integration Tests:**
- [ ] Works with Python files
- [ ] Works with TypeScript/JavaScript files
- [ ] Works with React/Next.js components
- [ ] Understands project context
- [ ] Respects code style (ESLint, Black, etc.)

### **Performance Tests:**
- [ ] Response time < 5 seconds
- [ ] No memory leaks
- [ ] Doesn't slow down editor
- [ ] Handles large files

### **Error Handling:**
- [ ] Graceful API errors
- [ ] Network timeout handling
- [ ] Invalid API key handling
- [ ] Rate limit handling

---

## 🛠️ Testing Commands

### **Test Cline in Your Project:**

```bash
# 1. Test code generation
# Open a file and ask Cline to generate a function

# 2. Test code completion
# Type a comment and see if Cline suggests code

# 3. Test code explanation
# Select code and ask Cline to explain it

# 4. Test refactoring
# Select code and ask Cline to refactor it
```

---

## 📝 Example Test Scenarios

### **Scenario 1: Generate Test Function**

**Input:**
```python
# Write a test for the Character Engine create_character method
```

**Expected:** Cline generates pytest test function

### **Scenario 2: Explain Complex Code**

**Input:** Select this code:
```python
async def generate_character_voice(self, request, job_id):
    # Complex implementation
```

**Expected:** Cline explains the function's purpose and flow

### **Scenario 3: Refactor Code**

**Input:** Select code with code smells

**Expected:** Cline suggests cleaner alternatives

---

## 🐛 Troubleshooting

### **Issue: Cline Not Responding**

**Solutions:**
1. Check API key is set correctly
2. Verify internet connection
3. Check API quota/limits
4. Restart Cursor/VS Code
5. Check extension logs

### **Issue: Wrong Code Suggestions**

**Solutions:**
1. Provide more context in comments
2. Check model selection (GPT-4 vs GPT-3.5)
3. Adjust temperature setting
4. Enable project context awareness

### **Issue: Slow Performance**

**Solutions:**
1. Use faster model (GPT-3.5 instead of GPT-4)
2. Reduce max tokens
3. Disable auto-suggestions
4. Check network latency

---

## 🔧 Advanced Configuration

### **Custom Prompts:**

Some Cline extensions allow custom system prompts:

```json
{
  "cline.systemPrompt": "You are a Python expert specializing in FastAPI and AI/ML. Always write clean, tested code following PEP 8."
}
```

### **Context Awareness:**

Enable project context:
```json
{
  "cline.useProjectContext": true,
  "cline.maxContextFiles": 10
}
```

---

## 📊 Testing Results Template

```markdown
## Cline Extension Test Results

**Date:** 2026-01-21
**Version:** [Cline version]
**Model:** GPT-4 / Claude

### Test Results:
- ✅ Code Completion: Working
- ✅ Code Generation: Working
- ✅ Code Explanation: Working
- ⚠️ Refactoring: Needs improvement
- ✅ Performance: Good (< 3s response)

### Issues Found:
- [List any issues]

### Recommendations:
- [Suggestions for improvement]
```

---

## 🚀 Best Practices

### **1. Use Clear Prompts**
✅ Good: "Create a FastAPI endpoint to create a character"
❌ Vague: "Make an endpoint"

### **2. Provide Context**
✅ Good: "In the Character Engine, add a method to..."
❌ Less helpful: "Add a method"

### **3. Review Generated Code**
- Always review Cline's suggestions
- Test generated code
- Check for security issues
- Verify it follows your style guide

### **4. Iterate**
- Ask follow-up questions
- Request improvements
- Refine the generated code

---

## 📚 Resources

- **Cline Extension:** [VS Code Marketplace](https://marketplace.visualstudio.com/)
- **Documentation:** Check extension's GitHub/website
- **Support:** Extension's issue tracker

---

## ✅ Quick Test

**Try this now:**

1. Open `src/engines/writing_engine.py`
2. Add a comment: `# Generate a function to create a script from a prompt`
3. Press Cline's shortcut (usually `Ctrl+Space` or `Tab`)
4. See if Cline generates the function

**If it works:** ✅ Cline is configured correctly!

---

**Need help testing Cline?** Ask me:
- "Test Cline code generation in the Writing Engine"
- "Verify Cline understands the project structure"
- "Check if Cline respects ESLint rules"
