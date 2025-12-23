import { create } from 'zustand';
import { Project, Script, Scene, Shot } from '../types';

interface AppState {
  currentProject: Project | null;
  projects: Project[];
  
  // Actions
  setCurrentProject: (project: Project | null) => void;
  createProject: (name: string, description: string) => void;
  updateProject: (projectId: string, updates: Partial<Project>) => void;
  deleteProject: (projectId: string) => void;
  
  // Script actions
  setScript: (script: Script) => void;
  updateScript: (updates: Partial<Script>) => void;
  
  // Scene actions
  addScene: (scene: Omit<Scene, 'id'>) => void;
  updateScene: (sceneId: string, updates: Partial<Scene>) => void;
  deleteScene: (sceneId: string) => void;
  
  // Shot actions
  addShot: (sceneId: string, shot: Omit<Shot, 'id'>) => void;
  updateShot: (shotId: string, updates: Partial<Shot>) => void;
  deleteShot: (shotId: string) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  currentProject: null,
  projects: [],

  setCurrentProject: (project) => set({ currentProject: project }),

  createProject: (name, description) => {
    const newProject: Project = {
      id: crypto.randomUUID(),
      name,
      description,
      scenes: [],
      status: 'draft',
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    set((state) => ({
      projects: [...state.projects, newProject],
      currentProject: newProject,
    }));
  },

  updateProject: (projectId, updates) => {
    set((state) => ({
      projects: state.projects.map((p) =>
        p.id === projectId ? { ...p, ...updates, updatedAt: new Date() } : p
      ),
      currentProject:
        state.currentProject?.id === projectId
          ? { ...state.currentProject, ...updates, updatedAt: new Date() }
          : state.currentProject,
    }));
  },

  deleteProject: (projectId) => {
    set((state) => ({
      projects: state.projects.filter((p) => p.id !== projectId),
      currentProject:
        state.currentProject?.id === projectId ? null : state.currentProject,
    }));
  },

  setScript: (script) => {
    const { currentProject } = get();
    if (currentProject) {
      set((state) => ({
        currentProject: { ...state.currentProject!, script },
      }));
    }
  },

  updateScript: (updates) => {
    const { currentProject } = get();
    if (currentProject?.script) {
      set((state) => ({
        currentProject: {
          ...state.currentProject!,
          script: { ...state.currentProject!.script!, ...updates },
        },
      }));
    }
  },

  addScene: (scene) => {
    const { currentProject } = get();
    if (currentProject) {
      const newScene: Scene = {
        ...scene,
        id: crypto.randomUUID(),
      };
      set((state) => ({
        currentProject: {
          ...state.currentProject!,
          scenes: [...state.currentProject!.scenes, newScene],
        },
      }));
    }
  },

  updateScene: (sceneId, updates) => {
    const { currentProject } = get();
    if (currentProject) {
      set((state) => ({
        currentProject: {
          ...state.currentProject!,
          scenes: state.currentProject!.scenes.map((s) =>
            s.id === sceneId ? { ...s, ...updates } : s
          ),
        },
      }));
    }
  },

  deleteScene: (sceneId) => {
    const { currentProject } = get();
    if (currentProject) {
      set((state) => ({
        currentProject: {
          ...state.currentProject!,
          scenes: state.currentProject!.scenes.filter((s) => s.id !== sceneId),
        },
      }));
    }
  },

  addShot: (sceneId, shot) => {
    const { currentProject } = get();
    if (currentProject) {
      const newShot: Shot = {
        ...shot,
        id: crypto.randomUUID(),
      };
      set((state) => ({
        currentProject: {
          ...state.currentProject!,
          scenes: state.currentProject!.scenes.map((s) =>
            s.id === sceneId
              ? { ...s, shots: [...(s.shots || []), newShot] }
              : s
          ),
        },
      }));
    }
  },

  updateShot: (shotId, updates) => {
    const { currentProject } = get();
    if (currentProject) {
      set((state) => ({
        currentProject: {
          ...state.currentProject!,
          scenes: state.currentProject!.scenes.map((s) => ({
            ...s,
            shots: s.shots?.map((shot) =>
              shot.id === shotId ? { ...shot, ...updates } : shot
            ),
          })),
        },
      }));
    }
  },

  deleteShot: (shotId) => {
    const { currentProject } = get();
    if (currentProject) {
      set((state) => ({
        currentProject: {
          ...state.currentProject!,
          scenes: state.currentProject!.scenes.map((s) => ({
            ...s,
            shots: s.shots?.filter((shot) => shot.id !== shotId),
          })),
        },
      }));
    }
  },
}));
