import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Download, Video, Film, ChevronLeft, Play, Settings } from 'lucide-react';
import { useAppStore } from '../store';
import { VideoExportSettings } from '../types';
import { videoApi } from '../utils/api';
import './Export.css';

const Export: React.FC = () => {
  const navigate = useNavigate();
  const { currentProject } = useAppStore();
  const [exportSettings, setExportSettings] = useState<VideoExportSettings>({
    resolution: '1080p',
    fps: 30,
    format: 'mp4',
    quality: 'high',
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [videoPreviewUrl, setVideoPreviewUrl] = useState<string | null>(null);

  if (!currentProject) {
    return (
      <div className="container">
        <div className="empty-state">
          <Film size={64} />
          <h3>No Project Selected</h3>
          <p>Please create or select a project from the dashboard</p>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const totalScenes = currentProject.scenes.length;
  const totalShots = currentProject.scenes.reduce((acc, scene) => acc + (scene.shots?.length || 0), 0);
  const totalDuration = currentProject.scenes.reduce(
    (acc, scene) => acc + (scene.shots?.reduce((sum, shot) => sum + shot.duration, 0) || 0),
    0
  );

  const handleGenerateVideo = async () => {
    setIsGenerating(true);
    setGenerationProgress(0);

    try {
      const result = await videoApi.generate(currentProject.id);
      
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setGenerationProgress((prev) => {
          if (prev >= 100) {
            clearInterval(progressInterval);
            return 100;
          }
          return prev + 10;
        });
      }, 1000);

      // In a real application, you would poll the status endpoint
      setTimeout(() => {
        clearInterval(progressInterval);
        setGenerationProgress(100);
        setVideoPreviewUrl(result.videoUrl);
        setIsGenerating(false);
      }, 10000);
    } catch (error) {
      console.error('Failed to generate video:', error);
      alert('Failed to generate video. Please try again.');
      setIsGenerating(false);
    }
  };

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const blob = await videoApi.export(currentProject.id, exportSettings);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${currentProject.name.replace(/\s+/g, '_')}.${exportSettings.format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to export video:', error);
      alert('Failed to export video. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="container">
      <div className="export-page">
        <div className="export-header">
          <div>
            <button className="btn btn-secondary btn-small" onClick={() => navigate('/shots')}>
              <ChevronLeft size={16} />
              Back to Shots
            </button>
            <h1>Video Export</h1>
            <p className="subtitle">Generate and export your final video</p>
          </div>
        </div>

        <div className="export-layout">
          <div className="export-main">
            <div className="card project-summary">
              <h3>Project Summary</h3>
              <div className="summary-grid">
                <div className="summary-item">
                  <Film size={24} />
                  <div>
                    <div className="summary-label">Project</div>
                    <div className="summary-value">{currentProject.name}</div>
                  </div>
                </div>
                <div className="summary-item">
                  <Video size={24} />
                  <div>
                    <div className="summary-label">Scenes</div>
                    <div className="summary-value">{totalScenes}</div>
                  </div>
                </div>
                <div className="summary-item">
                  <Play size={24} />
                  <div>
                    <div className="summary-label">Shots</div>
                    <div className="summary-value">{totalShots}</div>
                  </div>
                </div>
                <div className="summary-item">
                  <Settings size={24} />
                  <div>
                    <div className="summary-label">Duration</div>
                    <div className="summary-value">{Math.floor(totalDuration / 60)}m {Math.floor(totalDuration % 60)}s</div>
                  </div>
                </div>
              </div>
            </div>

            {videoPreviewUrl ? (
              <div className="card video-preview">
                <h3>Video Preview</h3>
                <div className="video-player">
                  <video controls src={videoPreviewUrl}>
                    Your browser does not support the video tag.
                  </video>
                </div>
              </div>
            ) : (
              <div className="card generate-section">
                <div className="generate-content">
                  <Video size={64} />
                  <h3>Generate Your Video</h3>
                  <p>Click the button below to generate your film from the scenes and shots you've created.</p>
                  
                  {isGenerating && (
                    <div className="progress-section">
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{ width: `${generationProgress}%` }}
                        />
                      </div>
                      <div className="progress-text">{generationProgress}% Complete</div>
                    </div>
                  )}

                  <button
                    className="btn btn-primary btn-large"
                    onClick={handleGenerateVideo}
                    disabled={isGenerating || totalShots === 0}
                  >
                    {isGenerating ? 'Generating Video...' : 'Generate Video'}
                  </button>
                </div>
              </div>
            )}
          </div>

          <div className="export-sidebar">
            <div className="card export-settings">
              <h3>Export Settings</h3>
              <div className="settings-form">
                <div className="input-group">
                  <label>Resolution</label>
                  <select
                    value={exportSettings.resolution}
                    onChange={(e) =>
                      setExportSettings({ ...exportSettings, resolution: e.target.value as any })
                    }
                  >
                    <option value="720p">720p (HD)</option>
                    <option value="1080p">1080p (Full HD)</option>
                    <option value="4k">4K (Ultra HD)</option>
                  </select>
                </div>

                <div className="input-group">
                  <label>Frame Rate</label>
                  <select
                    value={exportSettings.fps}
                    onChange={(e) =>
                      setExportSettings({ ...exportSettings, fps: parseInt(e.target.value) as any })
                    }
                  >
                    <option value="24">24 FPS (Cinematic)</option>
                    <option value="30">30 FPS (Standard)</option>
                    <option value="60">60 FPS (Smooth)</option>
                  </select>
                </div>

                <div className="input-group">
                  <label>Format</label>
                  <select
                    value={exportSettings.format}
                    onChange={(e) =>
                      setExportSettings({ ...exportSettings, format: e.target.value as any })
                    }
                  >
                    <option value="mp4">MP4</option>
                    <option value="mov">MOV</option>
                    <option value="avi">AVI</option>
                  </select>
                </div>

                <div className="input-group">
                  <label>Quality</label>
                  <select
                    value={exportSettings.quality}
                    onChange={(e) =>
                      setExportSettings({ ...exportSettings, quality: e.target.value as any })
                    }
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="ultra">Ultra</option>
                  </select>
                </div>
              </div>
            </div>

            <button
              className="btn btn-primary btn-large export-button"
              onClick={handleExport}
              disabled={!videoPreviewUrl || isExporting}
            >
              <Download size={20} />
              {isExporting ? 'Exporting...' : 'Export Video'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Export;
