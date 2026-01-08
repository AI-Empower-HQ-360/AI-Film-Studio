# Blueprint Quick Reference Guide

This is a quick reference guide to help you navigate the comprehensive [Investor & Developer Master Blueprint](./INVESTOR_DEVELOPER_MASTER_BLUEPRINT.md).

## 📚 Document Sections

### For Investors

| Section | Page Reference | Key Information |
|---------|----------------|-----------------|
| **Executive Summary** | Top of document | High-level overview, key highlights |
| **Business Model & Revenue** | Section 10 | Subscription tiers, revenue projections, unit economics |
| **Subscription & Credit System** | Section 4 | Pricing: Free (\$0), Pro (\$29/mo), Enterprise (\$299/mo) |
| **Success Metrics** | Section 13 | KPIs, target metrics, growth projections |
| **Scalability & Performance** | Section 9 | Scaling strategies, cost optimization |
| **Security & Compliance** | Section 11 | Security measures, GDPR/CCPA compliance |

### For Developers

| Section | Page Reference | Key Information |
|---------|----------------|-----------------|
| **System Architecture Overview** | Section 1 | Complete architecture diagram with all 8 layers |
| **Workflow Layers** | Section 2 | Detailed breakdown of each layer (Frontend to YouTube) |
| **AI Dependencies & Pipeline** | Section 3 | 7-stage AI pipeline with dependency matrix |
| **Technology Stack Matrix** | Section 8 | Complete tech stack (React, Node.js, Python, AWS) |
| **Environment Strategy** | Section 6 | Dev, Sandbox/QA, Staging, Production specs |
| **Integration Layers** | Section 7 | Salesforce CRM & YouTube integration details |

### For Product Managers

| Section | Page Reference | Key Information |
|---------|----------------|-----------------|
| **User Inputs & Outputs** | Section 5 | What users provide and what they receive |
| **Subscription & Credit System** | Section 4 | Feature limits per tier, credit calculation (3 credits = 1 min) |
| **Implementation Roadmap** | Section 12 | 4-phase rollout plan (MVP → Scale → Growth) |

## 🎯 Quick Facts

### AI Capabilities
- **Voice Options**: 25+ voices (Baby, Child, Teen, Adult, Mature)
- **Languages**: 50+ languages supported
- **Cultural Contexts**: Indian, Western, Middle Eastern, Asian, African
- **Music Types**: Indian (Classical, Devotional, Bollywood), Western (Orchestral, Pop)
- **Podcast Mode**: Two-character dialogue with automatic speaker attribution

### Technical Specifications
- **Video Format**: MP4 (H.264 + AAC), 1080p
- **Duration**: 30 seconds - 5 minutes (10 minutes for Enterprise)
- **Processing Time**: 2-5 minutes (for 1-minute video)
- **Concurrent Jobs**: 100+ supported
- **Uptime Target**: 99.9%

### Business Model
- **Free Tier**: \$0/month, 3 credits/month, watermarked
- **Pro Tier**: \$29/month, 30 credits/month, no watermark
- **Enterprise Tier**: \$299/month, unlimited credits, priority support
- **Credit Formula**: 3 credits = 1 minute of video

### Infrastructure
- **Cloud Provider**: AWS
- **Environments**: 4 (Dev, Sandbox/QA, Staging, Production)
- **GPU Instances**: g4dn.xlarge (NVIDIA T4, 16GB)
- **Database**: PostgreSQL (Multi-AZ in production)
- **Cache**: Redis (Cluster mode in production)
- **Storage**: S3 + CloudFront CDN

### Integrations
- **Salesforce CRM**: Bidirectional sync, custom objects, flows, dashboards
- **YouTube**: OAuth 2.0, direct upload, playlist management, SEO optimization
- **Payment**: Stripe for subscriptions and credit purchases

## 🔗 Related Documents

- [System Design Document](./architecture/system-design.md) - Detailed technical architecture
- [Functional Requirements (FRD)](./requirements/FRD.md) - Feature specifications
- [Non-Functional Requirements (NFR)](./requirements/NFR.md) - Performance, security, scalability

## 📊 Diagrams Available

The master blueprint includes:
1. **High-Level Architecture Diagram** - Complete system overview (Section 1.1)
2. **AI Dependency Flow Diagram** - 9-step AI pipeline (Section 3.1)
3. **Input-Output Flow Diagram** - User journey sequence (Section 5.3)
4. **Environment Promotion Flow** - Deployment pipeline (Section 6.3)
5. **YouTube Integration Flow** - OAuth and upload process (Section 7.2.1)

## 🎓 Understanding the Architecture

### The 8 Layers (Color-Coded)

1. **User Layer (Blue)** - User inputs and interactions
2. **Frontend Layer (Light Blue)** - React + Next.js UI
3. **Backend Layer (Green)** - Microservices (Node.js + Python)
4. **Data Layer (Yellow)** - PostgreSQL, Redis, S3
5. **AI/ML Layer (Orange)** - 7-stage AI pipeline with GPU processing
6. **Cloud Layer (Purple)** - AWS infrastructure (ECS, RDS, S3, etc.)
7. **Salesforce CRM Layer (Light Green)** - Customer management & analytics
8. **YouTube Layer (Red)** - Video distribution & publishing

### The 7-Stage AI Pipeline

1. **Script Analysis** → Extract story, characters, actions, culture
2. **Image Generation** → Create characters, backgrounds, props
3. **Voice Synthesis** → Generate speech with 25+ voice options
4. **Animation & Lip-sync** → Animate faces and synchronize lips
5. **Music/Slokas/Poems** → Add background audio
6. **Podcast Mode** → Two-character dialogue (optional)
7. **Subtitles** → ASR + Translation to 50+ languages

## 💡 Key Innovation: Cultural Awareness

The platform automatically detects cultural context from scripts and generates:
- Culturally appropriate clothing (Saree, Kurta, Kimono, etc.)
- Context-specific props (Diyas, Rangoli, Cherry blossoms, etc.)
- Regional music styles (Indian Classical, Western Orchestral, etc.)
- Appropriate backgrounds (Temples, Modern architecture, etc.)

This makes content authentic and relatable to diverse global audiences.

## 📈 Success Metrics Summary

- **Target Users**: 10,000+ monthly active users
- **Target MRR**: \$150,000+
- **Retention Rate**: >70% month-over-month
- **Conversion Rate**: >5% (Free to Paid)
- **LTV:CAC Ratio**: >10:1
- **Gross Margin**: 82-98%

## 🚀 Implementation Timeline

- **Phase 1 (Months 1-3)**: MVP with core features
- **Phase 2 (Months 4-6)**: Enhanced features + integrations
- **Phase 3 (Months 7-9)**: Scale and enterprise features
- **Phase 4 (Months 10-12)**: Growth and advanced features

## 📞 Need More Information?

For detailed information on any topic, refer to the specific section in the [Master Blueprint](./INVESTOR_DEVELOPER_MASTER_BLUEPRINT.md).

For questions or clarifications:
- **Technical**: Review `/docs/architecture/` and `/docs/api/`
- **Business**: See Section 10 (Business Model & Revenue)
- **Implementation**: See Section 12 (Implementation Roadmap)

---

**Last Updated**: 2025-12-31  
**Document Version**: 1.0
