# 🌐 AI FILM STUDIO – FRONTEND TECH STACK

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Table of Contents

1. [Overview](#overview)
2. [Framework / Libraries](#1️⃣-framework--libraries)
3. [Styling / UI](#2️⃣-styling--ui)
4. [Forms / Inputs](#3️⃣-forms--inputs)
5. [Video & Audio](#4️⃣-video--audio)
6. [Interactivity & Components](#5️⃣-interactivity--components)
7. [Multilingual / Internationalization](#6️⃣-multilingual--internationalization)
8. [Frontend Hosting](#7️⃣-frontend-hosting)
9. [Summary](#-summary)

---

## Overview

This document provides a comprehensive overview of the **Frontend Tech Stack** for **AI Film Studio**. The frontend is built with modern, scalable technologies that support AI integration, YouTube upload, multi-language subtitles, and subscription systems. The stack is fully compatible with GitHub Copilot and designed for rapid development and deployment.

---

## 1️⃣ Framework / Libraries

| Layer            | Recommendation                            | Notes                                                     |
| ---------------- | ----------------------------------------- | --------------------------------------------------------- |
| Framework        | **React**                                 | Component-based, widely used, flexible for interactive UI |
| SSR / Routing    | **Next.js**                               | Server-side rendering, dynamic routing, SEO-friendly      |
| State Management | **Redux** / **Zustand** / **Context API** | Manage global state for user, projects, credits, AI jobs  |

### Framework Details

#### React
- **Version:** 18.x
- **Purpose:** Core UI library for building component-based interfaces
- **Benefits:**
  - Large ecosystem and community support
  - Virtual DOM for efficient rendering
  - Hooks for state and lifecycle management
  - Strong TypeScript support
  - Excellent developer experience with React DevTools

#### Next.js
- **Version:** 14.x
- **Purpose:** React framework with server-side rendering and routing
- **Key Features:**
  - Server-Side Rendering (SSR) for improved SEO
  - Static Site Generation (SSG) for performance
  - API routes for backend integration
  - File-based routing system
  - Image optimization out of the box
  - Built-in code splitting and lazy loading
  - Automatic prefetching for faster navigation

#### State Management Options

**Redux**
- **Version:** 5.x with Redux Toolkit
- **Use Case:** Complex applications with extensive global state
- **Benefits:**
  - Predictable state container
  - Time-travel debugging
  - Middleware support (Redux Thunk, Redux Saga)
  - DevTools integration
- **Best For:** Large-scale applications with complex state interactions

**Zustand**
- **Version:** 4.x
- **Use Case:** Lightweight state management with minimal boilerplate
- **Benefits:**
  - Simple API with hooks-based approach
  - No providers needed
  - TypeScript friendly
  - Small bundle size (~1KB)
  - Built-in middleware support
- **Best For:** Medium-sized applications with moderate state complexity

**Context API**
- **Version:** Built into React
- **Use Case:** Simple state sharing across components
- **Benefits:**
  - No additional dependencies
  - Native React solution
  - Good for theming and authentication state
- **Best For:** Small applications or isolated state needs

---

## 2️⃣ Styling / UI

| Layer             | Recommendation                     | Notes                                                  |
| ----------------- | ---------------------------------- | ------------------------------------------------------ |
| Styling           | **TailwindCSS**                    | Utility-first CSS, fast styling, responsive design     |
| Component Library | **Material UI** / **Chakra UI**    | Pre-built components, forms, buttons, modals           |
| Animations        | **Framer Motion** / CSS Animations | Smooth transitions for modals, video previews, buttons |

### Styling Details

#### TailwindCSS
- **Version:** 3.x
- **Purpose:** Utility-first CSS framework for rapid UI development
- **Key Features:**
  - Utility classes for every CSS property
  - Built-in responsive design utilities
  - Dark mode support
  - Custom design system via configuration
  - JIT (Just-In-Time) compiler for smaller bundle sizes
  - PurgeCSS integration to remove unused styles
- **Configuration:**
  ```javascript
  // tailwind.config.js
  module.exports = {
    content: ['./src/**/*.{js,ts,jsx,tsx}'],
    theme: {
      extend: {
        colors: {
          primary: '#FF6B6B',
          secondary: '#4ECDC4',
        },
      },
    },
    plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
    ],
  }
  ```

#### Material UI (MUI)
- **Version:** 5.x
- **Purpose:** Comprehensive React component library
- **Key Components:**
  - Button, TextField, Select, Checkbox, Radio
  - Dialog, Drawer, Snackbar, Alert
  - AppBar, Toolbar, Menu, Tabs
  - Table, Pagination, DataGrid
  - Autocomplete, DatePicker, TimePicker
- **Benefits:**
  - Material Design guidelines
  - Extensive component library
  - Built-in theming system
  - Accessibility compliant
  - TypeScript definitions included

#### Chakra UI
- **Version:** 2.x
- **Purpose:** Simple, modular, and accessible component library
- **Key Features:**
  - Composable components
  - Style props for quick styling
  - Dark mode by default
  - Excellent accessibility (WAI-ARIA compliant)
  - Smaller bundle size than Material UI
  - Better integration with Tailwind CSS

#### Framer Motion
- **Version:** 11.x
- **Purpose:** Production-ready animation library for React
- **Key Features:**
  - Declarative animations with simple syntax
  - Gesture recognition (drag, tap, hover)
  - Layout animations
  - SVG animations
  - Scroll-triggered animations
  - Shared layout animations
- **Use Cases:**
  - Modal enter/exit animations
  - Video preview transitions
  - Button hover effects
  - Page transitions
  - Loading states

---

## 3️⃣ Forms / Inputs

| Layer        | Recommendation      | Notes                                        |
| ------------ | ------------------- | -------------------------------------------- |
| Forms        | **React Hook Form** | Lightweight, handles validations efficiently |
| File Uploads | **React Dropzone**  | Drag & drop images, video assets             |
| Text Inputs  | Multiline textareas | For scripts / captions                       |

### Forms & Input Details

#### React Hook Form
- **Version:** 7.x
- **Purpose:** Performant form validation library
- **Key Features:**
  - Minimal re-renders for better performance
  - Built-in validation rules
  - Easy integration with UI libraries
  - TypeScript support
  - Small bundle size (~8KB)
  - Supports schema validation (Yup, Zod, Joi)
- **Example Usage:**
  ```javascript
  import { useForm } from 'react-hook-form';
  
  const { register, handleSubmit, formState: { errors } } = useForm();
  
  const onSubmit = (data) => console.log(data);
  
  <form onSubmit={handleSubmit(onSubmit)}>
    <input {...register('title', { required: true, maxLength: 100 })} />
    {errors.title && <span>Title is required</span>}
  </form>
  ```

#### React Dropzone
- **Version:** 14.x
- **Purpose:** Drag and drop file upload component
- **Key Features:**
  - Drag and drop interface
  - File type validation
  - File size limits
  - Multiple file uploads
  - Preview generation
  - Customizable styling
  - Mobile-friendly
- **Supported File Types:**
  - Images: JPG, PNG, GIF, WebP
  - Videos: MP4, MOV, AVI, WebM
  - Documents: PDF, TXT
- **Use Cases:**
  - Script file uploads
  - Background image uploads
  - Video asset uploads
  - Logo/branding uploads

#### Text Input Components
- **Multiline Textareas:**
  - Purpose: Script editing, caption input, descriptions
  - Features:
    - Auto-resize based on content
    - Character count display
    - Syntax highlighting for scripts (optional)
    - Undo/redo functionality
    - Markdown support (optional)

---

## 4️⃣ Video & Audio

| Layer          | Recommendation                        | Notes                                      |
| -------------- | ------------------------------------- | ------------------------------------------ |
| Video Player   | **HTML5 Video Player** / **Video.js** | Preview generated videos, podcast playback |
| Audio Playback | Native HTML5 Audio / Wavesurfer.js    | For voice previews, music snippets         |

### Video & Audio Details

#### HTML5 Video Player
- **Purpose:** Native browser video playback
- **Key Features:**
  - Built-in controls
  - No additional dependencies
  - Supports MP4, WebM, Ogg
  - Subtitles/captions support (VTT)
  - Picture-in-picture mode
  - Fullscreen support
- **Use Cases:**
  - Quick video previews
  - Simple playback needs
  - Minimal customization required

#### Video.js
- **Version:** 8.x
- **Purpose:** Extensible HTML5 video player
- **Key Features:**
  - Customizable controls and styling
  - Plugin ecosystem
  - Adaptive streaming support (HLS, DASH)
  - Multiple quality levels
  - Playlist support
  - Analytics integration
  - Responsive design
  - Touch-friendly controls
- **Plugins:**
  - videojs-contrib-quality-levels
  - videojs-resolution-switcher
  - videojs-playlist
  - videojs-seek-buttons
- **Use Cases:**
  - Generated video previews
  - Multi-quality video playback
  - Advanced player controls
  - Analytics tracking

#### HTML5 Audio
- **Purpose:** Native browser audio playback
- **Key Features:**
  - Simple audio controls
  - Supports MP3, WAV, OGG
  - Lightweight
  - No dependencies
- **Use Cases:**
  - Voice-over previews
  - Background music snippets
  - Sound effects testing

#### Wavesurfer.js
- **Version:** 7.x
- **Purpose:** Audio visualization and waveform display
- **Key Features:**
  - Waveform visualization
  - Regions and markers
  - Zoom and scroll
  - Timeline display
  - Audio editing capabilities
  - Spectrogram view
  - Multiple plugin support
- **Use Cases:**
  - Audio editing interface
  - Voice-over trimming
  - Music track visualization
  - Precise audio timing

---

## 5️⃣ Interactivity & Components

| Component         | Purpose                                                      |
| ----------------- | ------------------------------------------------------------ |
| Dropdowns         | Select voice, video duration, music, language                |
| Modals / Popups   | Video processing status, YouTube OAuth, subscription top-ups |
| Buttons           | Generate video, download, regenerate, upload                 |
| Tabs / Accordions | Multi-language subtitles, FAQ, settings                      |
| Notifications     | Toast messages for success/failure alerts                    |

### Interactive Components Details

#### Dropdowns
- **Purpose:** Selection of various options throughout the application
- **Implementation:** Material UI Select, Chakra Select, or Headless UI Listbox
- **Features:**
  - Searchable options
  - Multi-select capability
  - Custom option rendering
  - Keyboard navigation
  - Virtual scrolling for large lists
- **Use Cases:**
  - Voice selection (different voice actors/styles)
  - Video duration (30s, 60s, 90s)
  - Music track selection
  - Language selection
  - Video quality settings
  - Export format selection

#### Modals / Popups
- **Purpose:** Overlay dialogs for important actions and information
- **Implementation:** Material UI Dialog, Chakra Modal, or Headless UI Dialog
- **Features:**
  - Focus trap for accessibility
  - Backdrop click to close
  - ESC key to close
  - Nested modals support
  - Animations (enter/exit)
  - Custom sizes
- **Use Cases:**
  - Video processing status with progress bar
  - YouTube OAuth authentication flow
  - Subscription plan selection and top-ups
  - Confirmation dialogs (delete project)
  - Settings and preferences
  - Tutorial/onboarding flows
  - Error messages with details

#### Buttons
- **Purpose:** Primary interaction elements
- **Types:**
  - Primary: Generate video, Save project
  - Secondary: Cancel, Back
  - Destructive: Delete, Remove
  - Icon buttons: Settings, Menu, Close
  - Loading states: Spinner during processing
- **States:**
  - Default, Hover, Active, Disabled, Loading
- **Use Cases:**
  - Generate video from script
  - Download generated video
  - Regenerate with different parameters
  - Upload assets
  - Save/Edit project
  - Share video
  - YouTube publish

#### Tabs / Accordions
- **Purpose:** Organize content in collapsible sections
- **Implementation:** Material UI Tabs/Accordion, Chakra Tabs/Accordion
- **Features:**
  - Keyboard navigation
  - Animated transitions
  - Controlled/uncontrolled modes
  - Vertical/horizontal orientation
- **Use Cases:**
  - Multi-language subtitle editing (tabs for each language)
  - FAQ section (accordion)
  - Project settings (tabs: General, AI, Video, Audio)
  - Video export options
  - User profile sections
  - Help documentation

#### Notifications (Toast)
- **Purpose:** Temporary feedback messages
- **Implementation:** React Hot Toast, React Toastify, or Chakra Toast
- **Features:**
  - Auto-dismiss with configurable timeout
  - Position control (top, bottom, corners)
  - Different variants (success, error, warning, info)
  - Action buttons (undo, view details)
  - Queue management
  - Custom styling
- **Use Cases:**
  - Success: "Video generated successfully!"
  - Error: "Failed to upload file. Please try again."
  - Warning: "You're running low on credits."
  - Info: "Processing started. This may take a few minutes."
  - Progress: "Video generation: 45% complete"

---

## 6️⃣ Multilingual / Internationalization

| Layer   | Recommendation | Notes                                                    |
| ------- | -------------- | -------------------------------------------------------- |
| Library | **i18next**    | Supports multiple languages for subtitles, UI, tutorials |

### Internationalization Details

#### i18next
- **Version:** 23.x
- **Purpose:** Complete internationalization framework
- **Key Features:**
  - Translation management
  - Language detection
  - Lazy loading of translations
  - Pluralization support
  - Interpolation
  - Context-based translations
  - Namespace support
  - Backend plugin for loading translations
- **Integration:**
  - react-i18next for React integration
  - next-i18next for Next.js integration
- **Supported Languages (Initial):**
  - English (en)
  - Spanish (es)
  - French (fr)
  - German (de)
  - Japanese (ja)
  - Chinese Simplified (zh-CN)
  - Portuguese (pt-BR)
  - Arabic (ar)

#### Configuration Example
```javascript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: require('./locales/en.json') },
      es: { translation: require('./locales/es.json') },
      // ... more languages
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });
```

#### Translation Structure
```json
{
  "common": {
    "generate": "Generate Video",
    "download": "Download",
    "cancel": "Cancel"
  },
  "dashboard": {
    "welcome": "Welcome, {{name}}!",
    "projects": "Your Projects",
    "credits": "Credits remaining: {{count}}"
  },
  "video": {
    "processing": "Processing video...",
    "success": "Video generated successfully!",
    "error": "Failed to generate video"
  }
}
```

#### Use Cases
- UI translations (buttons, labels, messages)
- Multi-language subtitles for generated videos
- Tutorial and help content in multiple languages
- Email notifications in user's preferred language
- Error messages localization
- Date and time formatting
- Number and currency formatting

---

## 7️⃣ Frontend Hosting

| Layer          | Recommendation                       | Notes                                        |
| -------------- | ------------------------------------ | -------------------------------------------- |
| Hosting        | **AWS S3 + CloudFront** / **Vercel** | Fast CDN, scalable hosting for React/Next.js |
| SSL / Security | Managed via hosting provider         | HTTPS for all pages                          |

### Hosting Details

#### AWS S3 + CloudFront (Primary)
- **Purpose:** Static website hosting with global CDN
- **Architecture:**
  - Next.js static export deployed to S3
  - CloudFront distribution for CDN delivery
  - Route53 for DNS management
  - ACM for SSL/TLS certificates

**S3 Configuration:**
```yaml
Bucket Configuration:
  - Bucket Name: ai-film-studio-frontend-prod
  - Region: us-east-1
  - Static Website Hosting: Enabled
  - Index Document: index.html
  - Error Document: 404.html
  - Versioning: Enabled
  - Encryption: AES-256

Bucket Policy:
  - Public Read: Disabled (CloudFront only)
  - CORS: Enabled for API calls
```

**CloudFront Configuration:**
```yaml
Distribution Settings:
  - Origin: S3 Static Website
  - Origin Access Identity: Enabled
  - SSL Certificate: ACM (*.aifilmstudio.com)
  - HTTP to HTTPS: Redirect
  - Supported Protocols: TLS 1.2, TLS 1.3
  - Compression: Gzip, Brotli
  - Cache Behavior:
      - Default TTL: 86400 (1 day)
      - Min TTL: 0
      - Max TTL: 31536000 (1 year)
  - Custom Error Responses:
      - 404 → /404.html
      - 403 → /index.html (for SPA routing)
  - Edge Locations: Global (225+ locations)
  - Origin Shield: Enabled (us-east-1)
```

**Performance Optimizations:**
- Static asset caching with long TTL
- Image optimization via CloudFront
- Gzip/Brotli compression
- HTTP/2 and HTTP/3 support
- Edge caching for low latency
- Cache invalidation strategy

**Cost Considerations:**
- S3 Storage: ~$0.023/GB/month
- CloudFront Data Transfer: ~$0.085/GB (first 10TB)
- CloudFront Requests: ~$0.0075/10,000 requests
- Route53: ~$0.50/hosted zone/month

#### Vercel (Alternative)
- **Purpose:** Managed platform for Next.js applications
- **Key Features:**
  - Zero-configuration deployments
  - Automatic SSL certificates
  - Global edge network
  - Serverless functions support
  - Preview deployments for PRs
  - Built-in analytics
  - Incremental Static Regeneration (ISR)
  - Edge middleware support

**Vercel Configuration:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://api.aifilmstudio.com/$1"
    }
  ]
}
```

**Benefits:**
- Automatic HTTPS
- Instant cache invalidation
- Preview deployments for every PR
- Built-in monitoring and analytics
- Optimized for Next.js
- Serverless functions at the edge

**Cost Considerations:**
- Free tier: 100GB bandwidth
- Pro tier: $20/user/month
- Enterprise: Custom pricing

#### SSL / Security
**AWS ACM (Certificate Manager):**
- Free SSL/TLS certificates
- Automatic renewal
- Wildcard certificate support (*.aifilmstudio.com)
- Integration with CloudFront and ALB

**Vercel SSL:**
- Automatic SSL certificates via Let's Encrypt
- Automatic renewal
- Custom domain support
- Wildcard certificates included

**Security Headers:**
```yaml
Response Headers:
  - Strict-Transport-Security: max-age=31536000; includeSubDomains
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
  - Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
  - Referrer-Policy: strict-origin-when-cross-origin
```

---

## 🔹 Summary

The **AI Film Studio Frontend Tech Stack** is a modern, production-ready architecture designed for scalability, performance, and developer productivity.

### Core Technologies
* **React + Next.js**: Component-based UI with server-side rendering
* **TailwindCSS + Material UI/Chakra UI**: Rapid styling with pre-built, accessible components
* **Redux / Zustand**: Flexible global state management
* **React Hook Form + Dropzone**: Efficient form handling and file uploads
* **Video.js / HTML5 Video**: Professional video and audio preview
* **i18next**: Comprehensive multi-language support
* **AWS S3 + CloudFront / Vercel**: Scalable hosting with global CDN

### Key Capabilities
✅ **AI Integration Ready**: Seamless connection to backend AI services  
✅ **YouTube Upload**: OAuth integration for direct publishing  
✅ **Multi-Language Subtitles**: Full i18n support for global reach  
✅ **Subscription System**: Ready for Stripe/payment integration  
✅ **Responsive Design**: Mobile-first approach with TailwindCSS  
✅ **Performance Optimized**: Code splitting, lazy loading, CDN delivery  
✅ **Accessibility**: WAI-ARIA compliant components  
✅ **Developer Experience**: TypeScript, hot reload, comprehensive tooling  

### Deployment Options
1. **AWS S3 + CloudFront**: Full control, cost-effective for high traffic
2. **Vercel**: Zero-config, optimized for Next.js, perfect for rapid iteration

### Integration Points
- **Backend API**: RESTful API via Axios/Fetch
- **Authentication**: JWT tokens with refresh mechanism
- **File Storage**: Direct S3 uploads with presigned URLs
- **Real-time Updates**: WebSocket or Server-Sent Events for job progress
- **Analytics**: Google Analytics, Mixpanel, or custom solution
- **Error Tracking**: Sentry or similar service

### Development Workflow
1. Local development with hot reload
2. Feature branches with preview deployments
3. Automated testing (Jest, Playwright)
4. Code review and quality checks
5. Staging deployment for QA
6. Production deployment with blue-green strategy
7. Monitoring and performance tracking

This stack is **fully compatible** with GitHub Copilot and modern development practices, ensuring rapid feature development while maintaining code quality and performance standards.

---

## Related Documents

- [System Design Document](./system-design.md)
- [Functional Requirements Document](../requirements/FRD.md)
- [Non-Functional Requirements](../requirements/NFR.md)
- [Main README](../../README.md)

---

## Document Revision History

| Version | Date       | Author            | Changes                                  |
|---------|------------|-------------------|------------------------------------------|
| 1.0     | 2025-12-31 | AI-Empower-HQ-360 | Initial frontend tech stack document     |

---

**End of Document**
