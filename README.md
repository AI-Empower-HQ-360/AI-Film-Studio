# AI Film Studio

End-to-end AI Film Studio: script → scenes → shots → video → MP4

A comprehensive web application that enables users to create complete films using AI assistance. From writing scripts to breaking down scenes, planning shots, and exporting final videos.

## 🎬 Features

### Complete Film Production Pipeline
- **Script Writing**: Create scripts manually or use AI generation
- **Scene Breakdown**: Automatically or manually break scripts into scenes
- **Shot Planning**: Define camera angles, movements, and shot compositions
- **Video Generation**: AI-powered video generation from shots
- **MP4 Export**: Export final films in various resolutions and formats

### Modern Frontend Interface
- Clean, intuitive UI optimized for creative workflows
- Real-time project state management
- Responsive design for desktop and mobile
- Dark theme optimized for long working sessions

## 🚀 Quick Start

### Frontend Setup

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

4. Open your browser to `http://localhost:3000`

For detailed frontend documentation, see [frontend/README.md](frontend/README.md)

## 📁 Project Structure

```
AI-Film-Studio/
├── frontend/              # React + TypeScript frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── store/        # State management
│   │   ├── types/        # TypeScript definitions
│   │   └── utils/        # Utility functions
│   ├── package.json
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md             # This file
```

## 🛠️ Technology Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Zustand for state management
- React Router for navigation
- Axios for API communication
- Lucide React for icons

### Planned Backend (API)
- Python with FastAPI or similar
- AI/ML integration for:
  - Script generation
  - Scene analysis
  - Shot planning
  - Video generation

## 📖 Usage

### 1. Create a New Project
Start by creating a new film project from the dashboard. Give it a name and description.

### 2. Write or Generate a Script
Use the Script Editor to either:
- Write your script manually
- Generate a script using AI by providing a story prompt

### 3. Break Down into Scenes
Automatically or manually break your script into individual scenes. Each scene includes:
- Location
- Time of day (INT/EXT)
- Description
- Dialogue and action

### 4. Plan Shots
For each scene, define individual shots with:
- Shot type (Wide, Medium, Close-up, etc.)
- Camera movement (Static, Pan, Dolly, etc.)
- Duration
- Description

### 5. Generate and Export
Generate your video from the planned shots and export in your desired format:
- Resolution: 720p, 1080p, or 4K
- Frame rate: 24, 30, or 60 FPS
- Format: MP4, MOV, or AVI
- Quality levels from Low to Ultra

## 🎨 Screenshots

The interface includes:
- **Dashboard**: Project overview and management
- **Script Editor**: Full-featured script writing interface
- **Scene Breakdown**: Visual scene organization
- **Shot Planning**: Detailed shot-by-shot planning
- **Export**: Video generation and export controls

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern web technologies
- Icons by Lucide
- Inspired by professional film production workflows

## 📞 Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Note**: This project is under active development. The backend API integration is planned for future releases. Currently, the frontend provides a complete UI/UX experience with mock data handling.
