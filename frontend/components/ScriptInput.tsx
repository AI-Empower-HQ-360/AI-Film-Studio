'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/api';
import type { JobCreateData } from '@/lib/types';

interface ScriptInputProps {
  projectId: number;
  onJobCreated?: (jobId: number) => void;
}

export default function ScriptInput({ projectId, onJobCreated }: ScriptInputProps) {
  const [script, setScript] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const jobData: JobCreateData = {
        project_id: projectId,
        script: script,
        config: {
          num_images: 10,
          video_duration: 30,
          include_voice: true,
          include_music: true,
        },
      };

      const response = await apiClient.post('/api/v1/jobs/', jobData);
      const job = response.data;

      if (onJobCreated) {
        onJobCreated(job.id);
      }

      // Navigate to job progress page
      router.push(`/jobs/${job.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Create Film from Script</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="script" className="block text-sm font-medium text-gray-700 mb-2">
            Film Script
          </label>
          <textarea
            id="script"
            value={script}
            onChange={(e) => setScript(e.target.value)}
            rows={12}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your film script here... Each line will be converted to a scene."
            required
          />
          <p className="mt-2 text-sm text-gray-500">
            Tip: Write each scene on a separate line for better results.
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !script.trim()}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating Job...' : 'Generate Film'}
        </button>
      </form>

      <div className="mt-6 p-4 bg-gray-50 rounded-md">
        <h3 className="font-semibold mb-2">What happens next?</h3>
        <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
          <li>Your script will be moderated for content safety</li>
          <li>Images will be generated for each scene</li>
          <li>Video will be composed with transitions</li>
          <li>Voice narration will be synthesized</li>
          <li>Background music will be added</li>
          <li>Final video will be ready for download</li>
        </ul>
      </div>
    </div>
  );
}
