# AI Film Studio - Frontend

This is the frontend application for AI Film Studio, built with Next.js 14, TypeScript, and Tailwind CSS.

## 🏠 Homepage

The application includes a fully functional homepage (`/`) that showcases the AI Film Studio platform with:

- **Navigation Bar**: Fixed header with logo, navigation links (Features, How It Works, Pricing), and CTA button
- **Hero Section**: Compelling headline, value proposition, and call-to-action buttons
- **Features Section**: 6 key features of the platform including Script Analysis, Storyboard Generation, Video Composition, Audio Generation, GPU Acceleration, and Cloud-Native infrastructure
- **How It Works**: 4-step process visualization (Upload Script → AI Analysis → Generate Media → Download Film)
- **CTA Section**: Encouraging message to join creators
- **Footer**: Links and copyright information

## 🚀 Getting Started

### Prerequisites

- Node.js >= 18
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Development

The development server will be available at [http://localhost:3000](http://localhost:3000)

### Linting

```bash
npm run lint
```

## 📁 Project Structure

```
frontend/
├── src/
│   └── app/
│       ├── components/
│       │   └── LandingPage.tsx    # Main homepage component
│       ├── layout.tsx              # Root layout with metadata
│       ├── page.tsx                # Home page (renders LandingPage)
│       └── globals.css             # Global styles
├── public/                         # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.mjs
```

## 🎨 Styling

The application uses Tailwind CSS for styling with a custom dark theme featuring:
- Dark blue/slate color scheme
- Gradient accents (sky-blue to purple to pink)
- Responsive design with mobile-first approach
- Smooth transitions and hover effects

## 🔧 Technologies

- **Next.js 14.2.35**: React framework with App Router
- **React 18.3.1**: UI library
- **TypeScript 5.7.2**: Type-safe development
- **Tailwind CSS 3.4.17**: Utility-first CSS framework
- **ESLint**: Code linting

## 📝 License

MIT License - See LICENSE file for details
