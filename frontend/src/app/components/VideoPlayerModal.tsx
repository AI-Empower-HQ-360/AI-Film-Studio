'use client';
import { useState, useRef, useEffect } from 'react';
import type { FilmProject } from '../../types/project';

interface VideoPlayerModalProps {
  project: FilmProject | null;
  onClose: () => void;
  onDownload?: (project: FilmProject) => void;
  onShare?: (project: FilmProject) => void;
}

export default function VideoPlayerModal({ project, onClose, onDownload, onShare }: VideoPlayerModalProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [showControls, setShowControls] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const controlsTimeoutRef = useRef<NodeJS.Timeout>();

  // Track fullscreen state
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  useEffect(() => {
    if (!project) return;

    const video = videoRef.current;
    if (!video) return;

    const handleLoadedMetadata = () => {
      setDuration(video.duration);
    };

    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime);
    };

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);

    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);

    return () => {
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
    };
  }, [project]);

  const togglePlayPause = () => {
    const video = videoRef.current;
    if (!video) return;

    if (isPlaying) {
      video.pause();
    } else {
      video.play();
    }
  };

  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    const video = videoRef.current;
    const progressBar = e.currentTarget;
    if (!video || !progressBar) return;

    const rect = progressBar.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const width = rect.width;
    const newTime = (clickX / width) * duration;
    
    video.currentTime = newTime;
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    
    const video = videoRef.current;
    if (video) {
      video.volume = newVolume;
    }
  };

  const toggleFullscreen = () => {
    const container = containerRef.current;
    if (!container) return;

    const isCurrentlyFullscreen = !!document.fullscreenElement;
    if (!isCurrentlyFullscreen) {
      if (container.requestFullscreen) {
        container.requestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const handleMouseMove = () => {
    setShowControls(true);
    if (controlsTimeoutRef.current) {
      clearTimeout(controlsTimeoutRef.current);
    }
    controlsTimeoutRef.current = setTimeout(() => {
      if (isPlaying) {
        setShowControls(false);
      }
    }, 3000);
  };

  const handleDownload = async () => {
    if (!project?.videoUrl) return;
    
    try {
      const response = await fetch(project.videoUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${project.title}.mp4`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      onDownload?.(project);
    } catch (error) {
      console.error('Error downloading video:', error);
    }
  };

  const handleShare = async () => {
    if (!project) return;

    if (navigator.share && project.videoUrl) {
      try {
        await navigator.share({
          title: project.title,
          text: `Check out this AI-generated film: ${project.title}`,
          url: project.videoUrl,
        });
        onShare?.(project);
      } catch (error) {
        console.log('Error sharing:', error);
      }
    } else {
      // Fallback: copy to clipboard
      if (project.videoUrl) {
        navigator.clipboard.writeText(project.videoUrl);
        // You could show a toast notification here
      }
    }
  };

  if (!project) return null;

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center">
      <div 
        ref={containerRef}
        className="w-full h-full flex flex-col"
        onMouseMove={handleMouseMove}
        onMouseLeave={() => setShowControls(true)}
      >
        {/* Header */}
        <div className={`flex items-center justify-between p-4 bg-black/50 transition-all duration-300 ${
          showControls ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-full'
        }`}>
          <div>
            <h2 className="text-xl font-bold text-white">{project.title}</h2>
            <div className="text-sm text-slate-300">
              {project.settings.duration}s • {project.settings.style} • {project.settings.resolution}
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={handleShare}
              className="px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
            >
              📤 Share
            </button>
            <button
              onClick={handleDownload}
              className="px-3 py-2 bg-sky-600 hover:bg-sky-700 text-white rounded-lg transition-colors"
            >
              📥 Download
            </button>
            <button
              onClick={onClose}
              className="text-slate-300 hover:text-white text-xl p-2"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Video Container */}
        <div className="flex-1 flex items-center justify-center relative">
          {project.videoUrl ? (
            <video
              ref={videoRef}
              src={project.videoUrl}
              poster={project.thumbnailUrl}
              className="max-w-full max-h-full"
              onClick={togglePlayPause}
            />
          ) : (
            <div className="text-center">
              <div className="text-6xl mb-4">🎬</div>
              <p className="text-white text-xl mb-2">Video not available</p>
              <p className="text-slate-400">
                {project.status === 'processing' ? 'Still generating...' : 'Video failed to load'}
              </p>
            </div>
          )}

          {/* Play/Pause Overlay */}
          {project.videoUrl && (
            <button
              onClick={togglePlayPause}
              className={`absolute inset-0 flex items-center justify-center bg-black/30 transition-all duration-300 ${
                showControls && !isPlaying ? 'opacity-100' : 'opacity-0'
              }`}
            >
              <div className="bg-black/50 rounded-full p-4">
                <span className="text-white text-4xl">
                  {isPlaying ? '⏸️' : '▶️'}
                </span>
              </div>
            </button>
          )}
        </div>

        {/* Controls */}
        {project.videoUrl && (
          <div className={`bg-black/50 p-4 transition-all duration-300 ${
            showControls ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-full'
          }`}>
            {/* Progress Bar */}
            <div 
              className="w-full h-2 bg-slate-600 rounded-full cursor-pointer mb-4 relative"
              onClick={handleSeek}
            >
              <div 
                className="h-full bg-gradient-to-r from-sky-500 to-purple-500 rounded-full"
                style={{ width: duration ? `${(currentTime / duration) * 100}%` : '0%' }}
              />
              <div 
                className="absolute top-1/2 w-4 h-4 bg-white rounded-full transform -translate-y-1/2 -translate-x-1/2 shadow-lg"
                style={{ left: duration ? `${(currentTime / duration) * 100}%` : '0%' }}
              />
            </div>

            {/* Control Buttons */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button
                  onClick={togglePlayPause}
                  className="text-white hover:text-sky-400 transition-colors"
                >
                  <span className="text-2xl">{isPlaying ? '⏸️' : '▶️'}</span>
                </button>
                
                <div className="text-white text-sm">
                  {formatTime(currentTime)} / {formatTime(duration)}
                </div>

                {/* Volume Control */}
                <div className="flex items-center gap-2">
                  <span className="text-white">🔊</span>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={volume}
                    onChange={handleVolumeChange}
                    className="w-20"
                  />
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={toggleFullscreen}
                  className="text-white hover:text-sky-400 transition-colors text-xl"
                >
                  {isFullscreen ? '⮾' : '⛶'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}