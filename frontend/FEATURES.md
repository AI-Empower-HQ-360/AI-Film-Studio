# AI Film Studio - Feature Guide

## Complete Frontend Application Overview

This document provides a comprehensive overview of all features and pages in the AI Film Studio frontend application.

---

## 🏠 Dashboard Page

**Route**: `/`

### Features:
- **Project Management**
  - View all projects in a grid layout
  - Create new projects with name and description
  - Quick access to current active project
  - Project status badges (draft, in-progress, completed)
  
- **Project Statistics**
  - Number of scenes per project
  - Number of shots per project
  - Last updated timestamp
  
- **Actions**
  - Click any project card to open it
  - "New Project" button to create projects
  - "Continue Working" to resume current project

### UI Elements:
- Clean card-based design
- Empty state with helpful call-to-action
- Modal dialog for project creation
- Responsive grid layout

---

## 📝 Script Editor Page

**Route**: `/script`

### Features:
- **Manual Script Writing**
  - Full-screen text editor
  - Monospace font for screenplay formatting
  - Word count and reading time estimates
  
- **AI Script Generation**
  - Describe your story in natural language
  - AI generates complete script
  - Edit generated scripts
  
- **Script Metadata**
  - Script title
  - Author name
  - Creation and update timestamps
  
- **Statistics Display**
  - Real-time word count
  - Estimated reading time
  
- **Actions**
  - Save script
  - Proceed to scene breakdown

### UI Elements:
- Large textarea with screenplay-style formatting
- Prominent AI generation section
- Statistics bar
- Sticky action buttons

### Sample Script Format:
```
INT. COFFEE SHOP - DAY

The camera pans across a busy coffee shop. 
We see ALEX (30s), sitting alone at a corner table, 
typing on a laptop.

ALEX
(to waiter)
One more coffee, please.
```

---

## 🎬 Scene Breakdown Page

**Route**: `/scenes`

### Features:
- **AI Scene Generation**
  - Automatically break down script into scenes
  - Intelligent scene detection
  - Proper scene numbering
  
- **Manual Scene Management**
  - Add scenes manually
  - Edit scene details inline
  - Delete scenes
  
- **Scene Details**
  - Scene number
  - Title
  - Location (e.g., "Coffee Shop", "Park")
  - Time of day (INT/EXT)
  - Description
  - Dialogue and action content
  - Shot count
  
- **Actions per Scene**
  - Edit scene
  - Delete scene
  - Manage shots

### UI Elements:
- Grid layout of scene cards
- Color-coded badges for INT/EXT
- Expandable scene content
- Modal for adding new scenes

---

## 🎥 Shot Planning Page

**Route**: `/shots`

### Features:
- **Scene Selection**
  - Tabbed interface to switch between scenes
  - Shows shot count per scene
  
- **AI Shot Generation**
  - Automatically generate shots from scene
  - Intelligent camera work suggestions
  
- **Shot Details**
  - Shot number
  - Shot type:
    - Wide Shot
    - Medium Shot
    - Close-Up
    - Extreme Close-Up
    - POV (Point of View)
    - Over The Shoulder
  - Camera movement:
    - Static
    - Pan
    - Tilt
    - Zoom
    - Dolly
    - Tracking
  - Duration (in seconds)
  - Description
  - Dialogue
  - Image preview (when available)
  
- **Visual Feedback**
  - Image placeholders for shots
  - Duration display
  - Type and movement badges

### UI Elements:
- Scene selector tabs
- Grid of shot cards
- Image preview areas
- Inline editing
- Modal for adding shots

---

## 📤 Export Page

**Route**: `/export`

### Features:
- **Project Summary**
  - Total scenes count
  - Total shots count
  - Total duration calculation
  
- **Video Generation**
  - Generate video from all shots
  - Progress indicator
  - Preview player
  
- **Export Settings**
  - Resolution:
    - 720p (HD)
    - 1080p (Full HD)
    - 4K (Ultra HD)
  - Frame Rate:
    - 24 FPS (Cinematic)
    - 30 FPS (Standard)
    - 60 FPS (Smooth)
  - Format:
    - MP4
    - MOV
    - AVI
  - Quality:
    - Low
    - Medium
    - High
    - Ultra
    
- **Video Preview**
  - Built-in video player
  - Controls for playback
  
- **Export Actions**
  - Generate video button
  - Download video button

### UI Elements:
- Two-column layout (main content + settings sidebar)
- Summary cards with icons
- Progress bar during generation
- Video player for preview
- Settings panel with dropdowns

---

## 🎨 Design System

### Color Palette
- **Primary**: Purple/Indigo (#6366f1)
- **Secondary**: Purple (#8b5cf6)
- **Accent**: Pink (#ec4899)
- **Background**: Dark (#0f0f0f)
- **Surface**: Dark Gray (#1a1a1a)

### Typography
- **Headers**: Inter font family
- **Script Content**: Courier New (monospace)
- **Body**: Inter font family

### Components
- **Buttons**: 3 variants (primary, secondary, danger)
- **Cards**: Elevated surfaces with hover effects
- **Badges**: Status indicators with color coding
- **Modals**: Centered overlays with backdrop
- **Inputs**: Dark-themed form controls

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

---

## 🔄 User Workflow

### Complete Production Pipeline:

1. **Start** → Dashboard
   - Create or select project

2. **Write** → Script Editor
   - Write or generate script
   - Add metadata
   - Save and continue

3. **Organize** → Scenes
   - Break down script
   - Review and edit scenes
   - Proceed to shots

4. **Plan** → Shots
   - Define camera work
   - Set shot details
   - Add descriptions

5. **Finish** → Export
   - Generate video
   - Configure settings
   - Download final MP4

---

## 🎯 Key Features

### State Persistence
- Projects stored in application state
- Navigate between pages without losing work
- Current project remains active

### Inline Editing
- Edit scenes and shots without separate forms
- Real-time updates
- Cancel/save actions

### AI Integration Points
1. Script generation from prompts
2. Scene breakdown from scripts
3. Shot generation from scenes
4. Image generation for shot previews

### Responsive Design
- Works on desktop, tablet, and mobile
- Adaptive layouts
- Touch-friendly controls
- Collapsible navigation on mobile

---

## 📊 Statistics & Metrics

The application tracks and displays:
- Word count in scripts
- Reading time estimates
- Scene counts
- Shot counts per scene
- Total project duration
- Last updated timestamps

---

## 🚀 Performance Features

- **Fast Loading**: Vite for instant HMR
- **Optimized Builds**: Minified production bundles
- **Lazy Loading**: Route-based code splitting
- **Efficient Rendering**: React 18 optimizations

---

## 🔐 Future Enhancements

### Planned Features:
- [ ] User authentication
- [ ] Cloud storage integration
- [ ] Real-time collaboration
- [ ] Advanced timeline editor
- [ ] Asset library management
- [ ] Export presets
- [ ] Project templates
- [ ] Version history
- [ ] Comments and annotations
- [ ] Team sharing

---

## 📱 Accessibility

- Semantic HTML structure
- Keyboard navigation support
- ARIA labels on interactive elements
- Focus management in modals
- Contrast ratios meet WCAG standards

---

## 🎓 Learning Resources

### For Developers:
- Comprehensive README in `/frontend/README.md`
- Technical documentation in `/frontend/TECHNICAL.md`
- Inline code comments
- TypeScript type definitions

### For Users:
- Intuitive UI with helpful empty states
- Clear action buttons
- Progress indicators
- Contextual navigation

---

**Version**: 1.0.0  
**Last Updated**: December 2025
