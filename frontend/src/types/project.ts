export interface FilmProject {
  id: string;
  title: string;
  script: string;
  settings: {
    duration: '30' | '45' | '60' | '90';
    style: 'realistic' | 'animated' | 'cinematic' | 'documentary';
    mood: 'dramatic' | 'comedic' | 'suspenseful' | 'romantic' | 'action';
    resolution: '720p' | '1080p' | '4k';
  };
  status: 'draft' | 'processing' | 'completed' | 'failed';
  createdAt: string;
  completedAt?: string;
  thumbnailUrl?: string;
  videoUrl?: string;
}
