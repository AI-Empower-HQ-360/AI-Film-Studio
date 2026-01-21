# Amplify Gen 2 Configuration

This directory contains the AWS Amplify Gen 2 backend configuration for AI Film Studio.

## Structure

```
amplify/
├── backend.ts           # Main backend configuration
├── auth/
│   └── resource.ts      # Authentication setup
├── data/
│   └── resource.ts      # Data schema (DynamoDB + GraphQL API)
├── package.json         # Amplify dependencies
└── tsconfig.json        # TypeScript configuration
```

## Quick Start

### 1. Install Dependencies

```bash
cd amplify
npm install
```

### 2. Start Local Sandbox

```bash
npm run sandbox
```

This creates a local cloud environment for testing.

### 3. Deploy to Production

```bash
npx ampx generate outputs --branch main --app-id d2cj7uuldg6ksa
```

## Features

- **Type-safe configuration**: Full TypeScript support
- **Authentication**: Email/password with custom user attributes
- **Data modeling**: GraphQL API with DynamoDB backend
- **Authorization**: Owner-based and authenticated access
- **Sandbox**: Local cloud development environment

## Environment Variables

Amplify Gen 2 automatically generates `amplify_outputs.json` which contains:
- API endpoints
- Auth configuration
- GraphQL schema

Import in your frontend:
```typescript
import outputs from '@/amplify_outputs.json';
import { Amplify } from 'aws-amplify';

Amplify.configure(outputs);
```

## Key Differences from Gen 1

| Feature | Gen 1 | Gen 2 |
|---------|-------|-------|
| Configuration | YAML (amplify.yml) | TypeScript (backend.ts) |
| Type Safety | ❌ | ✅ |
| Local Testing | Limited | Full sandbox |
| Data Modeling | Schema.graphql | TypeScript DSL |
| CDK Support | Manual | Built-in |

## Learn More

- [Amplify Gen 2 Docs](https://docs.amplify.aws/gen2/)
- [Migration Guide](https://docs.amplify.aws/gen2/deploy-and-host/fullstack-branching/migration/)
