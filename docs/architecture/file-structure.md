# AI Film Studio - Complete File Structure

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Overview

This document provides the complete file and folder structure for the AI Film Studio project, organized by component and purpose. The structure follows industry best practices for separation of concerns, scalability, and maintainability.

---

## 📁 Complete Directory Structure

```
ai-film-studio/
│
├── frontend/                          # User-facing web application (React + Next.js)
│   ├── public/                        # Static assets served directly
│   │   ├── images/                    # Logo, icons, placeholders
│   │   │   ├── logo.svg
│   │   │   ├── logo-dark.svg
│   │   │   ├── placeholder-video.png
│   │   │   └── favicon.ico
│   │   ├── fonts/                     # Custom web fonts
│   │   │   ├── inter.woff2
│   │   │   └── roboto.woff2
│   │   ├── icons/                     # SVG icons
│   │   │   ├── play.svg
│   │   │   ├── pause.svg
│   │   │   └── upload.svg
│   │   └── locales/                   # Translation files
│   │       ├── en.json
│   │       ├── es.json
│   │       ├── hi.json
│   │       └── fr.json
│   │
│   ├── src/                           # Source code
│   │   ├── app/                       # Next.js App Router (v14+)
│   │   │   ├── layout.tsx             # Root layout with providers
│   │   │   ├── page.tsx               # Home page
│   │   │   ├── loading.tsx            # Loading UI
│   │   │   ├── error.tsx              # Error boundary
│   │   │   ├── not-found.tsx          # 404 page
│   │   │   ├── (auth)/                # Authentication routes group
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── register/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── reset-password/
│   │   │   │       └── page.tsx
│   │   │   ├── (dashboard)/           # Protected routes group
│   │   │   │   ├── layout.tsx         # Dashboard layout
│   │   │   │   ├── dashboard/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── projects/
│   │   │   │   │   ├── page.tsx       # Project list
│   │   │   │   │   ├── [id]/          # Dynamic project page
│   │   │   │   │   │   ├── page.tsx
│   │   │   │   │   │   └── edit/
│   │   │   │   │   │       └── page.tsx
│   │   │   │   │   └── new/
│   │   │   │   │       └── page.tsx
│   │   │   │   ├── generate/
│   │   │   │   │   └── page.tsx       # Video generation UI
│   │   │   │   ├── library/
│   │   │   │   │   └── page.tsx       # Asset library
│   │   │   │   ├── settings/
│   │   │   │   │   └── page.tsx       # User settings
│   │   │   │   └── billing/
│   │   │   │       └── page.tsx       # Subscription management
│   │   │   └── api/                   # API routes (serverless functions)
│   │   │       ├── auth/
│   │   │       │   ├── login/route.ts
│   │   │       │   └── logout/route.ts
│   │   │       ├── upload/
│   │   │       │   └── route.ts       # Handle file uploads
│   │   │       └── webhook/
│   │   │           └── route.ts       # Stripe webhooks
│   │   │
│   │   ├── components/                # Reusable React components
│   │   │   ├── common/                # Generic UI components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Dropdown.tsx
│   │   │   │   ├── Spinner.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Badge.tsx
│   │   │   │   ├── Alert.tsx
│   │   │   │   ├── Tooltip.tsx
│   │   │   │   └── Tabs.tsx
│   │   │   ├── layout/                # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Navigation.tsx
│   │   │   │   └── MobileMenu.tsx
│   │   │   ├── auth/                  # Authentication components
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   ├── PasswordResetForm.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── projects/              # Project-related components
│   │   │   │   ├── ProjectCard.tsx
│   │   │   │   ├── ProjectList.tsx
│   │   │   │   ├── ProjectForm.tsx
│   │   │   │   ├── ProjectGrid.tsx
│   │   │   │   └── ProjectFilters.tsx
│   │   │   ├── video/                 # Video-related components
│   │   │   │   ├── VideoPlayer.tsx
│   │   │   │   ├── VideoEditor.tsx
│   │   │   │   ├── VideoPreview.tsx
│   │   │   │   ├── VideoTimeline.tsx
│   │   │   │   └── VideoControls.tsx
│   │   │   ├── generation/            # AI generation components
│   │   │   │   ├── GenerationForm.tsx
│   │   │   │   ├── ScriptEditor.tsx
│   │   │   │   ├── VoiceSelector.tsx
│   │   │   │   ├── StyleSelector.tsx
│   │   │   │   ├── DurationSlider.tsx
│   │   │   │   └── GenerationProgress.tsx
│   │   │   ├── upload/                # File upload components
│   │   │   │   ├── FileUploader.tsx
│   │   │   │   ├── ImageUploader.tsx
│   │   │   │   ├── VideoUploader.tsx
│   │   │   │   └── UploadProgress.tsx
│   │   │   └── billing/               # Billing components
│   │   │       ├── PricingCard.tsx
│   │   │       ├── SubscriptionPlan.tsx
│   │   │       ├── PaymentForm.tsx
│   │   │       └── InvoiceList.tsx
│   │   │
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useAuth.ts             # Authentication hook
│   │   │   ├── useProjects.ts         # Project data fetching
│   │   │   ├── useVideoGeneration.ts  # Video generation state
│   │   │   ├── useFileUpload.ts       # File upload management
│   │   │   ├── useDebounce.ts         # Debouncing utility
│   │   │   ├── useLocalStorage.ts     # Local storage helper
│   │   │   ├── useWebSocket.ts        # WebSocket connection
│   │   │   └── useMediaQuery.ts       # Responsive design hook
│   │   │
│   │   ├── services/                  # API communication layer
│   │   │   ├── api.ts                 # Axios configuration
│   │   │   ├── auth.service.ts        # Authentication API calls
│   │   │   ├── project.service.ts     # Project CRUD operations
│   │   │   ├── video.service.ts       # Video generation API
│   │   │   ├── asset.service.ts       # Asset management
│   │   │   ├── user.service.ts        # User profile operations
│   │   │   ├── billing.service.ts     # Subscription API
│   │   │   └── youtube.service.ts     # YouTube integration
│   │   │
│   │   ├── store/                     # State management
│   │   │   ├── index.ts               # Redux store configuration
│   │   │   ├── slices/                # Redux Toolkit slices
│   │   │   │   ├── userSlice.ts       # User state
│   │   │   │   ├── projectSlice.ts    # Project state
│   │   │   │   ├── uiSlice.ts         # UI state (modals, toasts)
│   │   │   │   └── generationSlice.ts # Video generation state
│   │   │   └── projectStore.ts        # Zustand alternative store
│   │   │
│   │   ├── styles/                    # CSS and styling
│   │   │   ├── globals.css            # Global styles
│   │   │   ├── tailwind.css           # Tailwind imports
│   │   │   ├── video-player.css       # Video.js customization
│   │   │   └── animations.css         # Custom animations
│   │   │
│   │   ├── utils/                     # Utility functions
│   │   │   ├── formatters.ts          # Date, number formatting
│   │   │   ├── validators.ts          # Input validation
│   │   │   ├── helpers.ts             # General helpers
│   │   │   ├── constants.ts           # App constants
│   │   │   └── errors.ts              # Error handling
│   │   │
│   │   ├── types/                     # TypeScript type definitions
│   │   │   ├── project.ts             # Project types
│   │   │   ├── user.ts                # User types
│   │   │   ├── video.ts               # Video types
│   │   │   ├── api.ts                 # API response types
│   │   │   └── common.ts              # Shared types
│   │   │
│   │   └── config/                    # Configuration files
│   │       ├── i18n.ts                # i18next configuration
│   │       ├── theme.ts               # Theme configuration
│   │       └── constants.ts           # App-wide constants
│   │
│   ├── .env.local                     # Environment variables (local)
│   ├── .env.production                # Production environment variables
│   ├── .eslintrc.json                 # ESLint configuration
│   ├── .prettierrc                    # Prettier configuration
│   ├── next.config.js                 # Next.js configuration
│   ├── tailwind.config.js             # Tailwind CSS configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── package.json                   # Dependencies and scripts
│   └── README.md                      # Frontend documentation
│
├── backend/                           # Backend microservices (FastAPI + Python)
│   ├── services/                      # Microservices
│   │   ├── user-service/              # User authentication & management
│   │   │   ├── src/
│   │   │   │   ├── main.py            # FastAPI app entry point
│   │   │   │   ├── models/            # Database models
│   │   │   │   │   ├── user.py
│   │   │   │   │   └── session.py
│   │   │   │   ├── routes/            # API routes
│   │   │   │   │   ├── auth.py
│   │   │   │   │   └── profile.py
│   │   │   │   ├── schemas/           # Pydantic schemas
│   │   │   │   │   ├── user.py
│   │   │   │   │   └── auth.py
│   │   │   │   ├── services/          # Business logic
│   │   │   │   │   ├── auth_service.py
│   │   │   │   │   └── user_service.py
│   │   │   │   └── utils/
│   │   │   │       ├── jwt.py
│   │   │   │       └── password.py
│   │   │   ├── tests/
│   │   │   │   ├── test_auth.py
│   │   │   │   └── test_user.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   │
│   │   ├── project-service/           # Project CRUD & metadata
│   │   │   ├── src/
│   │   │   │   ├── main.py
│   │   │   │   ├── models/
│   │   │   │   │   └── project.py
│   │   │   │   ├── routes/
│   │   │   │   │   └── projects.py
│   │   │   │   ├── schemas/
│   │   │   │   │   └── project.py
│   │   │   │   └── services/
│   │   │   │       └── project_service.py
│   │   │   ├── tests/
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   │
│   │   ├── credit-service/            # Subscription & credit management
│   │   │   ├── src/
│   │   │   │   ├── main.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── subscription.py
│   │   │   │   │   └── credit.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── billing.py
│   │   │   │   │   └── credits.py
│   │   │   │   ├── schemas/
│   │   │   │   └── services/
│   │   │   │       ├── stripe_service.py
│   │   │   │       └── credit_service.py
│   │   │   ├── tests/
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   │
│   │   ├── ai-job-service/            # AI job queue management
│   │   │   ├── src/
│   │   │   │   ├── main.py
│   │   │   │   ├── models/
│   │   │   │   │   └── job.py
│   │   │   │   ├── routes/
│   │   │   │   │   └── jobs.py
│   │   │   │   ├── schemas/
│   │   │   │   │   └── job.py
│   │   │   │   └── services/
│   │   │   │       ├── job_service.py
│   │   │   │       └── queue_service.py
│   │   │   ├── tests/
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   │
│   │   ├── youtube-service/           # YouTube OAuth & upload
│   │   │   ├── src/
│   │   │   │   ├── main.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── oauth.py
│   │   │   │   │   └── upload.py
│   │   │   │   └── services/
│   │   │   │       └── youtube_service.py
│   │   │   ├── tests/
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   │
│   │   └── admin-service/             # Admin panel & monitoring
│   │       ├── src/
│   │       │   ├── main.py
│   │       │   ├── routes/
│   │       │   │   ├── users.py
│   │       │   │   ├── analytics.py
│   │       │   │   └── system.py
│   │       │   └── services/
│   │       │       └── admin_service.py
│   │       ├── tests/
│   │       ├── Dockerfile
│   │       └── requirements.txt
│   │
│   ├── common/                        # Shared utilities across services
│   │   ├── logger.py                  # Centralized logging
│   │   ├── middleware.py              # Common middleware
│   │   ├── exceptions.py              # Custom exceptions
│   │   ├── database.py                # Database connection
│   │   └── redis_client.py            # Redis connection
│   │
│   ├── queue/                         # Job queue definitions
│   │   ├── job_types.py               # Job type enums
│   │   ├── queue_manager.py           # Queue operations
│   │   └── workers.py                 # Background workers
│   │
│   ├── config/                        # Configuration
│   │   ├── settings.py                # Environment settings
│   │   ├── database.py                # DB configuration
│   │   └── aws.py                     # AWS SDK configuration
│   │
│   ├── migrations/                    # Alembic database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── docker-compose.yml             # Local development setup
│   ├── requirements.txt               # Shared dependencies
│   └── README.md                      # Backend documentation
│
├── ai/                                # AI/ML models and processing pipelines
│   ├── script-analysis/               # NLP & scene analysis
│   │   ├── src/
│   │   │   ├── analyzer.py            # Script parsing
│   │   │   ├── scene_detector.py      # Scene breakdown
│   │   │   ├── context_analyzer.py    # Cultural context analysis
│   │   │   └── dialogue_extractor.py
│   │   ├── models/                    # Fine-tuned models
│   │   │   └── script_model.pt
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── image-generation/              # Character & background generation
│   │   ├── src/
│   │   │   ├── generator.py           # Main generation logic
│   │   │   ├── character_gen.py       # Character image generation
│   │   │   ├── background_gen.py      # Background generation
│   │   │   └── style_transfer.py      # Style application
│   │   ├── models/                    # SDXL and LoRA models
│   │   │   ├── sdxl_base.safetensors
│   │   │   └── custom_lora.safetensors
│   │   ├── prompts/                   # Prompt templates
│   │   │   └── templates.json
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── voice-synthesis/               # Text-to-Speech & voice cloning
│   │   ├── src/
│   │   │   ├── tts_engine.py          # TTS generation
│   │   │   ├── voice_cloner.py        # Voice cloning
│   │   │   └── emotion_control.py     # Emotion modulation
│   │   ├── models/
│   │   │   └── tts_model.pt
│   │   ├── voices/                    # Pre-configured voices
│   │   │   ├── male_1.json
│   │   │   └── female_1.json
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── lip-sync-animation/            # Facial animation & lip sync
│   │   ├── src/
│   │   │   ├── lip_sync.py            # Lip synchronization
│   │   │   ├── facial_animator.py     # Facial expression
│   │   │   └── blendshapes.py         # Blendshape generation
│   │   ├── models/
│   │   │   └── lipsync_model.pt
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── music-poems/                   # Music & poem generation
│   │   ├── src/
│   │   │   ├── music_gen.py           # Background music
│   │   │   ├── sloka_gen.py           # Slokas generation
│   │   │   └── audio_mixer.py         # Audio mixing
│   │   ├── models/
│   │   │   └── musicgen_model.pt
│   │   ├── samples/                   # Audio samples
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── subtitles/                     # Multi-language subtitle generation
│   │   ├── src/
│   │   │   ├── subtitle_gen.py        # Subtitle generation
│   │   │   ├── translator.py          # Multi-language translation
│   │   │   └── synchronizer.py        # Timing synchronization
│   │   ├── models/
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── common/                        # Shared AI utilities
│   │   ├── model_loader.py            # Model loading utilities
│   │   ├── gpu_manager.py             # GPU resource management
│   │   └── preprocessing.py           # Data preprocessing
│   │
│   └── requirements.txt               # Shared AI dependencies
│
├── cloud-infra/                       # Infrastructure as Code (IaC)
│   ├── terraform/                     # Terraform configurations
│   │   ├── environments/              # Environment-specific configs
│   │   │   ├── dev/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── terraform.tfvars
│   │   │   ├── test/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── terraform.tfvars
│   │   │   ├── staging/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── terraform.tfvars
│   │   │   └── prod/
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       └── terraform.tfvars
│   │   │
│   │   ├── modules/                   # Reusable Terraform modules
│   │   │   ├── vpc/                   # VPC module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── ecs/                   # ECS cluster module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── rds/                   # RDS database module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── s3/                    # S3 bucket module
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── alb/                   # Application Load Balancer
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── cloudfront/            # CloudFront CDN
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   └── elasticache/           # Redis cache
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       └── outputs.tf
│   │   │
│   │   └── backend.tf                 # Terraform state backend (S3)
│   │
│   ├── k8s/                           # Kubernetes manifests (EKS)
│   │   ├── namespaces/
│   │   │   ├── dev.yaml
│   │   │   ├── staging.yaml
│   │   │   └── prod.yaml
│   │   ├── deployments/               # Application deployments
│   │   │   ├── backend-deployment.yaml
│   │   │   └── gpu-worker-deployment.yaml
│   │   ├── services/                  # Kubernetes services
│   │   │   ├── backend-service.yaml
│   │   │   └── gpu-worker-service.yaml
│   │   ├── ingress/                   # Ingress controllers
│   │   │   └── ingress.yaml
│   │   ├── configmaps/                # Configuration maps
│   │   │   └── app-config.yaml
│   │   ├── secrets/                   # Kubernetes secrets
│   │   │   └── app-secrets.yaml
│   │   ├── hpa/                       # Horizontal Pod Autoscaler
│   │   │   ├── backend-hpa.yaml
│   │   │   └── gpu-worker-hpa.yaml
│   │   └── helm/                      # Helm charts (alternative)
│   │       └── ai-film-studio/
│   │           ├── Chart.yaml
│   │           ├── values.yaml
│   │           └── templates/
│   │
│   └── monitoring/                    # Monitoring and alerting
│       ├── cloudwatch/                # CloudWatch dashboards
│       │   ├── backend-dashboard.json
│       │   ├── gpu-worker-dashboard.json
│       │   └── alarms.yaml
│       ├── prometheus/                # Prometheus (optional)
│       │   ├── prometheus.yml
│       │   └── alerts.yml
│       └── grafana/                   # Grafana dashboards
│           └── dashboards/
│               ├── system-overview.json
│               └── ai-processing.json
│
├── salesforce/                        # Salesforce metadata & integration
│   ├── objects/                       # Custom objects
│   │   ├── AI_Project__c/
│   │   │   ├── AI_Project__c.object
│   │   │   └── fields/
│   │   │       ├── Name.field
│   │   │       ├── Status__c.field
│   │   │       ├── User__c.field
│   │   │       └── Created_Date__c.field
│   │   ├── AI_Credit__c/
│   │   │   ├── AI_Credit__c.object
│   │   │   └── fields/
│   │   │       ├── Balance__c.field
│   │   │       ├── User__c.field
│   │   │       └── Transaction_Type__c.field
│   │   └── AI_Job__c/
│   │       ├── AI_Job__c.object
│   │       └── fields/
│   │           ├── Project__c.field
│   │           ├── Status__c.field
│   │           └── Result_URL__c.field
│   │
│   ├── flows/                         # Automation flows
│   │   ├── Credit_Allocation_Flow.flow
│   │   ├── Project_Approval_Flow.flow
│   │   └── Job_Notification_Flow.flow
│   │
│   ├── apex/                          # Apex classes & triggers
│   │   ├── classes/
│   │   │   ├── AIProjectController.cls
│   │   │   ├── CreditManager.cls
│   │   │   ├── JobStatusUpdater.cls
│   │   │   └── AIStudioAPIClient.cls
│   │   └── triggers/
│   │       ├── AIProjectTrigger.trigger
│   │       └── CreditTrigger.trigger
│   │
│   └── reports-dashboards/            # Reports and dashboards
│       ├── reports/
│       │   ├── User_Activity_Report.report
│       │   ├── Credit_Usage_Report.report
│       │   └── Project_Status_Report.report
│       └── dashboards/
│           ├── Executive_Dashboard.dashboard
│           └── Operations_Dashboard.dashboard
│
├── media/                             # Temporary media storage (local dev)
│   ├── images/                        # User-uploaded images
│   ├── videos/                        # Generated videos
│   ├── thumbnails/                    # Auto-generated thumbnails
│   └── subtitles/                     # Subtitle files (.srt, .vtt)
│   └── .gitkeep                       # Keep empty folders in git
│
├── scripts/                           # Utility & deployment scripts
│   ├── deploy.sh                      # Deployment automation
│   ├── backup.sh                      # Database and S3 backup
│   ├── preprocess-media.py            # Media preprocessing
│   ├── db-migrate.sh                  # Database migration runner
│   ├── seed-database.py               # Database seeding
│   └── cleanup-old-files.py           # Clean up old temp files
│
├── docs/                              # Documentation
│   ├── architecture/                  # Architecture documents
│   │   ├── system-design.md
│   │   ├── complete-visual-architecture.md
│   │   ├── frontend-tech-stack.md
│   │   └── file-structure.md
│   ├── requirements/                  # Requirements documents
│   │   ├── FRD.md                     # Functional Requirements
│   │   └── NFR.md                     # Non-Functional Requirements
│   ├── api/                           # API documentation
│   │   ├── openapi.yaml               # OpenAPI/Swagger spec
│   │   ├── authentication.md
│   │   └── endpoints.md
│   ├── deployment/                    # Deployment guides
│   │   ├── local-setup.md
│   │   ├── aws-deployment.md
│   │   └── ci-cd-guide.md
│   ├── operations/                    # Operations runbooks
│   │   ├── monitoring.md
│   │   ├── incident-response.md
│   │   └── disaster-recovery.md
│   └── user-guides/                   # End-user documentation
│       ├── getting-started.md
│       └── video-generation-guide.md
│
├── tests/                             # Integration and E2E tests
│   ├── frontend/                      # Frontend tests
│   │   ├── unit/                      # Jest unit tests
│   │   │   └── components/
│   │   └── e2e/                       # Playwright E2E tests
│   │       ├── auth.spec.ts
│   │       └── video-generation.spec.ts
│   ├── backend/                       # Backend tests
│   │   ├── unit/                      # pytest unit tests
│   │   │   └── test_services.py
│   │   └── integration/               # Integration tests
│   │       ├── test_api.py
│   │       └── test_database.py
│   └── ai/                            # AI model tests
│       ├── test_image_generation.py
│       └── test_voice_synthesis.py
│
├── .github/                           # GitHub-specific files
│   ├── workflows/                     # CI/CD pipelines
│   │   ├── backend-ci-cd.yml          # Backend deployment
│   │   ├── frontend-ci-cd.yml         # Frontend deployment
│   │   ├── terraform-deploy.yml       # Infrastructure deployment
│   │   └── ai-worker-ci-cd.yml        # GPU worker deployment
│   ├── ISSUE_TEMPLATE/                # Issue templates
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md       # PR template
│
├── .gitignore                         # Git ignore rules
├── .env.example                       # Example environment variables
├── docker-compose.yml                 # Multi-service local setup
├── Dockerfile                         # Main Dockerfile (if monorepo)
├── LICENSE                            # MIT License
├── README.md                          # Main project README
├── CONTRIBUTING.md                    # Contribution guidelines
└── CHANGELOG.md                       # Version history
```

---

## 📋 Key Folder Descriptions

### Frontend (`frontend/`)
- **Purpose**: User-facing web application built with React and Next.js
- **Key Files**:
  - `src/app/`: Next.js App Router (v14+) with file-based routing
  - `src/components/`: Reusable React components
  - `src/hooks/`: Custom React hooks for business logic
  - `src/services/`: API communication layer
  - `src/store/`: State management (Redux/Zustand)
- **Deployment**: Vercel, AWS S3 + CloudFront

### Backend (`backend/`)
- **Purpose**: Microservices for API endpoints and business logic
- **Key Services**:
  - `user-service/`: Authentication, user management
  - `project-service/`: Project CRUD operations
  - `credit-service/`: Billing and subscription
  - `ai-job-service/`: Job queue management
  - `youtube-service/`: YouTube integration
  - `admin-service/`: Admin panel
- **Technology**: FastAPI, Python 3.11+, PostgreSQL
- **Deployment**: Amazon ECS (Fargate), Docker containers

### AI (`ai/`)
- **Purpose**: AI/ML models and processing pipelines
- **Key Modules**:
  - `script-analysis/`: NLP and scene breakdown
  - `image-generation/`: SDXL-based image generation
  - `voice-synthesis/`: Text-to-Speech and voice cloning
  - `lip-sync-animation/`: Facial animation
  - `music-poems/`: Music and sloka generation
  - `subtitles/`: Multi-language subtitle generation
- **Technology**: PyTorch, Transformers, Diffusers, CUDA
- **Deployment**: GPU EC2 instances (g4dn.xlarge), Auto-scaling

### Cloud Infrastructure (`cloud-infra/`)
- **Purpose**: Infrastructure as Code for AWS resources
- **Key Folders**:
  - `terraform/`: Terraform configurations for all environments
  - `k8s/`: Kubernetes manifests for EKS deployment
  - `monitoring/`: CloudWatch, Prometheus, Grafana configs
- **Environments**: Dev, Test, Staging, Production

### Salesforce (`salesforce/`)
- **Purpose**: Salesforce metadata for CRM integration
- **Key Components**:
  - `objects/`: Custom objects (AI_Project__c, AI_Credit__c)
  - `flows/`: Process automation
  - `apex/`: Apex classes and triggers
  - `reports-dashboards/`: Analytics and reporting

### Media (`media/`)
- **Purpose**: Temporary storage for media files during processing
- **Note**: In production, all media is stored in S3
- **Folders**: images, videos, thumbnails, subtitles

### Scripts (`scripts/`)
- **Purpose**: Automation and utility scripts
- **Key Scripts**:
  - `deploy.sh`: Deployment automation
  - `backup.sh`: Database and S3 backups
  - `preprocess-media.py`: Media preprocessing

### Docs (`docs/`)
- **Purpose**: Comprehensive documentation
- **Key Folders**:
  - `architecture/`: System design, tech stack
  - `requirements/`: FRD, NFR
  - `api/`: API documentation (OpenAPI)
  - `deployment/`: Deployment guides
  - `operations/`: Runbooks, monitoring

### Tests (`tests/`)
- **Purpose**: Integration and E2E tests
- **Key Folders**:
  - `frontend/`: Jest unit tests, Playwright E2E tests
  - `backend/`: pytest unit and integration tests
  - `ai/`: AI model tests

---

## 🔧 Configuration Files

### Root Level Configuration

| File | Purpose |
|------|---------|
| `.gitignore` | Specifies files/folders to exclude from Git |
| `.env.example` | Template for environment variables |
| `docker-compose.yml` | Multi-service local development setup |
| `Dockerfile` | Container image for monorepo (if applicable) |
| `LICENSE` | MIT License |
| `README.md` | Main project documentation |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CHANGELOG.md` | Version history and release notes |

### Frontend Configuration

| File | Purpose |
|------|---------|
| `next.config.js` | Next.js configuration (routing, images, etc.) |
| `tailwind.config.js` | TailwindCSS theme and plugins |
| `tsconfig.json` | TypeScript compiler options |
| `.eslintrc.json` | ESLint rules for code quality |
| `.prettierrc` | Prettier formatting rules |
| `package.json` | Dependencies, scripts, metadata |

### Backend Configuration

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `alembic.ini` | Database migration configuration |
| `docker-compose.yml` | Local development services (DB, Redis) |
| `Dockerfile` | Container image for each service |

### Infrastructure Configuration

| File | Purpose |
|------|---------|
| `main.tf` | Terraform main configuration |
| `variables.tf` | Input variables for Terraform |
| `terraform.tfvars` | Variable values (per environment) |
| `backend.tf` | Terraform state backend (S3) |

---

## 📝 Environment Variables

### Frontend (`.env.local`)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_KEY=pk_test_xxxxx
NEXT_PUBLIC_YOUTUBE_CLIENT_ID=xxxxx.apps.googleusercontent.com
NEXT_PUBLIC_GA_TRACKING_ID=UA-XXXXXXXXX-X
```

### Backend (`.env`)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aifilmstudio
REDIS_URL=redis://localhost:6379/0

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
S3_BUCKET_NAME=ai-film-studio-media-prod
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789/ai-film-studio-jobs

# Authentication
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# External APIs
OPENAI_API_KEY=sk-xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
YOUTUBE_CLIENT_ID=xxxxx.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=xxxxx
SENDGRID_API_KEY=SG.xxxxx

# Salesforce
SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com
SALESFORCE_CLIENT_ID=xxxxx
SALESFORCE_CLIENT_SECRET=xxxxx
```

---

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio
```

### 2. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
alembic upgrade head  # Run database migrations
uvicorn src.main:app --reload
```

### 4. AI Worker Setup
```bash
cd ai
pip install -r requirements.txt
python src/main.py
```

### 5. Infrastructure Deployment
```bash
cd cloud-infra/terraform/environments/dev
terraform init
terraform plan
terraform apply
```

---

## 📊 File Statistics

- **Total Directories**: ~100+
- **Configuration Files**: ~30+
- **Documentation Files**: ~20+
- **Source Code Directories**: ~50+
- **Test Directories**: ~15+

---

## ✅ Best Practices

### Naming Conventions
- **Folders**: `kebab-case` (e.g., `user-service`)
- **Files**: `snake_case.py` for Python, `PascalCase.tsx` for React components
- **Constants**: `UPPER_SNAKE_CASE`
- **Variables**: `camelCase`

### Organization Principles
1. **Separation of Concerns**: Each folder has a single, well-defined purpose
2. **Modularity**: Components and services are self-contained
3. **Scalability**: Structure supports horizontal scaling
4. **Testability**: Test files mirror source structure
5. **Documentation**: README in each major directory

### Git Ignore Strategy
- Exclude `node_modules/`, `venv/`, `__pycache__/`
- Exclude `.env` files (keep `.env.example`)
- Exclude build artifacts (`dist/`, `out/`, `build/`)
- Include `.gitkeep` for empty folders

---

## 🔄 Maintenance

### Regular Tasks
1. **Dependency Updates**: Monthly review of `package.json` and `requirements.txt`
2. **Documentation**: Update docs when adding new features
3. **Cleanup**: Remove unused files and dependencies
4. **Backups**: Regular backups of database and S3

### Version Control
- **Branching Strategy**: Git Flow (main, develop, feature/*, hotfix/*)
- **Commit Messages**: Conventional Commits (feat, fix, docs, refactor)
- **Pull Requests**: Required for all changes

---

**Document Version History**

| Version | Date       | Author            | Changes                         |
|---------|------------|-------------------|---------------------------------|
| 1.0     | 2025-12-31 | AI-Empower-HQ-360 | Initial file structure document |

---

**End of Document**
