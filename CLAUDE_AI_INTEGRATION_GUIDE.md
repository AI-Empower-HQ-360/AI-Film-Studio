# Claude AI (Anthropic) Integration Guide

**How to Use Claude AI with AI Film Studio**

---

## 🎯 Overview

This guide explains how to integrate **Claude AI (Anthropic)** into your AI Film Studio project. Claude AI can be used for:

- **Script Writing & Story Generation**
- **Character Development & Analysis**
- **Dialogue Generation**
- **Scene Analysis**
- **Content Review & Improvement**

---

## 📋 Prerequisites

### 1. **Get Anthropic API Key**

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **"Create Key"**
5. Copy your API key (starts with `sk-ant-...`)

### 2. **Install Anthropic SDK**

```bash
pip install anthropic
```

Or add to `requirements.txt`:
```
anthropic>=0.18.0
```

---

## 🔧 Configuration

### **Environment Variables**

Add to your `.env` file:

```env
# Anthropic Claude API
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### **Available Claude Models:**

- `claude-3-5-sonnet-20241022` - Latest, most capable (recommended)
- `claude-3-opus-20240229` - Most powerful
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-haiku-20240307` - Fastest, cost-effective

---

## 💻 Integration Options

### **Option 1: Use Me (AI Assistant) in Cursor**

I'm already integrated! You can:

1. **Ask me questions** about your codebase
2. **Request code changes** - I'll make them directly
3. **Get explanations** - I'll search and explain code
4. **Debug issues** - I'll help troubleshoot
5. **Write new features** - I'll implement them

**Example:**
```
"Can you add Claude AI integration to the Writing Engine?"
"Show me how to use the Character Engine"
"Fix the ESLint errors in frontend"
```

### **Option 2: Integrate Claude API in Your Code**

I can create a Claude AI service for your backend. Here's how:

---

## 🚀 Implementation

### **Step 1: Create Claude Service**

I'll create `src/services/ai/anthropic_service.py` with:
- Message completion
- Streaming support
- Vision capabilities (for scene analysis)
- Error handling
- Rate limiting

### **Step 2: Integrate with Engines**

Claude can be used in:
- **Writing Engine** - Script generation, dialogue
- **Character Engine** - Character analysis, backstory
- **Pre-Production Engine** - Script breakdown analysis

### **Step 3: API Endpoints**

Add endpoints like:
- `POST /api/v1/ai/claude/complete` - Text completion
- `POST /api/v1/ai/claude/stream` - Streaming responses
- `POST /api/v1/ai/claude/analyze-image` - Vision analysis

---

## 📝 Usage Examples

### **In Python (Backend):**

```python
from src.services.ai.anthropic_service import AnthropicService

# Initialize
claude = AnthropicService()

# Complete text
result = await claude.complete(
    messages=[
        {"role": "user", "content": "Write a dramatic scene..."}
    ],
    model="claude-3-5-sonnet-20241022"
)

# Stream response
async for chunk in claude.stream_complete(
    messages=[{"role": "user", "content": "Generate dialogue..."}]
):
    print(chunk, end="")
```

### **In TypeScript (Frontend):**

```typescript
// Call backend API
const response = await fetch('/api/v1/ai/claude/complete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{ role: 'user', content: 'Generate script...' }],
    model: 'claude-3-5-sonnet-20241022'
  })
});

const data = await response.json();
console.log(data.content);
```

---

## 🎨 Use Cases in AI Film Studio

### **1. Script Writing**
```python
# Generate screenplay from prompt
script = await writing_engine.generate_script(
    prompt="A sci-fi thriller about AI",
    use_claude=True  # Use Claude instead of GPT-4
)
```

### **2. Character Development**
```python
# Analyze character personality
analysis = await character_engine.analyze_personality(
    character=character,
    use_claude=True
)
```

### **3. Dialogue Generation**
```python
# Generate character dialogue
dialogue = await writing_engine.generate_dialogue(
    character=character,
    scene_context=scene,
    use_claude=True
)
```

---

## 🔐 Security

- ✅ **Never commit API keys** to Git
- ✅ **Use environment variables**
- ✅ **Store in AWS Secrets Manager** (production)
- ✅ **Rotate keys regularly**

---

## 📊 Cost Management

Claude API Pricing (as of 2024):
- **Claude 3.5 Sonnet:** ~$3/1M input tokens, $15/1M output tokens
- **Claude 3 Opus:** ~$15/1M input tokens, $75/1M output tokens
- **Claude 3 Haiku:** ~$0.25/1M input tokens, $1.25/1M output tokens

**Recommendations:**
- Use **Haiku** for simple tasks
- Use **Sonnet** for most production work
- Use **Opus** for complex analysis

---

## 🆚 Claude vs OpenAI

| Feature | Claude AI | OpenAI GPT-4 |
|---------|-----------|--------------|
| **Context Window** | 200K tokens | 128K tokens |
| **Vision** | ✅ Excellent | ✅ Good |
| **Code** | ✅ Good | ✅ Excellent |
| **Writing** | ✅ Excellent | ✅ Excellent |
| **Cost** | Moderate | Higher |
| **Speed** | Fast | Moderate |

**Best Use Cases for Claude:**
- Long-form content generation
- Creative writing
- Analysis of long documents
- Vision-based scene analysis

---

## 🛠️ Next Steps

**Would you like me to:**

1. ✅ **Create the Claude AI service** (`anthropic_service.py`)
2. ✅ **Integrate it with your engines** (Writing, Character, etc.)
3. ✅ **Add API endpoints** for Claude
4. ✅ **Update environment configuration**
5. ✅ **Add usage examples**

**Just ask me:**
- "Create Claude AI service for the backend"
- "Integrate Claude with the Writing Engine"
- "Add Claude API endpoints"

---

## 📚 Resources

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [Anthropic Console](https://console.anthropic.com/)
- [Claude Models](https://docs.anthropic.com/claude/docs/models-overview)

---

**Ready to integrate Claude AI?** Just tell me what you'd like me to implement! 🚀
