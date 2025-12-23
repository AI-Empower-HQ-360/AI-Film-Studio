import React, { useState } from 'react';
import { projectsAPI, jobsAPI } from '@/lib/api';

interface ScriptEditorProps {
  projectId?: string;
  onJobCreated?: (jobId: string) => void;
}

export default function ScriptEditor({ projectId, onJobCreated }: ScriptEditorProps) {
  const [title, setTitle] = useState('');
  const [script, setScript] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      // Create or update project
      let currentProjectId = projectId;
      
      if (!currentProjectId) {
        const projectResponse = await projectsAPI.create({
          title,
          script,
        });
        currentProjectId = projectResponse.data.id;
        setSuccess('Project created successfully!');
      } else {
        await projectsAPI.update(currentProjectId, {
          title,
          script,
        });
        setSuccess('Project updated successfully!');
      }

      // Create a job for the project
      const jobResponse = await jobsAPI.create({
        project_id: currentProjectId,
        config: {
          music_prompt: 'Cinematic background music',
          video_duration: 9,
          audio_volume: 0.5,
          title,
        },
      });

      setSuccess('Job created successfully! Processing your video...');
      
      if (onJobCreated) {
        onJobCreated(jobResponse.data.id);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create project/job');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-4">Create Your Film</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium mb-2">
            Project Title
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="input"
            placeholder="Enter your film title"
            required
          />
        </div>

        <div>
          <label htmlFor="script" className="block text-sm font-medium mb-2">
            Script / Scene Descriptions
          </label>
          <textarea
            id="script"
            value={script}
            onChange={(e) => setScript(e.target.value)}
            className="textarea"
            placeholder="Describe your scenes... Each line will become a scene in your video."
            rows={10}
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            Tip: Write each scene on a new line for best results
          </p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            {success}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Creating...' : 'Generate Video'}
        </button>
      </form>
    </div>
  );
}
