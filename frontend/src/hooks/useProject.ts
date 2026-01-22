'use client';
import { useState, useCallback } from 'react';
import { api } from '@/lib/api';
import type { FilmProject } from '@/types/project';

export function useProject() {
  const [projects, setProjects] = useState<FilmProject[]>([]);
  const [currentProject, setCurrentProject] = useState<FilmProject | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getProjects();
      setProjects(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch projects');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchProject = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getProject(id);
      setCurrentProject(data);
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch project');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createProject = useCallback(async (projectData: Partial<FilmProject>) => {
    setIsLoading(true);
    setError(null);
    try {
      const newProject = await api.createProject({
        title: projectData.title || 'Untitled Project',
        script: projectData.script || '',
        settings: projectData.settings!,
        metadata: projectData.metadata,
      });
      setProjects((prev) => [newProject, ...prev]);
      return newProject;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateProject = useCallback(
    async (id: string, updates: Partial<FilmProject>) => {
      setIsLoading(true);
      setError(null);
      try {
        const updated = await api.updateProject(id, updates);
        setProjects((prev) =>
          prev.map((p) => (p.id === id ? updated : p))
        );
        if (currentProject?.id === id) {
          setCurrentProject(updated);
        }
        return updated;
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to update project');
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [currentProject]
  );

  const deleteProject = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.deleteProject(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
      if (currentProject?.id === id) {
        setCurrentProject(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete project');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [currentProject]);

  return {
    projects,
    currentProject,
    isLoading,
    error,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
  };
}
