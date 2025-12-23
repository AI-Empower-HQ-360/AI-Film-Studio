# Documentation Index

Welcome to the AI Film Studio documentation!

## 📚 Available Documentation

### [README.md](../README.md)
Main project overview, features, and quick start guide.

**Topics covered:**
- Project overview and features
- Folder structure
- Quick start instructions
- Configuration guide
- Development workflow
- License and contribution guidelines

### [API.md](./API.md)
Complete API endpoint reference.

**Topics covered:**
- Authentication endpoints
- Project management APIs
- Job management APIs
- Cost estimation
- Signed URL generation
- Request/response examples
- Error handling

### [ARCHITECTURE.md](./ARCHITECTURE.md)
System architecture and design documentation.

**Topics covered:**
- System overview
- Component architecture
- Database schema
- State machine design
- Security considerations
- Scalability patterns
- Monitoring strategies

### [DEPLOYMENT.md](./DEPLOYMENT.md)
Production deployment guide.

**Topics covered:**
- Docker deployment
- Cloud platform deployments (AWS, GCP, Heroku)
- Database setup
- Redis configuration
- S3 storage setup
- Environment variables
- Monitoring and logging
- Backup and recovery
- Troubleshooting

## 🚀 Getting Started

1. **First time here?** Start with [README.md](../README.md)
2. **Want to use the API?** Check [API.md](./API.md)
3. **Understanding the system?** Read [ARCHITECTURE.md](./ARCHITECTURE.md)
4. **Deploying to production?** Follow [DEPLOYMENT.md](./DEPLOYMENT.md)

## 💡 Common Use Cases

### For Developers

**Setting up locally:**
```bash
# 1. Clone the repository
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# 2. Start with Docker
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
```

**Making API requests:**
See [API.md](./API.md) for complete endpoint documentation.

### For DevOps

**Production deployment:**
See [DEPLOYMENT.md](./DEPLOYMENT.md) for platform-specific guides.

**Monitoring setup:**
Refer to the Monitoring section in [DEPLOYMENT.md](./DEPLOYMENT.md).

### For Architects

**System design:**
See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture.

**Scalability planning:**
Check the Scalability section in [ARCHITECTURE.md](./ARCHITECTURE.md).

## 🔍 Quick Reference

### Key Technologies

- **Backend:** FastAPI (Python)
- **Worker:** Celery + Redis
- **Frontend:** Next.js (TypeScript)
- **Database:** PostgreSQL
- **Storage:** AWS S3

### Main Components

1. **Authentication Service** - JWT-based user authentication
2. **Project Service** - Project management
3. **Job Service** - Job lifecycle management
4. **Worker Pipeline** - AI content generation
5. **Frontend** - User interface

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register new user |
| `/api/v1/auth/login` | POST | User login |
| `/api/v1/projects/` | GET/POST | List/create projects |
| `/api/v1/jobs/` | GET/POST | List/create jobs |
| `/api/v1/jobs/{id}` | GET | Get job status |
| `/api/v1/jobs/signed-url` | POST | Get download URL |

Full API reference: [API.md](./API.md)

### Job States

```
pending → queued → moderating → processing → completed
                        ↓              ↓
                  moderation_failed  failed
                        ↓              ↓
                    cancelled ← ← ← ← ←
```

### Environment Variables

**Backend:**
- `SECRET_KEY` - JWT secret
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `AWS_*` - AWS credentials

**Worker:**
- `REDIS_URL` - Redis connection
- `OPENAI_API_KEY` - OpenAI API key
- `STABILITY_API_KEY` - Stability AI key
- `ELEVENLABS_API_KEY` - ElevenLabs key

**Frontend:**
- `NEXT_PUBLIC_API_URL` - Backend API URL

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete variable list.

## 🛠️ Development Workflow

1. **Make changes** to code
2. **Test locally** with development server
3. **Run tests** (if available)
4. **Build** to verify no errors
5. **Deploy** to staging/production

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section in [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📝 License

See [LICENSE](../LICENSE) file for details.

---

**Last Updated:** 2024-01-01

For the latest documentation, visit the [GitHub repository](https://github.com/AI-Empower-HQ-360/AI-Film-Studio).
