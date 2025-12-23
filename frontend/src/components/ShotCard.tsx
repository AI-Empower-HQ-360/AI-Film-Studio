import React, { useState } from 'react';
import { Trash2, Edit2, Save, Image as ImageIcon } from 'lucide-react';
import { Shot } from '../types';
import './ShotCard.css';

interface ShotCardProps {
  shot: Shot;
  onUpdate: (updates: Partial<Shot>) => void;
  onDelete: () => void;
}

const ShotCard: React.FC<ShotCardProps> = ({ shot, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedShot, setEditedShot] = useState(shot);

  const handleSave = () => {
    onUpdate(editedShot);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedShot(shot);
    setIsEditing(false);
  };

  return (
    <div className="shot-card">
      <div className="shot-card-header">
        <div className="shot-number">Shot {shot.shotNumber}</div>
        <div className="shot-actions">
          {isEditing ? (
            <>
              <button className="btn btn-small btn-primary" onClick={handleSave}>
                <Save size={16} />
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
        <div className="shot-edit-form">
          <div className="input-group">
            <label>Shot Type</label>
            <select
              value={editedShot.shotType}
              onChange={(e) => setEditedShot({ ...editedShot, shotType: e.target.value as any })}
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
              value={editedShot.cameraMovement}
              onChange={(e) => setEditedShot({ ...editedShot, cameraMovement: e.target.value as any })}
            >
              <option value="STATIC">Static</option>
              <option value="PAN">Pan</option>
              <option value="TILT">Tilt</option>
              <option value="ZOOM">Zoom</option>
              <option value="DOLLY">Dolly</option>
              <option value="TRACKING">Tracking</option>
            </select>
          </div>
          <div className="input-group">
            <label>Duration (seconds)</label>
            <input
              type="number"
              value={editedShot.duration}
              onChange={(e) => setEditedShot({ ...editedShot, duration: parseFloat(e.target.value) })}
              min="0"
              step="0.5"
            />
          </div>
          <div className="input-group">
            <label>Description</label>
            <textarea
              value={editedShot.description}
              onChange={(e) => setEditedShot({ ...editedShot, description: e.target.value })}
              rows={3}
            />
          </div>
          <div className="input-group">
            <label>Dialogue (optional)</label>
            <textarea
              value={editedShot.dialogue || ''}
              onChange={(e) => setEditedShot({ ...editedShot, dialogue: e.target.value })}
              rows={2}
            />
          </div>
        </div>
      ) : (
        <div className="shot-content">
          {shot.imageUrl && (
            <div className="shot-image">
              <img src={shot.imageUrl} alt={`Shot ${shot.shotNumber}`} />
            </div>
          )}
          {!shot.imageUrl && (
            <div className="shot-placeholder">
              <ImageIcon size={48} />
              <span>No preview available</span>
            </div>
          )}
          <div className="shot-meta">
            <span className="badge badge-info">{shot.shotType}</span>
            <span className="badge badge-secondary">{shot.cameraMovement}</span>
            <span className="shot-duration">{shot.duration}s</span>
          </div>
          <p className="shot-description">{shot.description}</p>
          {shot.dialogue && (
            <div className="shot-dialogue">
              <strong>Dialogue:</strong> {shot.dialogue}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ShotCard;
