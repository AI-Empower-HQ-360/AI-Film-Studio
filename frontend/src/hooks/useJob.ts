'use client';
import { useState, useCallback, useEffect } from 'react';
import { api, JobStatusResponse } from '@/lib/api';
import { useWebSocket } from './useWebSocket';

export function useJob(jobId: string | null) {
  const [status, setStatus] = useState<JobStatusResponse | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // WebSocket for real-time updates
  const { isConnected, lastMessage } = useWebSocket(jobId, {
    onMessage: (message) => {
      if (message.type === 'job_update') {
        setStatus(message.data);
      }
    },
  });

  // Fallback: Poll for status if WebSocket is not connected
  useEffect(() => {
    if (!jobId || isConnected) return;

    const pollInterval = setInterval(async () => {
      try {
        const jobStatus = await api.getJobStatus(jobId);
        setStatus(jobStatus);

        // Stop polling if job is completed or failed
        if (jobStatus.status === 'completed' || jobStatus.status === 'failed') {
          setIsPolling(false);
          clearInterval(pollInterval);
        }
      } catch (err) {
        console.error('Failed to fetch job status:', err);
      }
    }, 2000);

    setIsPolling(true);

    return () => {
      clearInterval(pollInterval);
      setIsPolling(false);
    };
  }, [jobId, isConnected]);

  const submitJob = useCallback(async (projectId: string) => {
    setError(null);
    try {
      const response = await api.submitJob(projectId);
      return response.job_id;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit job';
      setError(errorMessage);
      throw err;
    }
  }, []);

  const cancelJob = useCallback(async (jobIdToCancel: string) => {
    setError(null);
    try {
      await api.cancelJob(jobIdToCancel);
      setStatus((prev) =>
        prev ? { ...prev, status: 'failed', error_message: 'Cancelled by user' } : null
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to cancel job';
      setError(errorMessage);
      throw err;
    }
  }, []);

  return {
    status,
    isPolling,
    isConnected,
    error,
    submitJob,
    cancelJob,
  };
}
