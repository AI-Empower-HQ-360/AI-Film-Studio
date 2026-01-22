# Frontend Testing Checklist — AI Film Studio

**Deployed URL:** [https://ai-empower-hq-360.github.io/AI-Film-Studio/](https://ai-empower-hq-360.github.io/AI-Film-Studio/)  
**Dashboard:** [https://ai-empower-hq-360.github.io/AI-Film-Studio/dashboard/](https://ai-empower-hq-360.github.io/AI-Film-Studio/dashboard/)

Use this checklist to manually test the home page, dashboard, and all other frontend functions.

---

## 1. Home Page

| # | Test | URL | Expected | Pass |
|---|------|-----|----------|------|
| 1.1 | Home loads | `/` or `/index.html` | Hero, "Transform Scripts into Films", nav | ☐ |
| 1.2 | Logo links to home | Click 🎬 AI Film Studio | Navigate to `/` | ☐ |
| 1.3 | **Features** section | Scroll / `/#features` | Feature cards visible | ☐ |
| 1.4 | **How It Works** | `/#how-it-works` | Steps 1–4 visible | ☐ |
| 1.5 | **Quick Start — Try with Your Script** | Click button | Script/YouTube input appears | ☐ |
| 1.6 | **Write Script** mode | Toggle, enter text | Script input focused | ☐ |
| 1.7 | **YouTube URL** mode | Toggle, enter `https://youtube.com/...` | URL validated | ☐ |
| 1.8 | **Start Creating Free** | Click | Navigate to `/signup` | ☐ |
| 1.9 | **Dashboard** link (footer/nav) | Click | Navigate to `/dashboard` | ☐ |
| 1.10 | **Pricing** link | Click | Navigate to `/pricing` | ☐ |

---

## 2. Dashboard

| # | Test | URL | Expected | Pass |
|---|------|-----|----------|------|
| 2.1 | Dashboard loads | `/dashboard` or `/dashboard/` | Dashboard layout, tabs | ☐ |
| 2.2 | **Overview** tab | Default | Stats, recent projects | ☐ |
| 2.3 | **Content** tab | `?tab=content` or tab click | Project grid | ☐ |
| 2.4 | **Usage** tab | `?tab=usage` | Usage / credits info | ☐ |
| 2.5 | **Account** tab | `?tab=account` | Account settings | ☐ |
| 2.6 | **Create New Film** | Button | Film Creation Wizard opens | ☐ |
| 2.7 | **Project cards** | Click project | Details or video modal | ☐ |
| 2.8 | **Play video** | Click play on project | Video plays in modal | ☐ |
| 2.9 | **Quick start from home** | Home → script → Dashboard | Wizard opens with script | ☐ |
| 2.10 | **User dropdown** (if present) | Click avatar/name | Menu with Dashboard, Sign out | ☐ |

---

## 3. Navigation & Common Links

| # | Test | Action | Expected | Pass |
|---|------|--------|----------|------|
| 3.1 | **Features** | Nav → Features | `/#features` or `/features` | ☐ |
| 3.2 | **How It Works** | Nav → How It Works | `/#how-it-works` | ☐ |
| 3.3 | **Pricing** | Nav → Pricing | `/pricing` | ☐ |
| 3.4 | **Dashboard** | Nav → Dashboard | `/dashboard` | ☐ |
| 3.5 | **Sign In** | Nav → Sign In | `/signin` | ☐ |
| 3.6 | **Sign Up** | Nav → Sign Up | `/signup` | ☐ |
| 3.7 | **Mobile menu** | Resize → toggle | Links accessible | ☐ |

---

## 4. Other Pages

| # | Page | URL | What to check | Pass |
|---|------|-----|---------------|------|
| 4.1 | **About** | `/about` | About content, no 404 | ☐ |
| 4.2 | **Blog** | `/blog` | Blog list or placeholder | ☐ |
| 4.3 | **Careers** | `/careers` | Careers content | ☐ |
| 4.4 | **Contact** | `/contact` | Contact form or info | ☐ |
| 4.5 | **Docs** | `/docs` | API/docs content | ☐ |
| 4.6 | **Features** | `/features` | Features page | ☐ |
| 4.7 | **Pricing** | `/pricing` | Plans, "Back to Home" | ☐ |
| 4.8 | **Privacy** | `/privacy` | Privacy policy | ☐ |
| 4.9 | **Terms** | `/terms` | Terms of use | ☐ |
| 4.10 | **Sign In** | `/signin` | Form, redirect to dashboard | ☐ |
| 4.11 | **Sign Up** | `/signup` | Form, redirect to dashboard | ☐ |

---

## 5. Film Creation Wizard (Dashboard)

| # | Test | Action | Expected | Pass |
|---|------|--------|----------|------|
| 5.1 | Open wizard | "Create New Film" | Modal/wizard opens | ☐ |
| 5.2 | **Step 1 — Script** | Enter script | Next enabled | ☐ |
| 5.3 | **Step 2 — Settings** | Duration, style, mood | Options selectable | ☐ |
| 5.4 | **Step 3 — Generate** | Confirm | Loading / success state | ☐ |
| 5.5 | **Close wizard** | Cancel / X | Wizard closes | ☐ |
| 5.6 | **Quick start with script** | Home script → Dashboard | Wizard pre-filled | ☐ |

---

## 6. Project Grid & Video

| # | Test | Action | Expected | Pass |
|---|------|--------|----------|------|
| 6.1 | Project grid | Content tab | Cards with title, status | ☐ |
| 6.2 | **Filter** (if any) | Use filter | List updates | ☐ |
| 6.3 | **Click project** | Click card | Detail view or modal | ☐ |
| 6.4 | **Play** | Play button | Video modal, playback | ☐ |
| 6.5 | **Close modal** | X or overlay | Modal closes | ☐ |
| 6.6 | **"Create" from grid** | Button to new film | Wizard or create flow | ☐ |

---

## 7. Responsive & Basic UX

| # | Test | Action | Expected | Pass |
|---|------|--------|----------|------|
| 7.1 | **Desktop** | 1920×1080 | Layout correct | ☐ |
| 7.2 | **Tablet** | 768×1024 | Responsive layout | ☐ |
| 7.3 | **Mobile** | 375×667 | Mobile nav, readable | ☐ |
| 7.4 | **Tab order** | Tab through page | Logical focus order | ☐ |
| 7.5 | **No layout shift** | Load page | No big CLS | ☐ |

---

## 8. Static Website (GitHub Pages)

If you use the **static** site (`website/`):

| # | Test | URL | Expected | Pass |
|---|------|-----|----------|------|
| 8.1 | Home | `/` or `index.html` | Hero, feature cards | ☐ |
| 8.2 | Features | `features.html` | Features content | ☐ |
| 8.3 | Docs | `docs.html` | Documentation | ☐ |
| 8.4 | About | `about.html` | About content | ☐ |
| 8.5 | Nav links | Click each | No 404 | ☐ |

---

## 9. Run E2E Tests Against Deployed Site

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\frontend
$env:PLAYWRIGHT_TEST_BASE_URL="https://ai-empower-hq-360.github.io/AI-Film-Studio"
npx playwright test --config=playwright.config.production.ts
```

Or use the npm script (if added):

```powershell
npm run test:e2e:production
```

---

## 10. Run Locally (Next.js)

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\frontend
npm install
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000) and go through **§1–§7** above using local URLs.

---

## Quick Links

| Page | Production | Local |
|------|------------|-------|
| Home | [GitHub Pages](https://ai-empower-hq-360.github.io/AI-Film-Studio/) | http://localhost:3000 |
| Dashboard | [Dashboard](https://ai-empower-hq-360.github.io/AI-Film-Studio/dashboard/) | http://localhost:3000/dashboard |
| Pricing | [Pricing](https://ai-empower-hq-360.github.io/AI-Film-Studio/pricing) | http://localhost:3000/pricing |
| Sign In | [Sign In](https://ai-empower-hq-360.github.io/AI-Film-Studio/signin) | http://localhost:3000/signin |
| Sign Up | [Sign Up](https://ai-empower-hq-360.github.io/AI-Film-Studio/signup) | http://localhost:3000/signup |

---

## Notes

- **GitHub Pages** may serve the static `website/` (index, features, docs, about) or a static export of the Next.js app. If `/dashboard` returns 404, test the Next.js app locally or via Amplify.
- **Amplify** (see `amplify.yml`) deploys the **Next.js frontend**; use the Amplify app URL for full app (home, dashboard, etc.) if different from GitHub Pages.

**Last updated:** 2026-01-22
