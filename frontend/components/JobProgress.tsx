'use client';

import { useState, useEffect } from 'react';
import apiClient from '@/lib/api';
import type { Job } from '@/lib/types';

interface JobProgressProps {
  jobId: number;
}

export default function JobProgress({ jobId }: JobProgressProps) {
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJob();
    
    // Poll for updates every 5 seconds if job is not in terminal state
    const interval = setInterval(() => {
      if (job && !isTerminalState(job.status)) {
        fetchJob();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [jobId]);

  const fetchJob = async () => {
    try {
      const response = await apiClient.get(`/api/v1/jobs/${jobId}`);
      setJob(response.data);
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch job');
      setLoading(false);
    }
  };

  const isTerminalState = (status: string) => {
    return ['completed', 'failed', 'cancelled'].includes(status);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-100';
      case 'failed':
      case 'moderation_failed':
        return 'text-red-600 bg-red-100';
      case 'cancelled':
        return 'text-gray-600 bg-gray-100';
      case 'processing':
        return 'text-blue-600 bg-blue-100';
      default:
        return 'text-yellow-600 bg-yellow-100';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {error}
      </div>
    );
  }

  if (!job) {
    return null;
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Job Progress</h2>

      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium">Status</span>
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(job.status)}`}>
            {job.status.toUpperCase()}
          </span>
        </div>

        <div className="mb-2">
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium">Progress</span>
            <span className="text-sm text-gray-600">{job.progress.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-blue-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${job.progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-gray-50 rounded">
          <p className="text-sm text-gray-600">Job ID</p>
          <p className="font-semibold">{job.id}</p>
        </div>
        <div className="p-4 bg-gray-50 rounded">
          <p className="text-sm text-gray-600">Moderation Status</p>
          <p className="font-semibold capitalize">{job.moderation_status}</p>
        </div>
        <div className="p-4 bg-gray-50 rounded">
          <p className="text-sm text-gray-600">Estimated Cost</p>
          <p className="font-semibold">${job.estimated_cost.toFixed(2)}</p>
        </div>
        <div className="p-4 bg-gray-50 rounded">
          <p className="text-sm text-gray-600">Actual Cost</p>
          <p className="font-semibold">${job.actual_cost.toFixed(2)}</p>
        </div>
      </div>

      {job.error_message && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          <p className="font-semibold">Error:</p>
          <p>{job.error_message}</p>
        </div>
      )}

      <div className="mb-4 p-4 bg-gray-50 rounded">
        <p className="text-sm font-medium text-gray-700 mb-2">Script:</p>
        <p className="text-sm text-gray-600 whitespace-pre-wrap">{job.script}</p>
      </div>

      {job.status === 'completed' && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded">
          <h3 className="font-semibold text-green-800 mb-2">✓ Job Completed!</h3>
          <p className="text-sm text-green-700 mb-3">
            Your film is ready. Click below to download.
          </p>
        </div>
      )}

      <div className="mt-4 text-xs text-gray-500">
        <p>Created: {new Date(job.created_at).toLocaleString()}</p>
        <p>Updated: {new Date(job.updated_at).toLocaleString()}</p>
        {job.completed_at && (
          <p>Completed: {new Date(job.completed_at).toLocaleString()}</p>
        )}
      </div>
    </div>
  );
}
