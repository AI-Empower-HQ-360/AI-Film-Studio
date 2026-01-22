# Cline AI Extension Setup Guide

## What is Cline?

Cline is an AI coding assistant extension for VS Code that helps you write, debug, and understand code using AI. It's similar to GitHub Copilot but with a focus on conversational AI assistance.

## Installation Steps

### Step 1: Install Cline Extension

1. **Open VS Code**
   - Launch Visual Studio Code

2. **Open Extensions View**
   - Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)
   - Or click the Extensions icon in the sidebar (square icon with 4 squares)

3. **Search for Cline**
   - Type "Cline" in the search box
   - Look for "Cline" by **Anysphere** or **cline-ai**

4. **Install**
   - Click the "Install" button
   - Wait for installation to complete

### Step 2: Get API Key

Cline requires an API key from one of these providers:

#### Option A: OpenAI (Recommended)
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Important:** Save it immediately - you won't see it again!

#### Option B: Anthropic (Claude)
1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

#### Option C: Other Providers
- Cline may support other providers - check the extension documentation

### Step 3: Configure Cline

1. **Open Settings**
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac)
   - Or go to File → Preferences → Settings

2. **Search for Cline**
   - Type "Cline" in the settings search box

3. **Enter API Key**
   - Find "Cline: API Key" setting
   - Paste your API key
   - Or use the command palette method below

### Alternative: Configure via Command Palette

1. **Open Command Palette**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)

2. **Configure Cline**
   - Type "Cline: Configure" or "Cline: Set API Key"
   - Select the command
   - Enter your API key when prompted

### Step 4: Verify Connection

1. **Open Cline Chat**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Cline: Open Chat"
   - Press Enter

2. **Test Connection**
   - Type a simple message like: "Hello, can you help me?"
   - If Cline responds, you're connected! ✅
   - If you see an error, check your API key

## Using Cline

### Opening Cline Chat

**Method 1: Command Palette**
- Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
- Type "Cline: Open Chat"
- Press Enter

**Method 2: Sidebar Icon**
- Look for the Cline icon in the VS Code sidebar
- Click it to open the chat panel

**Method 3: Keyboard Shortcut**
- Check if Cline has a default keyboard shortcut
- Or set one in: File → Preferences → Keyboard Shortcuts

### Basic Usage

1. **Ask Questions**
   ```
   "How does this function work?"
   "Explain this code"
   "What does this error mean?"
   ```

2. **Get Code Help**
   ```
   "Write a function to validate email addresses"
   "Fix this bug: [paste code]"
   "Refactor this code to be more efficient"
   ```

3. **Run Tests**
   ```
   "Run all tests in the project"
   "Fix the failing test in test_character_engine.py"
   ```

4. **Generate Code**
   ```
   "Create a new API endpoint for user authentication"
   "Write unit tests for the CharacterEngine class"
   ```

## Troubleshooting

### Issue: "API Key not found" or "Invalid API Key"

**Solution:**
1. Check that you've entered the API key correctly
2. Make sure there are no extra spaces
3. Verify the API key is still valid (not expired/revoked)
4. Try regenerating the API key from your provider

### Issue: "Rate limit exceeded"

**Solution:**
1. You've used up your API quota
2. Wait a bit and try again
3. Consider upgrading your API plan
4. Check your usage at the provider's dashboard

### Issue: Cline not responding

**Solution:**
1. Check your internet connection
2. Verify the API key is correct
3. Check VS Code output panel for errors:
   - View → Output
   - Select "Cline" from the dropdown
4. Restart VS Code
5. Reinstall the Cline extension

### Issue: Can't find Cline extension

**Solution:**
1. Make sure you're searching for "Cline" (not "Cline AI" or variations)
2. Check if the extension is compatible with your VS Code version
3. Try searching for "Anysphere" (the publisher)
4. Check VS Code marketplace: https://marketplace.visualstudio.com/

## Configuration Options

### Common Settings

Access via: `Ctrl+,` → Search "Cline"

- **Cline: API Key** - Your API key
- **Cline: Model** - Which AI model to use (e.g., gpt-4, claude-3)
- **Cline: Max Tokens** - Maximum response length
- **Cline: Temperature** - Creativity level (0-1)

### Environment Variables (Alternative)

You can also set the API key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:CLINE_API_KEY = "your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set CLINE_API_KEY=your-api-key-here
```

**Mac/Linux:**
```bash
export CLINE_API_KEY="your-api-key-here"
```

## Quick Start Example

1. **Install Cline** (if not already installed)
2. **Set API Key** via Command Palette: `Ctrl+Shift+P` → "Cline: Configure"
3. **Open Chat**: `Ctrl+Shift+P` → "Cline: Open Chat"
4. **Try this prompt:**
   ```
   "Can you help me understand the CharacterEngine class in this project?"
   ```

## Cost Considerations

- **OpenAI**: Pay-per-use, typically $0.01-0.10 per request
- **Anthropic**: Pay-per-use, similar pricing
- **Free Tier**: Some providers offer limited free usage
- **Monitor Usage**: Check your API dashboard regularly

## Security Best Practices

1. **Never commit API keys to Git**
   - Use environment variables or VS Code settings
   - Add `.env` to `.gitignore` if using environment files

2. **Use separate keys for development/production**
   - Different keys for different environments

3. **Rotate keys regularly**
   - Change API keys periodically for security

4. **Set usage limits**
   - Configure spending limits in your API provider dashboard

## Alternative: GitHub Copilot

If Cline doesn't work for you, consider:
- **GitHub Copilot**: Built into VS Code, requires GitHub subscription
- **Codeium**: Free alternative with similar features
- **Tabnine**: Another AI coding assistant

## Need More Help?

- **Cline Documentation**: Check the extension's GitHub repository
- **VS Code Extension Marketplace**: https://marketplace.visualstudio.com/
- **Cline Issues**: Report problems on the extension's GitHub issues page

---

**Quick Checklist:**
- [ ] VS Code installed
- [ ] Cline extension installed
- [ ] API key obtained (OpenAI or Anthropic)
- [ ] API key configured in VS Code
- [ ] Cline chat opens successfully
- [ ] Can send messages and get responses

Once all checked, you're ready to use Cline! 🚀
