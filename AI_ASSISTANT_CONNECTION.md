# AI Assistant — Connected to AI Film Studio

**Status:** ✅ AI Assistant operates in **AI Film Studio** project context.

---

## ✅ Connection Setup

The AI assistant (Cursor AI / Auto) is configured to:

1. **Use AI Film Studio as the workspace** — All file operations and terminal commands run in this project.
2. **Respect project structure** — Backend (`src/`), frontend (`frontend/`), infra (`infrastructure/`), tests (`tests/`).
3. **Follow the 8-engine architecture** — Character, Writing, Pre-Production, Production Management, Production Layer, Post-Production, Marketing, Enterprise Platform.

---

## 📍 Project Root

```
C:\Users\ctrpr\Projects\AI-Film-Studio
```

**Verify connection:** Open Cursor/VS Code with this folder as the workspace.

- **File → Open Folder →** `C:\Users\ctrpr\Projects\AI-Film-Studio`
- Or: `code C:\Users\ctrpr\Projects\AI-Film-Studio`

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.cursorrules` | Tells the AI to always use AI Film Studio as context |
| `.vscode/settings.json` | Editor and project settings |

---

## ✅ How to Ensure AI Is "Connected"

### 1. Open the correct workspace
- Open **AI Film Studio** (not youtube-video-summar or another project).
- Folder name in the title bar should be **AI-Film-Studio**.

### 2. Start a chat in this project
- With AI Film Studio as the active workspace, start a new AI chat.
- The assistant will use `.cursorrules` and this project’s files.

### 3. Verify when unsure
You can say:
- *"Are you connected to AI Film Studio?"*
- *"Confirm you're using AI Film Studio."*

The assistant should confirm and run commands from `C:\Users\ctrpr\Projects\AI-Film-Studio`.

---

## 🚀 Quick Checks

```powershell
# Run from AI Film Studio root
cd C:\Users\ctrpr\Projects\AI-Film-Studio
git status
python -m pytest tests/unit -q --tb=no -x 2>$null | Select-Object -First 5
```

If these run without path errors, you’re in the right project.

---

## 📂 Key Directories

| Path | Purpose |
|------|---------|
| `src/` | Backend API, engines, services |
| `src/engines/` | Character, Writing, Pre-Production, etc. |
| `frontend/` | Next.js app |
| `tests/` | pytest and frontend tests |
| `infrastructure/aws-cdk/` | AWS CDK stacks |
| `docs/` | Blueprints and architecture |

---

## 🔗 Related Docs

- **Blueprint:** `docs/INVESTOR_DEVELOPER_MASTER_BLUEPRINT.md`
- **How to use AI:** `HOW_TO_USE_AI_ASSISTANT.md`
- **AI assistants setup:** `AI_CODING_ASSISTANTS_SETUP.md`

---

**You’re connected.** The AI assistant uses **AI Film Studio** as the primary project for all work.
