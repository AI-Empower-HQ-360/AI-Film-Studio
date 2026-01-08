# Frontend - AI Film Studio

## Overview

The frontend of AI Film Studio is a modern web application built with **React 18+**, **Next.js 14**, and **TypeScript**. It provides an intuitive user interface for creating AI-powered short films.

## Technology Stack

- **Framework**: Next.js 14 (React 18+)
- **Language**: TypeScript 5.x
- **Styling**: TailwindCSS 3.x, Material UI
- **State Management**: Redux Toolkit, Zustand
- **Forms**: React Hook Form + Yup validation
- **API Client**: Axios with React Query
- **Video**: Video.js for playback
- **i18n**: i18next for multi-language support

## Project Structure

```
frontend/
├── public/          # Static assets (images, fonts, icons)
├── src/
│   ├── app/         # Next.js App Router pages
│   ├── components/  # Reusable React components
│   ├── hooks/       # Custom React hooks
│   ├── services/    # API communication layer
│   ├── store/       # State management (Redux/Zustand)
│   ├── styles/      # CSS and styling
│   ├── utils/       # Utility functions
│   └── types/       # TypeScript type definitions
└── package.json
```

## Getting Started

### Prerequisites

- Node.js >= 18.x
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`.

### Environment Variables

Create a `.env.local` file with:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_KEY=pk_test_xxxxx
NEXT_PUBLIC_YOUTUBE_CLIENT_ID=xxxxx.apps.googleusercontent.com
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Key Features

### 1. User Authentication
- Email/password registration and login
- Google and GitHub OAuth
- JWT token management
- Password reset flow

### 2. Project Management
- Create, edit, delete projects
- Project status tracking
- Asset organization
- Collaboration features

### 3. Video Generation
- Script input and editing
- Voice selection (multiple languages)
- Style customization
- Duration control (30-90 seconds)
- Real-time progress tracking

### 4. Media Management
- Drag-and-drop file upload
- Image and video preview
- Asset library
- Thumbnail generation

### 5. YouTube Integration
- OAuth authentication
- Direct video upload
- Metadata management
- Upload status tracking

### 6. Subscription Management
- Plan selection and upgrade
- Payment processing (Stripe)
- Credit balance display
- Usage tracking

## Component Architecture

### Common Components
- **Button**: Customizable button with variants
- **Input**: Form input with validation
- **Modal**: Reusable modal dialogs
- **Card**: Content containers
- **Spinner**: Loading indicators

### Layout Components
- **Header**: Top navigation bar
- **Footer**: Footer with links
- **Sidebar**: Dashboard navigation
- **Navigation**: Mobile and desktop menus

### Feature Components
- **ProjectCard**: Project display card
- **VideoPlayer**: Video playback component
- **GenerationForm**: Video generation interface
- **FileUploader**: Drag-and-drop upload

## State Management

### Global State (Redux)
- User authentication state
- User profile and credits
- UI state (modals, notifications)

### Local State (Zustand)
- Project list and selection
- Video generation parameters
- Upload progress

### Server State (React Query)
- API data fetching and caching
- Automatic refetching
- Optimistic updates

## Styling

### TailwindCSS
Utility-first CSS framework for rapid development:

```jsx
<div className="flex items-center justify-between p-4 bg-white shadow-md rounded-lg">
  <h2 className="text-xl font-bold">Project Name</h2>
  <span className="text-sm text-gray-500">Status</span>
</div>
```

### Material UI
Pre-built components for complex UI elements:

```jsx
import { Button, TextField, Dialog } from '@mui/material';

<Dialog open={isOpen} onClose={handleClose}>
  <TextField label="Project Name" fullWidth />
  <Button variant="contained">Create</Button>
</Dialog>
```

## API Integration

All API calls are centralized in the `services/` directory:

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 30000
});

// Add JWT token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## Internationalization

Multi-language support using i18next:

```typescript
import { useTranslation } from 'react-i18next';

const Component = () => {
  const { t, i18n } = useTranslation();
  
  return (
    <div>
      <h1>{t('welcome')}</h1>
      <button onClick={() => i18n.changeLanguage('es')}>
        Español
      </button>
    </div>
  );
};
```

## Testing

### Unit Tests (Jest)
```bash
npm run test
```

### E2E Tests (Playwright)
```bash
npm run test:e2e
```

## Deployment

### Vercel (Recommended)
```bash
vercel --prod
```

### AWS S3 + CloudFront
```bash
npm run build
npm run export
aws s3 sync out/ s3://ai-film-studio-frontend-prod/
```

## Performance Optimization

- **Code Splitting**: Automatic with Next.js
- **Image Optimization**: Next.js `<Image>` component
- **Lazy Loading**: React.lazy and Suspense
- **Caching**: React Query and CDN caching
- **Bundle Analysis**: `npm run analyze`

## Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)

## Contributing

Please read the [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE)

---

For more details, see the [Frontend Tech Stack Documentation](../docs/architecture/frontend-tech-stack.md).
