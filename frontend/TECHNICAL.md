# AI Film Studio Frontend - Technical Documentation

## Architecture Overview

### Technology Stack
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5
- **Routing**: React Router v6
- **State Management**: Zustand 4
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Styling**: CSS with CSS Custom Properties

### Design Patterns

#### 1. Component-Based Architecture
The application follows a modular component structure:
- **Pages**: High-level route components
- **Components**: Reusable UI elements
- **Store**: Centralized state management
- **Utils**: Helper functions and API clients

#### 2. State Management with Zustand
```typescript
// Centralized store with actions
const useAppStore = create<AppState>((set, get) => ({
  currentProject: null,
  projects: [],
  // Actions
  setCurrentProject: (project) => set({ currentProject: project }),
  // ... more actions
}));
```

#### 3. Type Safety with TypeScript
All data structures are strictly typed:
```typescript
interface Project {
  id: string;
  name: string;
  scenes: Scene[];
  status: 'draft' | 'in-progress' | 'completed';
}
```

### Data Flow

```
User Action → Component → Store Update → Re-render
                    ↓
              API Call (optional)
                    ↓
              Backend Response → Store Update
```

### Page Workflow

1. **Dashboard** (`/`)
   - Project listing and management
   - Create new projects
   - Select active project

2. **Script Editor** (`/script`)
   - Manual script writing
   - AI-powered script generation
   - Script metadata (title, author)

3. **Scenes** (`/scenes`)
   - Automatic scene breakdown from script
   - Manual scene creation
   - Scene editing and management

4. **Shots** (`/shots`)
   - Shot planning per scene
   - AI-generated shots
   - Shot details (type, movement, duration)

5. **Export** (`/export`)
   - Video generation from shots
   - Export settings configuration
   - Final MP4 download

## Component Details

### Layout Component
Provides consistent navigation and structure across all pages.
- Sticky header with navigation
- Responsive design
- Active route highlighting

### SceneCard Component
Displays and manages individual scenes.
- Inline editing
- Scene metadata display
- Shot count indicator

### ShotCard Component
Displays and manages individual shots.
- Image/video preview
- Shot specifications
- Dialogue display

## API Integration

### Endpoints Configuration
```typescript
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### API Services
- **scriptApi**: Script generation and analysis
- **sceneApi**: Scene breakdown and generation
- **shotApi**: Shot generation and image creation
- **videoApi**: Video generation and export

## Styling System

### CSS Custom Properties
```css
:root {
  --primary: #6366f1;
  --secondary: #8b5cf6;
  --accent: #ec4899;
  --background: #0f0f0f;
  --surface: #1a1a1a;
}
```

### Utility Classes
- `.btn` - Button styles with variants
- `.card` - Container with elevation
- `.badge` - Status indicators
- `.modal` - Overlay dialogs

### Responsive Design
- Mobile-first approach
- Breakpoints at 768px and 1024px
- Flexible grid layouts

## Performance Optimizations

1. **Code Splitting**: React Router handles automatic code splitting
2. **Lazy Loading**: Components load on-demand
3. **Optimized Builds**: Vite provides fast HMR and optimized production builds
4. **CSS Optimization**: Minimal CSS with efficient selectors

## Development Workflow

### Running Locally
```bash
npm install
npm run dev
```

### Building for Production
```bash
npm run build
npm run preview
```

### Linting
```bash
npm run lint
```

## Future Enhancements

### Planned Features
1. **Real-time Collaboration**: Multiple users editing same project
2. **Version Control**: Track changes and revert to previous versions
3. **Asset Library**: Manage images, videos, and audio files
4. **Timeline Editor**: Visual timeline for precise shot timing
5. **Export Presets**: Save and reuse export configurations
6. **Cloud Storage**: Save projects to cloud
7. **Sharing**: Share projects with team members

### Technical Improvements
1. **Testing**: Add unit and integration tests
2. **Accessibility**: WCAG 2.1 AA compliance
3. **Internationalization**: Multi-language support
4. **Performance Monitoring**: Add analytics and monitoring
5. **Offline Support**: Progressive Web App capabilities

## Deployment

### Build Output
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   └── index-[hash].css
└── vite.svg
```

### Deployment Targets
- **Static Hosting**: Netlify, Vercel, GitHub Pages
- **CDN**: CloudFlare, AWS CloudFront
- **Self-hosted**: Nginx, Apache

### Environment Variables
```bash
VITE_API_URL=http://localhost:8000/api
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in vite.config.ts or use:
   npm run dev -- --port 3001
   ```

2. **Build Errors**
   ```bash
   # Clear cache and rebuild
   rm -rf node_modules dist
   npm install
   npm run build
   ```

3. **Type Errors**
   ```bash
   # Run TypeScript compiler to see all errors
   npx tsc --noEmit
   ```

## Contributing Guidelines

### Code Style
- Use TypeScript for all new files
- Follow existing naming conventions
- Add comments for complex logic
- Keep components focused and small

### Git Workflow
1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

### Review Checklist
- [ ] Code compiles without errors
- [ ] No console errors or warnings
- [ ] Responsive on mobile and desktop
- [ ] Follows existing code style
- [ ] Types are properly defined
- [ ] No unused imports or variables

## Resources

### Documentation
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Zustand Documentation](https://zustand-demo.pmnd.rs/)

### Tools
- [VS Code](https://code.visualstudio.com/)
- [React DevTools](https://react.dev/learn/react-developer-tools)
- [Redux DevTools](https://github.com/reduxjs/redux-devtools) (works with Zustand)

---

Last Updated: December 2025
Version: 1.0.0
