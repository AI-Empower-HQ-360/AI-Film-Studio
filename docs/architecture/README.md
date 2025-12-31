# Backend Architecture Documentation

This directory contains comprehensive documentation for the AI Film Studio backend architecture and implementation.

## 📚 Documentation Index

### 1. [Backend Tech Stack](./backend-tech-stack.md)
**Comprehensive overview of the Node.js-based backend technology stack**

- **Framework & Runtime**: Node.js 18.x, Express.js, NestJS
- **Database Layer**: PostgreSQL/MySQL, Redis, AWS S3
- **Microservices**: 6 independent services (User, Project, Credit, AI Job, YouTube, Admin)
- **Authentication**: JWT, OAuth 2.0, bcrypt encryption
- **AI Integration**: Video generation, voice synthesis, lip-sync, music generation
- **Queue Management**: BullMQ, RabbitMQ, AWS SQS
- **Monitoring**: Winston, Prometheus, Grafana, CloudWatch
- **Complete stack specifications and architecture diagrams**

### 2. [Backend Implementation Guide](./backend-implementation-guide.md)
**Practical implementation guide with code examples**

- **Project Structure**: Recommended folder organization for microservices
- **Service Templates**: Express.js and NestJS implementation patterns
- **Database Setup**: Connection pooling and migration scripts
- **API Routes**: Controller and service layer implementations
- **Worker Processes**: BullMQ worker examples for AI job processing
- **Testing Strategy**: Unit and integration test examples with Jest
- **Deployment**: Docker, Docker Compose, and Kubernetes configurations

### 3. [API Specification](./api-specification.md)
**Complete REST API documentation for all microservices**

#### User Service APIs
- `POST /users/register` - User registration
- `POST /users/login` - User authentication
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile

#### Project Service APIs
- `POST /projects/create` - Create new project
- `GET /projects` - List user projects
- `GET /projects/:id` - Get project details
- `POST /projects/:id/regenerate` - Regenerate project
- `DELETE /projects/:id` - Delete project

#### Credit / Subscription APIs
- `GET /credits/balance` - Get credit balance
- `POST /credits/topup` - Purchase credits
- `GET /plans` - List subscription plans

#### AI Job Service APIs
- `POST /ai/video-generate` - Generate video from text
- `POST /ai/audio-generate` - Generate voice/audio
- `POST /ai/lip-sync` - Apply lip-sync to video
- `POST /ai/music-generate` - Generate background music
- `GET /ai/jobs/:id/status` - Check job status

#### YouTube Service APIs
- `POST /youtube/upload` - Upload to YouTube
- `POST /youtube/playlist` - Create playlist
- `GET /youtube/videos` - List uploaded videos

#### Admin Service APIs
- `GET /admin/users` - List all users
- `GET /admin/analytics` - Platform analytics
- `POST /admin/users/:id/grant-credits` - Grant credits

### 4. [System Design](./system-design.md)
**Existing comprehensive system architecture document**

- High-level architecture diagrams
- Component specifications
- Network architecture
- Security architecture
- Scaling strategies
- Disaster recovery planning
- Cost breakdown analysis

## 🏗️ Architecture Overview

### Microservices Architecture

```
┌─────────────┐
│  API Gateway │
│  (Nginx/Kong)│
└──────┬───────┘
       │
       ├────┬────┬────┬────┬────┐
       │    │    │    │    │    │
       ▼    ▼    ▼    ▼    ▼    ▼
    ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐
    │USR││PRJ││CRD││AI ││YT ││ADM│
    │   ││   ││   ││   ││   ││   │
    │SVC││SVC││SVC││SVC││SVC││SVC│
    └─┬─┘└─┬─┘└─┬─┘└─┬─┘└─┬─┘└─┬─┘
      │    │    │    │    │    │
      └────┴────┴────┴────┴────┘
            │         │
            ▼         ▼
        ┌─────┐   ┌─────┐
        │ DB  │   │Queue│
        └─────┘   └─────┘
```

### Technology Stack Summary

| Layer | Technologies |
|-------|-------------|
| **Runtime** | Node.js 18.x LTS |
| **Framework** | Express.js / NestJS |
| **Database** | PostgreSQL 15, Redis 7.x |
| **Storage** | AWS S3 |
| **Queue** | BullMQ, RabbitMQ, AWS SQS |
| **Authentication** | JWT, OAuth 2.0 |
| **AI Services** | Stable Diffusion, ElevenLabs, Wav2Lip |
| **Monitoring** | Winston, Prometheus, CloudWatch |
| **Deployment** | Docker, Kubernetes, AWS ECS |

## 🚀 Getting Started

### Prerequisites
- Node.js 18.x or higher
- PostgreSQL 15
- Redis 7.x
- Docker & Docker Compose
- AWS Account (for S3)

### Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd AI-Film-Studio
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Services (Development)**
   ```bash
   docker-compose up -d
   npm run dev
   ```

4. **Run Migrations**
   ```bash
   npm run migrate
   ```

5. **Access Services**
   - User Service: http://localhost:3001
   - Project Service: http://localhost:3002
   - Credit Service: http://localhost:3003
   - AI Job Service: http://localhost:3004
   - YouTube Service: http://localhost:3005
   - Admin Service: http://localhost:3006

## 📖 Additional Resources

- [Project README](../../README.md) - Main project documentation
- [Functional Requirements](../requirements/FRD.md) - Feature specifications
- [Non-Functional Requirements](../requirements/NFR.md) - Performance and quality requirements

## 🤝 Contributing

When contributing to the backend:
1. Follow the service patterns defined in the Implementation Guide
2. Write tests for all new endpoints (see Testing Strategy)
3. Update API documentation for any API changes
4. Ensure all services can scale independently
5. Follow security best practices (JWT, input validation, rate limiting)

## �� Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-31 | Initial backend documentation with Node.js stack |

---

**Maintained by**: AI-Empower-HQ-360  
**Last Updated**: 2025-12-31
