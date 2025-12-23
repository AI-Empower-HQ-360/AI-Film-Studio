'use client';

import { useState } from 'react';
import apiClient from '@/lib/api';

interface DownloadButtonProps {
  jobId: number;
}

export default function DownloadButton({ jobId }: DownloadButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDownload = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/api/v1/jobs/signed-url', {
        job_id: jobId,
      });

      const { url, expires_at } = response.data;

      // Open download link in new tab
      window.open(url, '_blank');

      // Show expiration time
      const expiresDate = new Date(expires_at);
      alert(`Download link expires at: ${expiresDate.toLocaleString()}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate download link');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      <button
        onClick={handleDownload}
        disabled={loading}
        className="w-full bg-green-600 text-white py-3 px-6 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            Generating Download Link...
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download Video
          </>
        )}
      </button>

      <p className="mt-2 text-sm text-gray-600 text-center">
        Download link will expire in 1 hour
      </p>
    </div>
  );
}
