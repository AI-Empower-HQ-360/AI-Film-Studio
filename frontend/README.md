# AI Film Studio - Frontend

A modern, React-based frontend application for the AI Film Studio project. This application provides an end-to-end workflow for creating AI-generated films: from script writing to scene breakdown, shot planning, and final video export.

## Features

### 🎬 Complete Film Production Workflow
- **Dashboard**: Project management and overview
- **Script Editor**: Write or generate scripts with AI assistance
- **Scene Breakdown**: Organize scripts into individual scenes
- **Shot Planning**: Define camera angles, movements, and shot details
- **Video Export**: Generate and export final MP4 videos

### 🎨 Modern UI/UX
- Clean, dark-themed interface optimized for creative work
- Responsive design that works on desktop, tablet, and mobile
- Smooth animations and transitions
- Intuitive navigation between workflow stages

### 🤖 AI Integration Ready
- AI script generation from prompts
- Automatic scene breakdown from scripts
- Smart shot generation from scenes
- Image generation for shot previews

### 💾 State Management
- Zustand for efficient state management
- Persistent project data
- Real-time updates across components

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Navigation
- **Zustand** - State management
- **Axios** - API communication
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- A backend API server running on `localhost:8000` (optional for full functionality)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run test` - Run tests

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Layout.tsx     # Main layout with navigation
│   │   ├── SceneCard.tsx  # Scene display and editing
│   │   └── ShotCard.tsx   # Shot display and editing
│   ├── pages/             # Page components
│   │   ├── Dashboard.tsx  # Project management
│   │   ├── ScriptEditor.tsx # Script writing/editing
│   │   ├── Scenes.tsx     # Scene breakdown
│   │   ├── Shots.tsx      # Shot planning
│   │   └── Export.tsx     # Video generation/export
│   ├── store/             # State management
│   │   └── index.ts       # Zustand store
│   ├── types/             # TypeScript types
│   │   └── index.ts       # Type definitions
│   ├── utils/             # Utility functions
│   │   └── api.ts         # API client
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── index.html             # HTML template
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── vite.config.ts         # Vite config
└── README.md              # This file
```

## Usage Guide

### 1. Creating a Project

1. Click "New Project" on the dashboard
2. Enter project name and description
3. Click "Create Project"

### 2. Writing a Script

1. Navigate to the Script Editor
2. Option A: Use the AI generator by describing your story
3. Option B: Write your script manually in the text area
4. Fill in script title and author information
5. Click "Save Script" and then "Proceed to Scenes"

### 3. Breaking Down Scenes

1. Use "AI Generate" to automatically break down your script into scenes
2. Or manually add scenes with the "Add Scene" button
3. Edit scene details including:
   - Scene number
   - Title
   - Location
   - Time of day (INT/EXT)
   - Description
   - Content
4. Click "Proceed to Shots" when ready

### 4. Planning Shots

1. Select a scene from the scene tabs
2. Use "AI Generate" to create shots automatically
3. Or add shots manually specifying:
   - Shot type (Wide, Medium, Close-up, etc.)
   - Camera movement (Static, Pan, Tilt, etc.)
   - Duration
   - Description
   - Dialogue
4. Edit or delete shots as needed
5. Click "Proceed to Export"

### 5. Exporting Video

1. Review your project summary
2. Configure export settings:
   - Resolution (720p, 1080p, 4K)
   - Frame rate (24, 30, 60 FPS)
   - Format (MP4, MOV, AVI)
   - Quality (Low, Medium, High, Ultra)
3. Click "Generate Video" to create preview
4. Review the video preview
5. Click "Export Video" to download

## API Integration

The frontend expects a backend API at `http://localhost:8000/api` with the following endpoints:

### Script Endpoints
- `POST /api/scripts/generate` - Generate script from prompt
- `POST /api/scripts/analyze` - Analyze script content

### Scene Endpoints
- `POST /api/scenes/generate/:scriptId` - Generate scenes from script
- `POST /api/scenes/breakdown` - Break down script into scenes

### Shot Endpoints
- `POST /api/shots/generate/:sceneId` - Generate shots from scene
- `POST /api/shots/:shotId/image` - Generate image for shot

### Video Endpoints
- `POST /api/video/generate/:projectId` - Generate video
- `POST /api/video/export/:projectId` - Export video
- `GET /api/video/status/:jobId` - Get generation status

## Customization

### Styling

The application uses CSS custom properties for theming. You can customize colors in `src/index.css`:

```css
:root {
  --primary: #6366f1;
  --secondary: #8b5cf6;
  --accent: #ec4899;
  /* ... more variables */
}
```

### Adding New Features

1. Create new components in `src/components/`
2. Add new pages in `src/pages/`
3. Update routes in `src/App.tsx`
4. Add types in `src/types/index.ts`
5. Update store in `src/store/index.ts`

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.
