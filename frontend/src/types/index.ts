export interface Script {
  id: string;
  title: string;
  content: string;
  author: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Scene {
  id: string;
  scriptId: string;
  sceneNumber: number;
  title: string;
  description: string;
  location: string;
  timeOfDay: 'INT' | 'EXT' | 'INT/EXT';
  content: string;
  shots?: Shot[];
}

export interface Shot {
  id: string;
  sceneId: string;
  shotNumber: number;
  shotType: 'WIDE' | 'MEDIUM' | 'CLOSE-UP' | 'EXTREME CLOSE-UP' | 'POV' | 'OVER THE SHOULDER';
  cameraMovement: 'STATIC' | 'PAN' | 'TILT' | 'ZOOM' | 'DOLLY' | 'TRACKING';
  description: string;
  dialogue?: string;
  duration: number;
  imageUrl?: string;
  videoUrl?: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  script?: Script;
  scenes: Scene[];
  status: 'draft' | 'in-progress' | 'completed';
  createdAt: Date;
  updatedAt: Date;
}

export interface VideoExportSettings {
  resolution: '720p' | '1080p' | '4k';
  fps: 24 | 30 | 60;
  format: 'mp4' | 'mov' | 'avi';
  quality: 'low' | 'medium' | 'high' | 'ultra';
}
