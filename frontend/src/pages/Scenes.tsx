import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Wand2, Clapperboard, ArrowRight } from 'lucide-react';
import { useAppStore } from '../store';
import SceneCard from '../components/SceneCard';
import { sceneApi } from '../utils/api';
import './Scenes.css';

const Scenes: React.FC = () => {
  const navigate = useNavigate();
  const { currentProject, addScene, updateScene, deleteScene } = useAppStore();
  const [isGenerating, setIsGenerating] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newScene, setNewScene] = useState({
    sceneNumber: (currentProject?.scenes.length || 0) + 1,
    title: '',
    description: '',
    location: '',
    timeOfDay: 'INT' as const,
    content: '',
  });

  if (!currentProject) {
    return (
      <div className="container">
        <div className="empty-state">
          <Clapperboard size={64} />
          <h3>No Project Selected</h3>
          <p>Please create or select a project from the dashboard</p>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const handleGenerateScenes = async () => {
    if (!currentProject.script?.content) {
      alert('Please write a script first');
      navigate('/script');
      return;
    }

    setIsGenerating(true);
    try {
      const scenes = await sceneApi.breakdownScript(currentProject.script.content);
      scenes.forEach((scene) => {
        addScene({
          scriptId: currentProject.script!.id,
          sceneNumber: scene.sceneNumber,
          title: scene.title,
          description: scene.description,
          location: scene.location,
          timeOfDay: scene.timeOfDay,
          content: scene.content,
        });
      });
    } catch (error) {
      console.error('Failed to generate scenes:', error);
      alert('Failed to generate scenes. Please try again or add scenes manually.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleAddScene = () => {
    addScene({
      scriptId: currentProject.script?.id || '',
      ...newScene,
    });
    setNewScene({
      sceneNumber: (currentProject?.scenes.length || 0) + 2,
      title: '',
      description: '',
      location: '',
      timeOfDay: 'INT',
      content: '',
    });
    setShowAddModal(false);
  };

  const handleProceedToShots = () => {
    navigate('/shots');
  };

  return (
    <div className="container">
      <div className="scenes-page">
        <div className="scenes-header">
          <div>
            <h1>Scene Breakdown</h1>
            <p className="subtitle">Break down your script into individual scenes</p>
          </div>
          <div className="scenes-actions">
            <button
              className="btn btn-secondary"
              onClick={handleGenerateScenes}
              disabled={isGenerating || !currentProject.script?.content}
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
            <button className="btn btn-secondary" onClick={() => setShowAddModal(true)}>
              <Plus size={20} />
              Add Scene
            </button>
            <button
              className="btn btn-primary"
              onClick={handleProceedToShots}
              disabled={currentProject.scenes.length === 0}
            >
              Proceed to Shots
              <ArrowRight size={20} />
            </button>
          </div>
        </div>

        {currentProject.scenes.length === 0 ? (
          <div className="empty-state">
            <Clapperboard size={64} />
            <h3>No Scenes Yet</h3>
            <p>Use AI to automatically break down your script or add scenes manually</p>
            <div className="empty-actions">
              <button
                className="btn btn-primary"
                onClick={handleGenerateScenes}
                disabled={!currentProject.script?.content}
              >
                <Wand2 size={20} />
                Generate from Script
              </button>
              <button className="btn btn-secondary" onClick={() => setShowAddModal(true)}>
                <Plus size={20} />
                Add Manually
              </button>
            </div>
          </div>
        ) : (
          <div className="scenes-grid">
            {currentProject.scenes.map((scene) => (
              <SceneCard
                key={scene.id}
                scene={scene}
                onUpdate={(updates) => updateScene(scene.id, updates)}
                onDelete={() => deleteScene(scene.id)}
                onOpenShots={() => navigate('/shots', { state: { sceneId: scene.id } })}
              />
            ))}
          </div>
        )}
      </div>

      {showAddModal && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Scene</h2>
            <div className="modal-content">
              <div className="input-group">
                <label>Scene Number</label>
                <input
                  type="number"
                  value={newScene.sceneNumber}
                  onChange={(e) => setNewScene({ ...newScene, sceneNumber: parseInt(e.target.value) })}
                  min="1"
                />
              </div>
              <div className="input-group">
                <label>Title</label>
                <input
                  type="text"
                  value={newScene.title}
                  onChange={(e) => setNewScene({ ...newScene, title: e.target.value })}
                  placeholder="Enter scene title"
                />
              </div>
              <div className="scene-meta-inputs">
                <div className="input-group">
                  <label>Location</label>
                  <input
                    type="text"
                    value={newScene.location}
                    onChange={(e) => setNewScene({ ...newScene, location: e.target.value })}
                    placeholder="e.g., Coffee Shop"
                  />
                </div>
                <div className="input-group">
                  <label>Time of Day</label>
                  <select
                    value={newScene.timeOfDay}
                    onChange={(e) => setNewScene({ ...newScene, timeOfDay: e.target.value as any })}
                  >
                    <option value="INT">Interior</option>
                    <option value="EXT">Exterior</option>
                    <option value="INT/EXT">Int/Ext</option>
                  </select>
                </div>
              </div>
              <div className="input-group">
                <label>Description</label>
                <textarea
                  value={newScene.description}
                  onChange={(e) => setNewScene({ ...newScene, description: e.target.value })}
                  placeholder="Brief scene description"
                  rows={3}
                />
              </div>
              <div className="input-group">
                <label>Content</label>
                <textarea
                  value={newScene.content}
                  onChange={(e) => setNewScene({ ...newScene, content: e.target.value })}
                  placeholder="Scene dialogue and action"
                  rows={5}
                />
              </div>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowAddModal(false)}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={handleAddScene}
                disabled={!newScene.title.trim()}
              >
                Add Scene
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Scenes;
