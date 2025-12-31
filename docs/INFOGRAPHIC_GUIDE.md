# AI Film Studio – Infographic Layout Guide (Canva/Figma Ready)

**Version:** 1.0  
**Last Updated:** December 31, 2025  
**Document Owner:** AI-Empower-HQ-360

---

## Purpose

This document provides complete specifications for creating a professional infographic for AI Film Studio. All measurements, colors, fonts, and content placements are specified so you can directly implement in Canva, Figma, or PowerPoint.

---

## 1. Canvas Setup

### Dimensions
- **Orientation:** Landscape (16:9 aspect ratio)
- **Size:** 1920px × 1080px (Full HD)
- **Alternative:** 3840px × 2160px (4K for print)
- **Bleed:** 10px on all sides (if printing)

### Background
- **Primary Background:** White (`#FFFFFF`)
- **Alternative:** Light Gray (`#F5F5F5`) for subtle texture
- **Gradient Option:** Soft gradient from `#F8F9FA` (top) to `#FFFFFF` (bottom)

### Grid
- **Columns:** 12-column grid
- **Gutter:** 20px
- **Margins:** 60px (left/right), 40px (top/bottom)

---

## 2. Color Palette (Production-Ready)

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **User Blue** | `#2196F3` | (33, 150, 243) | User layer, CTA buttons |
| **Frontend Light Blue** | `#64B5F6` | (100, 181, 246) | UI elements, highlights |
| **Backend Green** | `#4CAF50` | (76, 175, 80) | Backend services, success |
| **Database Yellow** | `#FFEB3B` | (255, 235, 59) | Storage, data indicators |
| **AI Orange** | `#FF9800` | (255, 152, 0) | AI features, processing |
| **Cloud Purple** | `#9C27B0` | (156, 39, 176) | Infrastructure, cloud |
| **CRM Light Green** | `#8BC34A` | (139, 195, 74) | Salesforce, analytics |
| **Output Red** | `#F44336` | (244, 67, 54) | YouTube, final output |

### Secondary Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Dark Text** | `#212121` | Primary text, headings |
| **Medium Text** | `#757575` | Secondary text, descriptions |
| **Light Text** | `#BDBDBD` | Tertiary text, captions |
| **Border** | `#E0E0E0` | Dividers, borders, lines |
| **Background Accent** | `#FAFAFA` | Boxes, cards, sections |

---

## 3. Typography

### Font Families
- **Primary:** Inter, Roboto, or Open Sans (modern sans-serif)
- **Accent:** Montserrat or Poppins (for headings)
- **Monospace:** Source Code Pro or Fira Code (for technical text)

### Font Sizes

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| **Main Title** | 72px | Bold (700) | "AI Film Studio" |
| **Section Headings** | 48px | Bold (700) | Layer names |
| **Subsection Headings** | 32px | SemiBold (600) | Feature titles |
| **Body Text** | 18px | Regular (400) | Descriptions |
| **Small Text** | 14px | Regular (400) | Captions, notes |
| **Technical Text** | 16px | Medium (500) | Tech stack items |

---

## 4. Infographic Layout (Section-by-Section)

### Layout Structure

```
┌────────────────────────────────────────────────────────────────┐
│                         HEADER (200px)                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│                     MAIN CONTENT (800px)                       │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                         FOOTER (80px)                          │
└────────────────────────────────────────────────────────────────┘
```

---

## 5. Header Section (200px height)

### Elements

**Logo & Title (Center-aligned)**
- **Logo:** 120px × 120px, top-left or centered
- **Title:** "AI Film Studio"
  - Font: 72px, Bold, Color: `#212121`
- **Tagline:** "Master AI Video Creation Platform"
  - Font: 24px, Regular, Color: `#757575`
  - Position: Below title, 10px gap

**Version Badge (Top-right)**
- Text: "v1.0"
- Background: `#4CAF50`, Text: `#FFFFFF`
- Size: 80px × 40px, Rounded corners (8px)

---

## 6. Main Content Section (Layered Architecture)

### Layout: Horizontal Flow (Left to Right)

```
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│  User  │ → │Frontend│ → │Backend │ → │Database│ → │  AI    │
└────────┘   └────────┘   └────────┘   └────────┘   └────────┘
                                                           ↓
┌────────┐   ┌────────┐   ┌────────┐
│ Cloud  │ → │  CRM   │ → │YouTube │
└────────┘   └────────┘   └────────┘
```

### Layer Box Specifications

Each layer is a rounded rectangle (card):

- **Width:** 200px
- **Height:** 150px
- **Rounded Corners:** 12px
- **Shadow:** 0px 4px 8px rgba(0,0,0,0.1)
- **Spacing:** 40px between boxes
- **Border:** 2px solid (layer-specific color)

### Layer Box Content Template

```
┌──────────────────────────┐
│    [Icon] 48×48          │  ← Top, centered, 20px margin
│                          │
│    Layer Name            │  ← 24px font, Bold, 10px below icon
│    (Color: layer color)  │
│                          │
│  • Feature 1             │  ← 14px font, Regular
│  • Feature 2             │  ← Bullet points, left-aligned
│  • Feature 3             │  ← 30px left margin
└──────────────────────────┘
```

---

## 7. Individual Layer Specifications

### Layer 1: User (Blue `#2196F3`)

**Icon:** 👤 (Person) or user profile icon

**Content:**
- **Heading:** "User Layer"
- **Features:**
  - Script Input
  - Image Upload
  - Voice Selection
  - YouTube Auth

---

### Layer 2: Frontend (Light Blue `#64B5F6`)

**Icon:** 💻 (Computer) or browser window icon

**Content:**
- **Heading:** "Frontend"
- **Features:**
  - React + Next.js
  - TailwindCSS
  - Video Preview
  - Multi-language

---

### Layer 3: Backend (Green `#4CAF50`)

**Icon:** ⚙️ (Gear) or server icon

**Content:**
- **Heading:** "Backend"
- **Features:**
  - NestJS/FastAPI
  - Microservices
  - JWT Auth
  - Job Queue

---

### Layer 4: Database (Yellow `#FFEB3B`)

**Icon:** 🗄️ (Database) or storage icon

**Content:**
- **Heading:** "Database/Storage"
- **Features:**
  - PostgreSQL
  - Redis Cache
  - AWS S3
  - CloudFront CDN

---

### Layer 5: AI/ML (Orange `#FF9800`)

**Icon:** 🤖 (Robot) or brain icon

**Content:**
- **Heading:** "AI/ML Layer"
- **Features:**
  - Image Gen (SDXL)
  - Voice Synthesis
  - Lip-sync
  - Subtitle Gen

---

### Layer 6: Cloud (Purple `#9C27B0`)

**Icon:** ☁️ (Cloud) or infrastructure icon

**Content:**
- **Heading:** "Cloud"
- **Features:**
  - AWS EC2 GPU
  - ECS/Kubernetes
  - Terraform
  - Monitoring

---

### Layer 7: CRM (Light Green `#8BC34A`)

**Icon:** 📊 (Chart) or Salesforce logo

**Content:**
- **Heading:** "Salesforce CRM"
- **Features:**
  - Project Tracking
  - Credit Mgmt
  - Dashboards
  - Automation

---

### Layer 8: Output (Red `#F44336`)

**Icon:** ▶️ (Play button) or YouTube logo

**Content:**
- **Heading:** "YouTube/Output"
- **Features:**
  - Video Upload
  - Playlists
  - Thumbnails
  - Download

---

## 8. Flow Arrows

### Arrow Specifications
- **Type:** Solid line with arrowhead
- **Width:** 4px
- **Color:** `#9E9E9E` (medium gray)
- **Arrowhead:** Triangle, 12px × 8px
- **Style:** Curved for better aesthetics
- **Animation (optional):** Dashed line with moving dots

### Arrow Placement
- Connect center-right of one box to center-left of next box
- Use bezier curves for smooth transitions
- Add small labels on arrows (e.g., "API Call", "Data Flow")

---

## 9. Sidebar: Subscription Tiers

**Position:** Right side, vertical layout

**Box:**
- Width: 300px
- Height: 600px
- Background: `#FAFAFA`
- Border: 1px solid `#E0E0E0`
- Rounded corners: 12px
- Padding: 30px

**Content:**

```
┌────────────────────────────┐
│   Subscription Tiers        │  ← 32px Bold
│                            │
│  ┌──────────────────┐      │
│  │ Free - $0/mo     │      │  ← Plan box
│  │ 3 credits        │      │  ← 18px Regular
│  └──────────────────┘      │
│                            │
│  ┌──────────────────┐      │
│  │ Standard - $39   │      │
│  │ 30 credits       │      │
│  └──────────────────┘      │
│                            │
│  ┌──────────────────┐      │
│  │ Pro - $49        │      │  ← Highlighted (border)
│  │ 60 credits       │      │
│  └──────────────────┘      │
│                            │
│  ┌──────────────────┐      │
│  │ Enterprise - $99 │      │
│  │ 150 credits      │      │
│  └──────────────────┘      │
│                            │
│  3 credits = 1 min video   │  ← 14px italic
└────────────────────────────┘
```

---

## 10. Footer Section

**Content:**
- **Left:** "© 2025 AI Film Studio | All Rights Reserved"
- **Center:** Website URL: www.aifilmstudio.com
- **Right:** Contact: info@aifilmstudio.com

**Styling:**
- Font: 14px, Regular
- Color: `#757575`
- Background: `#F5F5F5`
- Height: 80px, centered vertically

---

## 11. Additional Elements

### Metrics Badges (Optional)

Add small metric badges at the bottom:

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ 500+ Videos │  │ 94% Success │  │ 4.6/5 Stars │
│   Generated │  │     Rate    │  │  Satisfaction│
└─────────────┘  └─────────────┘  └─────────────┘
```

- Width: 180px each
- Height: 80px
- Background: White with shadow
- Icon above text
- Centered alignment

### Key Feature Highlights (Callout Boxes)

Position: Below main architecture diagram

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ 🎭 Multi-Age     │  │ 🎵 Music &       │  │ 📺 Direct        │
│    Voices        │  │    Slokas        │  │    YouTube       │
│                  │  │                  │  │    Upload        │
│ 50+ voice types  │  │ Indian & Western │  │ Auto playlists   │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## 12. Export Specifications

### For Digital Use (Web, Presentations)
- **Format:** PNG
- **Resolution:** 1920px × 1080px (Full HD)
- **DPI:** 72
- **Color Space:** RGB
- **Compression:** Medium (balance quality & file size)

### For Print
- **Format:** PDF or PNG
- **Resolution:** 3840px × 2160px (4K) or higher
- **DPI:** 300
- **Color Space:** CMYK
- **Bleed:** 10px on all sides

### For Social Media
- **LinkedIn/Twitter:** 1200px × 675px (PNG)
- **Instagram:** 1080px × 1080px (square)
- **Facebook:** 1200px × 630px

---

## 13. Implementation Steps (Canva)

1. **Create New Design**
   - Custom size: 1920 × 1080 px
   - Background: White or gradient

2. **Add Header**
   - Insert logo (Elements → Uploads)
   - Add title text (Text → Heading)
   - Position centered

3. **Create Layer Boxes**
   - Elements → Shapes → Rounded Rectangle
   - Resize to 200px × 150px
   - Apply layer colors (fill)
   - Add border (2px, layer color)
   - Add shadow effect

4. **Add Icons**
   - Elements → Search emoji or icons
   - Resize to 48px × 48px
   - Position at top of each box

5. **Add Text**
   - Text → Body text
   - Apply fonts and sizes per spec
   - Align within boxes

6. **Draw Arrows**
   - Elements → Lines & Shapes → Arrow
   - Customize color and width
   - Connect boxes

7. **Add Sidebar**
   - Elements → Shapes → Rectangle
   - Apply background color
   - Add subscription content

8. **Final Touches**
   - Add footer text
   - Add metric badges (optional)
   - Review spacing and alignment

9. **Export**
   - Download → PNG
   - Select quality: High
   - Transparent background: Optional

---

## 14. Implementation Steps (Figma)

1. **Create New File**
   - Frame: 1920 × 1080

2. **Setup Grid**
   - Layout Grid: 12 columns, 20px gutter

3. **Create Components**
   - Layer box component (reusable)
   - Arrow component
   - Subscription tier component

4. **Use Auto Layout**
   - For responsive spacing
   - Horizontal for main flow
   - Vertical for sidebar

5. **Apply Color Styles**
   - Define color palette as styles
   - Apply to components

6. **Add Text Styles**
   - Create text styles for each size/weight
   - Apply throughout design

7. **Export Assets**
   - Export as PNG (1x, 2x, 3x)
   - Export as SVG for web

---

## 15. Template Files (Reference)

We recommend using these templates as starting points:

**Canva:**
- Search "Infographic" templates
- Choose "Modern Architecture Diagram"
- Customize with AI Film Studio content

**Figma:**
- Community file: "Tech Architecture Infographic"
- Duplicate and customize

**PowerPoint:**
- Use SmartArt: Process diagrams
- Apply custom colors from palette

---

## 16. Accessibility Considerations

- **Color Contrast:** Ensure WCAG AA compliance (4.5:1 ratio)
- **Font Size:** Minimum 14px for readability
- **Alt Text:** Include descriptive text for screen readers
- **Color Blindness:** Test with Color Oracle or Stark plugin
- **Print-Friendly:** Ensure design works in grayscale

---

## 17. Branding Elements

### Logo Placement
- **Position:** Top-left or centered
- **Size:** 120px × 120px (maintain aspect ratio)
- **Clear Space:** Minimum 20px around logo
- **Background:** Transparent or white

### Color Consistency
- Use only colors from the specified palette
- Avoid introducing new colors
- Maintain 60-30-10 rule (60% background, 30% secondary, 10% accent)

### Typography
- Stick to 2-3 font families maximum
- Maintain hierarchy (headings, subheadings, body)
- Consistent line height (1.5x font size)

---

## 18. Quality Checklist

Before finalizing, verify:

- [ ] All text is readable (no typos, clear font)
- [ ] Colors match specification (exact hex codes)
- [ ] Alignment is consistent (use guides/grids)
- [ ] Spacing is uniform (consistent margins/padding)
- [ ] Arrows connect properly (no gaps or overlaps)
- [ ] Icons are clear and recognizable
- [ ] Logo is high-resolution (not pixelated)
- [ ] Export at correct resolution (1920×1080 minimum)
- [ ] File size is reasonable (<5MB for web)
- [ ] Design works on different backgrounds (test on projector)

---

## 19. Variations

### Simplified Version (4 Layers)
For presentations with limited space:

```
User → Frontend → Backend → AI/ML → Output
```

Focus on: User input, AI processing, Video output

### Detailed Version (10+ Layers)
For technical documentation:

Add sub-layers:
- Backend: Auth, Projects, Credits, Jobs
- AI: Script, Image, Voice, Lipsync, Music, Subtitles

### Dark Mode Version
- Background: `#121212`
- Text: `#FFFFFF`
- Boxes: `#1E1E1E` with lighter borders
- Adjust colors for better contrast

---

## 20. Additional Resources

### Stock Images
- Unsplash: Free high-quality images
- Pexels: Video and image stock
- Icons8: Professional icon sets

### Design Inspiration
- Dribbble: Search "architecture infographic"
- Behance: Search "tech diagram"
- Pinterest: "System architecture design"

### Tools
- Canva: Easy, template-based
- Figma: Professional, collaborative
- Adobe Illustrator: Advanced, print-ready
- PowerPoint/Keynote: Quick, familiar

---

**End of Infographic Guide**

For complete architecture details, see [ARCHITECTURE_VISUAL.md](./ARCHITECTURE_VISUAL.md)  
For developer documentation, see [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)  
For investor presentation, see [INVESTOR_PRESENTATION.md](./INVESTOR_PRESENTATION.md)
