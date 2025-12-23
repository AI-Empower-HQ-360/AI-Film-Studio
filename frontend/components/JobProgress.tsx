import React, { useEffect, useState } from 'react';
import { jobsAPI } from '@/lib/api';

interface Job {
  id: string;
  status: string;
  progress: number;
  error_message?: string;
  output_video_url?: string;
  thumbnail_url?: string;
  created_at: string;
  updated_at: string;
}

interface JobProgressProps {
  jobId: string;
}

const statusColors: Record<string, string> = {
  pending: 'bg-gray-500',
  validating: 'bg-blue-500',
  queued: 'bg-blue-600',
  processing: 'bg-yellow-500',
  generating_images: 'bg-purple-500',
  generating_video: 'bg-purple-600',
  generating_audio: 'bg-indigo-500',
  composing: 'bg-indigo-600',
  completed: 'bg-green-500',
  failed: 'bg-red-500',
  cancelled: 'bg-gray-600',
};

const statusLabels: Record<string, string> = {
  pending: 'Pending',
  validating: 'Validating',
  queued: 'Queued',
  processing: 'Processing',
  generating_images: 'Generating Images',
  generating_video: 'Generating Video',
  generating_audio: 'Generating Audio',
  composing: 'Composing Final Video',
  completed: 'Completed',
  failed: 'Failed',
  cancelled: 'Cancelled',
};

export default function JobProgress({ jobId }: JobProgressProps) {
  const [job, setJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!jobId) return;

    const fetchJob = async () => {
      try {
        const response = await jobsAPI.get(jobId);
        setJob(response.data);
        setIsLoading(false);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch job');
        setIsLoading(false);
      }
    };

    fetchJob();

    // Poll for updates if job is not completed
    const interval = setInterval(() => {
      if (job && !['completed', 'failed', 'cancelled'].includes(job.status)) {
        fetchJob();
      }
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(interval);
  }, [jobId, job?.status]);

  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse">Loading job...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  if (!job) {
    return null;
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-4">Job Progress</h2>
      
      <div className="space-y-4">
        {/* Status Badge */}
        <div className="flex items-center gap-3">
          <span className={`px-3 py-1 rounded-full text-white text-sm font-medium ${statusColors[job.status]}`}>
            {statusLabels[job.status] || job.status}
          </span>
          {!['completed', 'failed', 'cancelled'].includes(job.status) && (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
          )}
        </div>

        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Progress</span>
            <span>{job.progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className={`h-2.5 rounded-full transition-all duration-300 ${
                job.status === 'failed' ? 'bg-red-500' : 'bg-primary-600'
              }`}
              style={{ width: `${job.progress}%` }}
            ></div>
          </div>
        </div>

        {/* Error Message */}
        {job.error_message && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <strong>Error:</strong> {job.error_message}
          </div>
        )}

        {/* Timestamps */}
        <div className="text-sm text-gray-600">
          <p>Created: {new Date(job.created_at).toLocaleString()}</p>
          <p>Updated: {new Date(job.updated_at).toLocaleString()}</p>
        </div>

        {/* Completed - Show Download Button */}
        {job.status === 'completed' && job.output_video_url && (
          <div className="mt-4">
            <button
              onClick={async () => {
                try {
                  const response = await jobsAPI.getDownloadUrl(jobId);
                  window.open(response.data.download_url, '_blank');
                } catch (err) {
                  alert('Failed to get download URL');
                }
              }}
              className="btn-primary w-full"
            >
              Download Video
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
