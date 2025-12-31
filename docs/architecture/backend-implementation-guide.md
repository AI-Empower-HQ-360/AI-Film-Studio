# Backend Implementation Guide - AI Film Studio

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Service Implementation Examples](#2-service-implementation-examples)
3. [Database Setup & Migrations](#3-database-setup--migrations)
4. [API Route Implementations](#4-api-route-implementations)
5. [Worker Process Implementation](#5-worker-process-implementation)
6. [Testing Strategy](#6-testing-strategy)
7. [Deployment Configuration](#7-deployment-configuration)

---

## 1. Project Setup

### Project Structure

```
ai-film-studio-backend/
├── services/
│   ├── user-service/
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   ├── middleware/
│   │   │   └── server.js
│   │   ├── package.json
│   │   └── Dockerfile
│   ├── project-service/
│   ├── credit-service/
│   ├── ai-job-service/
│   ├── youtube-service/
│   └── admin-service/
├── shared/
│   ├── database/
│   ├── utils/
│   └── constants/
├── workers/
│   ├── video-worker/
│   ├── audio-worker/
│   └── lipsync-worker/
├── docker-compose.yml
└── README.md
```

### Environment Variables (.env)

```bash
# Server Configuration
NODE_ENV=development
PORT=3001
SERVICE_NAME=user-service

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_film_studio
DB_USER=postgres
DB_PASSWORD=your_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=24h

# AWS
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
```

---

## 2. Service Implementation Examples

### Express.js Service Template

```javascript
// src/server.js
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Service running on port ${PORT}`);
});
```

### Controller Pattern

```javascript
// controllers/user-controller.js
class UserController {
  async register(req, res, next) {
    try {
      const { email, password, name } = req.body;
      // Implementation
      res.status(201).json({ user, token });
    } catch (error) {
      next(error);
    }
  }

  async login(req, res, next) {
    try {
      const { email, password } = req.body;
      // Implementation
      res.json({ user, token });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new UserController();
```

---

## 3. Database Setup & Migrations

### Database Connection

```javascript
// database/index.js
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
});

module.exports = { pool };
```

---

## 4. API Route Implementations

### User Routes

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/user-controller');
const { authenticate } = require('../middleware/auth');

router.post('/register', userController.register);
router.post('/login', userController.login);
router.get('/profile', authenticate, userController.getProfile);

module.exports = router;
```

---

## 5. Worker Process Implementation

### BullMQ Worker

```javascript
// workers/video-worker.js
const { Worker } = require('bullmq');
const videoService = require('../services/video-generation');

const worker = new Worker('video-generation', async (job) => {
  const { projectId, prompt } = job.data;
  
  // Process video generation
  const result = await videoService.generateVideo(prompt);
  
  return result;
}, { connection: redisConnection });

module.exports = worker;
```

---

## 6. Testing Strategy

### Unit Tests

```javascript
// tests/user-service.test.js
describe('UserService', () => {
  it('should create a new user', async () => {
    const user = await userService.create({
      email: 'test@example.com',
      password: 'password123'
    });
    
    expect(user).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });
});
```

---

## 7. Deployment Configuration

### Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3001

CMD ["node", "src/server.js"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  user-service:
    build: ./services/user-service
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - DB_HOST=postgres
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ai_film_studio
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-31  
**Status:** Approved
