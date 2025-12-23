# AI Film Studio Hub - Frontend

Next.js frontend application for the AI Film Studio Hub, providing a user interface for script entry, job progress tracking, and video preview/download.

## Features

- **Authentication**: JWT-based login and registration
- **Script Editor**: Write and submit film scripts
- **Job Progress**: Real-time job status and progress tracking
- **Video Preview**: Preview and download completed videos
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Built with Tailwind CSS

## Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

2. Configure environment:
```bash
cp .env.example .env.local
# Edit .env.local with your API URL
```

## Running

### Development
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Visit http://localhost:3000

### Production Build
```bash
npm run build
npm run start
```

## Architecture

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Home page
├── components/
│   ├── ScriptEditor.tsx    # Script input component
│   ├── JobProgress.tsx     # Job status tracker
│   └── VideoPreview.tsx    # Video player & download
├── lib/
│   ├── api.ts              # API client
│   └── auth.ts             # Auth state management
├── styles/
│   └── globals.css         # Global styles
└── package.json
```

## Components

### ScriptEditor
- Text input for project title and script
- Submit form to create projects and jobs
- Validates input before submission
- Shows success/error messages

### JobProgress
- Real-time job status display
- Progress bar with percentage
- Auto-refreshes every 3 seconds
- Shows error messages if job fails
- Download button when completed

### VideoPreview
- Video player for completed jobs
- Thumbnail preview
- Download buttons for video and thumbnail
- Job metadata display

## State Management

Uses Zustand for state management:
- **Auth Store**: User authentication state
- **Local Storage**: Persists JWT tokens

## API Integration

All API calls go through the centralized API client (`lib/api.ts`):
- Automatic token injection
- Error handling
- Type-safe endpoints

### API Endpoints Used
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `POST /projects` - Create project
- `PUT /projects/{id}` - Update project
- `POST /jobs` - Create job
- `GET /jobs/{id}` - Get job details
- `GET /jobs/{id}/download-url` - Get signed download URL

## Styling

Built with Tailwind CSS:
- Responsive design (mobile-first)
- Dark mode support (via CSS classes)
- Custom color palette
- Reusable component classes

Custom classes:
- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button
- `.card` - Card container
- `.input` - Text input
- `.textarea` - Textarea

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000/api/v1)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Development

### File Structure
- Use TypeScript for type safety
- Components in `components/`
- Pages in `app/` (App Router)
- Utilities in `lib/`

### Adding New Features
1. Create component in `components/`
2. Add API methods to `lib/api.ts`
3. Integrate in pages under `app/`
4. Style with Tailwind classes

## Deployment

### Vercel (Recommended)
```bash
npm run build
# Deploy to Vercel
```

### Docker
```bash
docker build -t ai-film-studio-frontend .
docker run -p 3000:3000 ai-film-studio-frontend
```

### Static Export
```bash
# Add to next.config.js: output: 'export'
npm run build
# Deploy the 'out' directory
```
