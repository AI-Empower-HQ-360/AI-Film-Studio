# Requirements ↔ Frontend Alignment

**Version:** 0.1.0  
**Last Updated:** 2026-01-22  
**Sources:** FRD, BRD, NFR, Master Workflow Roadmap, Investor Blueprint (v2.0)

---

## 1. Version & Changelog

| Item | Value |
|------|--------|
| **Current version** | 0.1.0 (see `VERSION`, `CHANGELOG.md`) |
| **v0.1.0 date** | 2025-12-27 |
| **Unreleased** | Frontend Next.js application (planned) |

Frontend and static webpages reference **v0.1.0** and **FRD/NFR aligned** where relevant.

---

## 2. FRD → Pages & Components

| FR | Requirement | Page / Component | Status |
|----|-------------|------------------|--------|
| **FR-001** | User Registration (email/password, OAuth Google/GitHub, 8+ chars, 1 upper, 1 number) | `/signup` | ✅ Form + OAuth placeholders |
| **FR-002** | User Login (email/password, OAuth, JWT, Remember Me) | `/signin` | ✅ Form + OAuth, Remember Me |
| **FR-003** | Password Reset (forgot-password, 1h expiry) | `/forgot-password` | ✅ Page + link from signin |
| **FR-010** | Create Project (title max 100, script max 500 words) | `FilmCreationWizard`, Landing quick start | ✅ Validation, word count |
| **FR-011** | List Projects (paginated, filter, sort) | Dashboard, `ProjectGrid` | ✅ Mock; API wiring pending |
| **FR-012** | Update Project (draft only) | Dashboard / wizard | ⏳ API pending |
| **FR-013** | Delete Project | Dashboard | ⏳ API pending |
| **FR-020** | Submit Film Generation Job | `FilmCreationWizard`, `useJob` | ✅ UI; API pending |
| **FR-021** | Track Job Progress | `useJob`, Dashboard | ✅ UI; API pending |
| **FR-022** | Download Generated Film | `ProjectGrid`, `VideoPlayerModal` | ✅ UI; API pending |
| **FR-027** | Cultural Preferences (primary/secondary culture) | `FilmCreationWizard` step 2 | ✅ Dropdown (FR-027) |
| **FR-030** | View Credit Balance | Dashboard Usage tab | ✅ Mock; API pending |
| **FR-031** | Purchase Credits ($5 / 10 credits) | Pricing, FAQ | ✅ Copy; Stripe pending |
| **FR-040** | Admin Dashboard | `/admin/dashboard` | ✅ Placeholder |
| **FR-041** | User Management | Admin | ⏳ Placeholder |
| **FR-042** | Content Moderation | `/admin/moderation` | ✅ Placeholder |

---

## 3. User Roles (FRD §2.1)

| Role | Description | Frontend |
|------|-------------|----------|
| **Guest** | View landing, signup | `/`, `/signup`, `/signin` |
| **Free User** | 3 films/month, watermarked | Dashboard, Film Wizard |
| **Pro User** | $29/mo, 30 films, no watermark | Pricing, Dashboard |
| **Enterprise User** | $299/mo, unlimited, priority | Pricing, Dashboard |
| **Admin** | Full access, moderation | `/admin/dashboard`, `/admin/moderation` |

---

## 4. Pricing (FRD / BRD)

| Tier | Price | Films | Frontend |
|------|--------|-------|----------|
| **Free** | $0 | 3/month, watermarked | `/pricing` |
| **Pro** | $29/mo | 30/month, no watermark | `/pricing` |
| **Enterprise** | $299/mo | Unlimited, priority | `/pricing` |
| **Credit top-up** | $5 for 10 credits | — | FAQ on `/pricing`, Docs |

---

## 5. Pages Overview

| Page | Route | Purpose |
|------|--------|---------|
| Home | `/` | Landing, quick start (script/YouTube), 8-engine, v0.1.0 |
| Dashboard | `/dashboard` | Overview, Content, Usage, Account; Film Wizard, ProjectGrid |
| Sign Up | `/signup` | FR-001 registration |
| Sign In | `/signin` | FR-002 login |
| Forgot Password | `/forgot-password` | FR-003 reset |
| Pricing | `/pricing` | Free / Pro / Enterprise, FAQ, credit top-up |
| Features | `/features` | 8-engine, pipeline, capabilities |
| Docs | `/docs` | FRD-aligned API reference, `/api/v1` |
| About | `/about` | Mission, version, team |
| Blog | `/blog` | Blog placeholder |
| Careers | `/careers` | Careers placeholder |
| Contact | `/contact` | Contact placeholder |
| Privacy | `/privacy` | Privacy policy |
| Terms | `/terms` | Terms of service |
| Admin Dashboard | `/admin/dashboard` | FR-040 |
| Admin Moderation | `/admin/moderation` | FR-042 |

---

## 6. Static Website (GitHub Pages)

| File | Updates |
|------|----------|
| `website/index.html` | Hero 8-engine, 3–5 min, 500 words (FR-010); footer v0.1.0, FRD, 2026 |
| `website/features.html` | Hero 8-engine, v0.1.0, FRD |
| `website/about.html` | Hero 8-engine, v0.1.0, FRD |
| `website/docs.html` | Hero FRD-aligned `/api/v1`, v0.1.0 |

---

## 7. Key Components

| Component | Purpose |
|-----------|---------|
| `Navigation` | Logo, Features, How it works, Pricing, Dashboard, Admin, Sign In, Sign Up |
| `LandingPage` | Hero, quick start (script ≤500 words, YouTube), 8-engine, footer v0.1.0 |
| `FilmCreationWizard` | Steps: Script (500 words), Settings (duration, style, mood, resolution, **cultural FR-027**), Review, Generate |
| `ProjectGrid` | Projects, filters, play, create |
| `VideoPlayerModal` | Play generated films |
| `UserDropdown` | Dashboard, Account, Sign out |

---

## 8. API Base (FRD)

All API references use base **`/api/v1`**. Key endpoints:

- `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/forgot-password`
- `POST /api/v1/projects`, `GET /api/v1/projects`, `PATCH /api/v1/projects/:id`, `DELETE /api/v1/projects/:id`
- `POST /api/v1/projects/:id/generate`, `GET /api/v1/jobs/:id`, `GET /api/v1/jobs/:id/download`
- `GET /api/v1/users/me/credits`, `POST /api/v1/credits/purchase`

See `frontend/src/app/docs/page.tsx` and `docs/requirements/FRD.md`.

---

## 9. References

- **FRD:** `docs/requirements/FRD.md`
- **BRD:** `docs/requirements/BRD.md`
- **NFR:** `docs/requirements/NFR.md`
- **Master Workflow:** `docs/requirements/MASTER-WORKFLOW-ROADMAP.md`
- **Blueprint:** `docs/INVESTOR_DEVELOPER_MASTER_BLUEPRINT.md`
- **Changelog:** `CHANGELOG.md`
- **Version:** `VERSION`
