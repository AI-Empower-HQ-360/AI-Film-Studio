import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Plus, Wand2, Video, ArrowRight, ChevronLeft } from 'lucide-react';
import { useAppStore } from '../store';
import ShotCard from '../components/ShotCard';
import { shotApi } from '../utils/api';
import './Shots.css';

const Shots: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { currentProject, addShot, updateShot, deleteShot } = useAppStore();
  const [selectedSceneId, setSelectedSceneId] = useState<string | null>(
    (location.state as any)?.sceneId || currentProject?.scenes[0]?.id || null
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newShot, setNewShot] = useState({
    shotNumber: 1,
    shotType: 'MEDIUM' as const,
    cameraMovement: 'STATIC' as const,
    description: '',
    dialogue: '',
    duration: 5,
  });

  if (!currentProject || currentProject.scenes.length === 0) {
    return (
      <div className="container">
        <div className="empty-state">
          <Video size={64} />
          <h3>No Scenes Available</h3>
          <p>Please create scenes before adding shots</p>
          <button className="btn btn-primary" onClick={() => navigate('/scenes')}>
            Go to Scenes
          </button>
        </div>
      </div>
    );
  }

  const selectedScene = currentProject.scenes.find((s) => s.id === selectedSceneId);
  const shots = selectedScene?.shots || [];

  const handleGenerateShots = async () => {
    if (!selectedSceneId) return;

    setIsGenerating(true);
    try {
      const generatedShots = await shotApi.generateFromScene(selectedSceneId);
      generatedShots.forEach((shot) => {
        addShot(selectedSceneId, {
          sceneId: selectedSceneId,
          shotNumber: shot.shotNumber,
          shotType: shot.shotType,
          cameraMovement: shot.cameraMovement,
          description: shot.description,
          dialogue: shot.dialogue,
          duration: shot.duration,
        });
      });
    } catch (error) {
      console.error('Failed to generate shots:', error);
      alert('Failed to generate shots. Please try again or add shots manually.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleAddShot = () => {
    if (!selectedSceneId) return;
    
    addShot(selectedSceneId, {
      sceneId: selectedSceneId,
      ...newShot,
    });
    setNewShot({
      shotNumber: shots.length + 2,
      shotType: 'MEDIUM',
      cameraMovement: 'STATIC',
      description: '',
      dialogue: '',
      duration: 5,
    });
    setShowAddModal(false);
  };

  const handleProceedToExport = () => {
    navigate('/export');
  };

  return (
    <div className="container">
      <div className="shots-page">
        <div className="shots-header">
          <div>
            <button className="btn btn-secondary btn-small" onClick={() => navigate('/scenes')}>
              <ChevronLeft size={16} />
              Back to Scenes
            </button>
            <h1>Shot Planning</h1>
            <p className="subtitle">Define individual shots for each scene</p>
          </div>
          <div className="shots-actions">
            <button
              className="btn btn-secondary"
              onClick={handleGenerateShots}
              disabled={isGenerating || !selectedSceneId}
            >
              {isGenerating ? (
                <>Generating...</>
              ) : (
                <>
                  <Wand2 size={20} />
                  AI Generate
                </>
              )}
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => setShowAddModal(true)}
              disabled={!selectedSceneId}
            >
              <Plus size={20} />
              Add Shot
            </button>
            <button
              className="btn btn-primary"
              onClick={handleProceedToExport}
            >
              Proceed to Export
              <ArrowRight size={20} />
            </button>
          </div>
        </div>

        <div className="scene-selector">
          <label>Select Scene:</label>
          <div className="scene-tabs">
            {currentProject.scenes.map((scene) => (
              <button
                key={scene.id}
                className={`scene-tab ${scene.id === selectedSceneId ? 'active' : ''}`}
                onClick={() => setSelectedSceneId(scene.id)}
              >
                <span className="scene-tab-number">Scene {scene.sceneNumber}</span>
                <span className="scene-tab-title">{scene.title}</span>
                <span className="scene-tab-count">{scene.shots?.length || 0} shots</span>
              </button>
            ))}
          </div>
        </div>

        {selectedScene && (
          <div className="selected-scene-info card">
            <div className="scene-info-header">
              <h3>{selectedScene.title}</h3>
              <div className="scene-badges">
                <span className="badge badge-info">{selectedScene.timeOfDay}</span>
                <span className="scene-location">{selectedScene.location}</span>
              </div>
            </div>
            <p>{selectedScene.description}</p>
          </div>
        )}

        {shots.length === 0 ? (
          <div className="empty-state">
            <Video size={64} />
            <h3>No Shots Yet</h3>
            <p>Use AI to automatically generate shots or add them manually</p>
            <div className="empty-actions">
              <button
                className="btn btn-primary"
                onClick={handleGenerateShots}
                disabled={!selectedSceneId}
              >
                <Wand2 size={20} />
                Generate Shots
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => setShowAddModal(true)}
                disabled={!selectedSceneId}
              >
                <Plus size={20} />
                Add Manually
              </button>
            </div>
          </div>
        ) : (
          <div className="shots-grid">
            {shots.map((shot) => (
              <ShotCard
                key={shot.id}
                shot={shot}
                onUpdate={(updates) => updateShot(shot.id, updates)}
                onDelete={() => deleteShot(shot.id)}
              />
            ))}
          </div>
        )}
      </div>

      {showAddModal && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Shot</h2>
            <div className="modal-content">
              <div className="input-group">
                <label>Shot Number</label>
                <input
                  type="number"
                  value={newShot.shotNumber}
                  onChange={(e) => setNewShot({ ...newShot, shotNumber: parseInt(e.target.value) })}
                  min="1"
                />
              </div>
              <div className="shot-type-inputs">
                <div className="input-group">
                  <label>Shot Type</label>
                  <select
                    value={newShot.shotType}
                    onChange={(e) => setNewShot({ ...newShot, shotType: e.target.value as any })}
                  >
                    <option value="WIDE">Wide Shot</option>
                    <option value="MEDIUM">Medium Shot</option>
                    <option value="CLOSE-UP">Close-Up</option>
                    <option value="EXTREME CLOSE-UP">Extreme Close-Up</option>
                    <option value="POV">POV</option>
                    <option value="OVER THE SHOULDER">Over The Shoulder</option>
                  </select>
                </div>
                <div className="input-group">
                  <label>Camera Movement</label>
                  <select
                    value={newShot.cameraMovement}
                    onChange={(e) => setNewShot({ ...newShot, cameraMovement: e.target.value as any })}
                  >
                    <option value="STATIC">Static</option>
                    <option value="PAN">Pan</option>
                    <option value="TILT">Tilt</option>
                    <option value="ZOOM">Zoom</option>
                    <option value="DOLLY">Dolly</option>
                    <option value="TRACKING">Tracking</option>
                  </select>
                </div>
              </div>
              <div className="input-group">
                <label>Duration (seconds)</label>
                <input
                  type="number"
                  value={newShot.duration}
                  onChange={(e) => setNewShot({ ...newShot, duration: parseFloat(e.target.value) })}
                  min="0"
                  step="0.5"
                />
              </div>
              <div className="input-group">
                <label>Description</label>
                <textarea
                  value={newShot.description}
                  onChange={(e) => setNewShot({ ...newShot, description: e.target.value })}
                  placeholder="Describe the shot"
                  rows={3}
                />
              </div>
              <div className="input-group">
                <label>Dialogue (optional)</label>
                <textarea
                  value={newShot.dialogue}
                  onChange={(e) => setNewShot({ ...newShot, dialogue: e.target.value })}
                  placeholder="Any dialogue in this shot"
                  rows={2}
                />
              </div>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowAddModal(false)}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={handleAddShot}
                disabled={!newShot.description.trim()}
              >
                Add Shot
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Shots;
