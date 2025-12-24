# AI-Film-Studio

End-to-end AI Film Studio: script → scenes → shots → video → MP4

## 🎬 Fully Automated Workflow

The AI Film Studio provides a complete automated pipeline that transforms scripts into finished films without human intervention.

### Features

- ✅ **Automated script parsing** - Breaks scripts into scenes and shots automatically
- ✅ **Intelligent task orchestration** - Manages dependencies and parallelization
- ✅ **Background workers** - Process tasks autonomously with retry logic
- ✅ **Progress tracking** - Real-time status updates for every job
- ✅ **Cost estimation** - Upfront pricing before job execution
- ✅ **Error handling** - Automatic retries and dead-letter queue for failures
- ✅ **RESTful API** - Simple HTTP API for job submission and monitoring
- ✅ **Scalable architecture** - Ready for distributed deployment

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Submit a script (in another terminal)
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "script": "SCENE 1: INT. ROOM - DAY\nSHOT 1: Wide - 5s\nA person enters",
    "title": "My First Film"
  }'
```

### Run the Demo

```bash
python examples/demo_automation.py
```

This will demonstrate the complete end-to-end automation workflow.

### Run Tests

```bash
pytest tests/
```

All 22 tests validate the automation workflow, API endpoints, and worker processing.

### Documentation

See [docs/AUTOMATION_WORKFLOW.md](docs/AUTOMATION_WORKFLOW.md) for complete documentation on:
- Architecture overview
- Component details
- API reference
- Script format
- Error handling
- Cost estimation

### Architecture

```
User → Script → API → Orchestrator → Queue → Workers → Storage → Final MP4
                  ↓
            Validation, Cost Estimation, Task Graph
```

The system is fully automated from script submission to final video delivery.
