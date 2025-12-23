import React, { useState } from 'react';
import { Plus, Trash2, Edit2, Save } from 'lucide-react';
import { Scene } from '../types';
import './SceneCard.css';

interface SceneCardProps {
  scene: Scene;
  onUpdate: (updates: Partial<Scene>) => void;
  onDelete: () => void;
  onOpenShots: () => void;
}

const SceneCard: React.FC<SceneCardProps> = ({ scene, onUpdate, onDelete, onOpenShots }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedScene, setEditedScene] = useState(scene);

  const handleSave = () => {
    onUpdate(editedScene);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedScene(scene);
    setIsEditing(false);
  };

  return (
    <div className="scene-card">
      <div className="scene-card-header">
        <div className="scene-number">Scene {scene.sceneNumber}</div>
        <div className="scene-actions">
          {isEditing ? (
            <>
              <button className="btn btn-small btn-primary" onClick={handleSave}>
                <Save size={16} />
                Save
              </button>
              <button className="btn btn-small btn-secondary" onClick={handleCancel}>
                Cancel
              </button>
            </>
          ) : (
            <>
              <button className="btn btn-small btn-secondary" onClick={() => setIsEditing(true)}>
                <Edit2 size={16} />
              </button>
              <button className="btn btn-small btn-danger" onClick={onDelete}>
                <Trash2 size={16} />
              </button>
            </>
          )}
        </div>
      </div>

      {isEditing ? (
        <div className="scene-edit-form">
          <div className="input-group">
            <label>Title</label>
            <input
              type="text"
              value={editedScene.title}
              onChange={(e) => setEditedScene({ ...editedScene, title: e.target.value })}
            />
          </div>
          <div className="scene-meta-row">
            <div className="input-group">
              <label>Location</label>
              <input
                type="text"
                value={editedScene.location}
                onChange={(e) => setEditedScene({ ...editedScene, location: e.target.value })}
              />
            </div>
            <div className="input-group">
              <label>Time</label>
              <select
                value={editedScene.timeOfDay}
                onChange={(e) => setEditedScene({ ...editedScene, timeOfDay: e.target.value as any })}
              >
                <option value="INT">INT</option>
                <option value="EXT">EXT</option>
                <option value="INT/EXT">INT/EXT</option>
              </select>
            </div>
          </div>
          <div className="input-group">
            <label>Description</label>
            <textarea
              value={editedScene.description}
              onChange={(e) => setEditedScene({ ...editedScene, description: e.target.value })}
              rows={3}
            />
          </div>
          <div className="input-group">
            <label>Content</label>
            <textarea
              value={editedScene.content}
              onChange={(e) => setEditedScene({ ...editedScene, content: e.target.value })}
              rows={5}
            />
          </div>
        </div>
      ) : (
        <div className="scene-content">
          <h3 className="scene-title">{scene.title}</h3>
          <div className="scene-meta">
            <span className="badge badge-info">{scene.timeOfDay}</span>
            <span>{scene.location}</span>
          </div>
          <p className="scene-description">{scene.description}</p>
          <div className="scene-text">{scene.content}</div>
          <div className="scene-footer">
            <div className="shots-count">
              {scene.shots?.length || 0} shot{scene.shots?.length !== 1 ? 's' : ''}
            </div>
            <button className="btn btn-primary btn-small" onClick={onOpenShots}>
              <Plus size={16} />
              Manage Shots
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SceneCard;
