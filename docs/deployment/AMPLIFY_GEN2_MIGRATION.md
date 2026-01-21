# Amplify Gen 2 Migration Guide

## ✅ What's New

You've been upgraded to **AWS Amplify Gen 2**! Here's what changed:

### Key Improvements

1. **Type-Safe Configuration** - All backend config in TypeScript
2. **Better DX** - Code-first instead of YAML
3. **Local Sandbox** - Test auth & data locally
4. **GraphQL API** - Auto-generated with type safety
5. **CDK Integration** - Full AWS CDK support built-in

## 📁 New Structure

```
amplify/                     # Gen 2 backend (NEW)
├── backend.ts              # Main config
├── auth/resource.ts        # Authentication
├── data/resource.ts        # Data schema
├── package.json
└── tsconfig.json

frontend/src/lib/
├── amplify-config.ts       # Amplify initialization (NEW)
├── amplify-data.ts         # Type-safe data client (NEW)
└── api.ts                  # Your existing REST API (keep for backend)
```

## 🚀 Getting Started

### 1. Install Amplify Dependencies

```bash
cd amplify
npm install
```

### 2. Start Local Sandbox

```bash
npm run sandbox
```

This creates a local cloud environment with:
- Cognito user pool (authentication)
- AppSync GraphQL API (data)
- DynamoDB tables

### 3. Generate Outputs

After sandbox or deployment:
```bash
npx ampx generate outputs --app-id d2cj7uuldg6ksa --branch main
```

This creates `amplify_outputs.json` with your API config.

### 4. Update Your Frontend

Import at the root of your app (e.g., `app/layout.tsx`):

```typescript
import '@/lib/amplify-config';
```

Use the data client:

```typescript
import { createProject, listProjects } from '@/lib/amplify-data';

// Create a project
const project = await createProject({
  title: 'My Film',
  script: 'Once upon a time...',
  settings: { duration: 60 }
});

// List projects
const projects = await listProjects();
```

Use authentication:

```typescript
import { AmplifyAuthProvider } from '@/components/AmplifyAuthProvider';

export default function RootLayout({ children }) {
  return (
    <AmplifyAuthProvider>
      {children}
    </AmplifyAuthProvider>
  );
}
```

## 🔄 Migration Path

### Keep Both Systems (Recommended)

1. **Amplify Gen 2** → Frontend hosting + Auth + GraphQL API
2. **Your FastAPI Backend** → AI services (video, voice, etc.)

The `api.ts` file still works for your Python backend!

```typescript
// Use Amplify for projects/users
import { createProject } from '@/lib/amplify-data';

// Use REST API for AI processing
import { api } from '@/lib/api';
const job = await api.submitJob(projectId);
```

## 📊 Feature Comparison

| Feature | Gen 1 (Current) | Gen 2 (New) |
|---------|----------------|-------------|
| Hosting | ✅ (keep using) | ✅ |
| Config | YAML | TypeScript |
| Type Safety | ❌ | ✅ |
| Local Dev | Limited | Full sandbox |
| GraphQL API | Manual setup | Auto-generated |
| Auth | Cognito (manual) | Built-in |

## 🎯 Deployment Options

### Option A: Keep Gen 1 Hosting + Add Gen 2 Backend

```bash
# Your current hosting works
# App: https://main.d2cj7uuldg6ksa.amplifyapp.com

# Add Gen 2 backend
cd amplify
npm run sandbox  # For testing
npx ampx generate outputs --app-id d2cj7uuldg6ksa --branch main
```

### Option B: Full Gen 2 Migration

Convert hosting to Gen 2 (requires some manual setup).

## 🔗 External API Integration

Your FastAPI backend is separate - Amplify Gen 2 doesn't replace it!

**Architecture:**
```
User → Amplify Hosting (Frontend)
     → Amplify Gen 2 (Auth, User Data, Projects)
     → Your FastAPI (AI Processing: video, voice, lipsync)
```

## 📝 Next Steps

1. ✅ Review generated files in `amplify/`
2. ✅ Install dependencies: `cd amplify && npm install`
3. ✅ Test sandbox: `npm run sandbox`
4. ✅ Update frontend to use Amplify auth
5. ✅ Keep existing FastAPI for AI services

## 📚 Resources

- [Gen 2 Docs](https://docs.amplify.aws/gen2/)
- [Data Modeling](https://docs.amplify.aws/gen2/build-a-backend/data/)
- [Authentication](https://docs.amplify.aws/gen2/build-a-backend/auth/)
- [Migration Guide](https://docs.amplify.aws/gen2/deploy-and-host/fullstack-branching/migration/)

---

**Questions?** Check `amplify/README.md` or the official docs!
