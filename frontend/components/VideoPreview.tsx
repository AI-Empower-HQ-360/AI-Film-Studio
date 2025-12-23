'use client';

import { useState } from 'react';

interface VideoPreviewProps {
  videoUrl: string;
  title?: string;
}

export default function VideoPreview({ videoUrl, title = 'Video Preview' }: VideoPreviewProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>

      <div className="relative w-full bg-black rounded-lg overflow-hidden" style={{ paddingTop: '56.25%' }}>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
          </div>
        )}

        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
            <div className="text-white text-center p-4">
              <p className="text-lg mb-2">Failed to load video</p>
              <p className="text-sm text-gray-400">The video might be processing or unavailable</p>
            </div>
          </div>
        )}

        <video
          className="absolute top-0 left-0 w-full h-full"
          controls
          onLoadedData={() => setIsLoading(false)}
          onError={() => {
            setIsLoading(false);
            setError(true);
          }}
        >
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      <div className="mt-4 flex justify-between items-center">
        <div className="text-sm text-gray-600">
          <p>Format: MP4</p>
          <p>Quality: HD (1080p)</p>
        </div>
      </div>
    </div>
  );
}
