import React, { useEffect, useState } from 'react';
import { jobsAPI } from '@/lib/api';

interface Job {
  id: string;
  status: string;
  progress: number;
  output_video_url?: string;
  thumbnail_url?: string;
  created_at: string;
}

interface VideoPreviewProps {
  jobId: string;
}

export default function VideoPreview({ jobId }: VideoPreviewProps) {
  const [job, setJob] = useState<Job | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await jobsAPI.get(jobId);
        setJob(response.data);
        
        // If completed, get download URL
        if (response.data.status === 'completed') {
          const urlResponse = await jobsAPI.getDownloadUrl(jobId);
          setDownloadUrl(urlResponse.data.download_url);
        }
      } catch (err) {
        console.error('Failed to fetch job:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchJob();
  }, [jobId]);

  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse">Loading video...</div>
      </div>
    );
  }

  if (!job || job.status !== 'completed') {
    return (
      <div className="card">
        <p className="text-gray-600">Video not ready yet. Current status: {job?.status}</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-4">Video Preview</h2>
      
      {/* Video Player */}
      <div className="mb-4">
        {downloadUrl ? (
          <video
            controls
            className="w-full rounded-lg"
            poster={job.thumbnail_url}
          >
            <source src={downloadUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        ) : (
          <div className="bg-gray-200 aspect-video flex items-center justify-center rounded-lg">
            <p className="text-gray-600">Video preview not available</p>
          </div>
        )}
      </div>

      {/* Download Button */}
      <div className="flex gap-2">
        <button
          onClick={() => {
            if (downloadUrl) {
              window.open(downloadUrl, '_blank');
            }
          }}
          className="btn-primary flex-1"
          disabled={!downloadUrl}
        >
          Download Video
        </button>
        
        {job.thumbnail_url && (
          <button
            onClick={() => window.open(job.thumbnail_url, '_blank')}
            className="btn-secondary"
          >
            Download Thumbnail
          </button>
        )}
      </div>

      {/* Video Info */}
      <div className="mt-4 text-sm text-gray-600">
        <p>Created: {new Date(job.created_at).toLocaleString()}</p>
        <p>Job ID: {job.id}</p>
      </div>
    </div>
  );
}
