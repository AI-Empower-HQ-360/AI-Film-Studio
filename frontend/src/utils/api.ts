import axios from 'axios';
import { Script, Scene, Shot } from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const scriptApi = {
  generate: async (prompt: string): Promise<Script> => {
    const response = await api.post('/scripts/generate', { prompt });
    return response.data;
  },
  
  analyze: async (scriptContent: string) => {
    const response = await api.post('/scripts/analyze', { content: scriptContent });
    return response.data;
  },
};

export const sceneApi = {
  generateFromScript: async (scriptId: string): Promise<Scene[]> => {
    const response = await api.post(`/scenes/generate/${scriptId}`);
    return response.data;
  },
  
  breakdownScript: async (scriptContent: string): Promise<Scene[]> => {
    const response = await api.post('/scenes/breakdown', { content: scriptContent });
    return response.data;
  },
};

export const shotApi = {
  generateFromScene: async (sceneId: string): Promise<Shot[]> => {
    const response = await api.post(`/shots/generate/${sceneId}`);
    return response.data;
  },
  
  generateImage: async (shotId: string, prompt: string): Promise<string> => {
    const response = await api.post(`/shots/${shotId}/image`, { prompt });
    return response.data.imageUrl;
  },
};

export const videoApi = {
  generate: async (projectId: string) => {
    const response = await api.post(`/video/generate/${projectId}`);
    return response.data;
  },
  
  export: async (projectId: string, settings: any) => {
    const response = await api.post(`/video/export/${projectId}`, settings, {
      responseType: 'blob',
    });
    return response.data;
  },
  
  getStatus: async (jobId: string) => {
    const response = await api.get(`/video/status/${jobId}`);
    return response.data;
  },
};

export default api;
