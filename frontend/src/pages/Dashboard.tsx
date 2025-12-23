import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Film, Calendar } from 'lucide-react';
import { useAppStore } from '../store';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { projects, currentProject, createProject, setCurrentProject, deleteProject } = useAppStore();
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');

  const handleCreateProject = () => {
    if (newProjectName.trim()) {
      createProject(newProjectName, newProjectDescription);
      setNewProjectName('');
      setNewProjectDescription('');
      setShowNewProjectModal(false);
      navigate('/script');
    }
  };

  const handleSelectProject = (projectId: string) => {
    const project = projects.find(p => p.id === projectId);
    if (project) {
      setCurrentProject(project);
      navigate('/script');
    }
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'completed':
        return 'badge-success';
      case 'in-progress':
        return 'badge-warning';
      default:
        return 'badge-info';
    }
  };

  return (
    <div className="container">
      <div className="dashboard">
        <div className="dashboard-header">
          <div>
            <h1>Your Projects</h1>
            <p className="subtitle">Create and manage your AI film projects</p>
          </div>
          <button className="btn btn-primary btn-large" onClick={() => setShowNewProjectModal(true)}>
            <Plus size={20} />
            New Project
          </button>
        </div>

        {currentProject && (
          <div className="current-project-banner">
            <div className="current-project-content">
              <div className="current-project-icon">
                <Film size={24} />
              </div>
              <div>
                <div className="current-project-label">Currently Working On</div>
                <h3>{currentProject.name}</h3>
                <p>{currentProject.description}</p>
              </div>
            </div>
            <button className="btn btn-primary" onClick={() => navigate('/script')}>
              Continue Working
            </button>
          </div>
        )}

        <div className="projects-grid">
          {projects.length === 0 ? (
            <div className="empty-state">
              <Film size={64} />
              <h3>No projects yet</h3>
              <p>Create your first AI film project to get started</p>
              <button className="btn btn-primary" onClick={() => setShowNewProjectModal(true)}>
                <Plus size={20} />
                Create First Project
              </button>
            </div>
          ) : (
            projects.map((project) => (
              <div key={project.id} className="project-card" onClick={() => handleSelectProject(project.id)}>
                <div className="project-card-header">
                  <h3>{project.name}</h3>
                  <span className={`badge ${getStatusBadgeClass(project.status)}`}>
                    {project.status}
                  </span>
                </div>
                <p className="project-description">{project.description}</p>
                <div className="project-stats">
                  <div className="project-stat">
                    <span className="stat-value">{project.scenes.length}</span>
                    <span className="stat-label">Scenes</span>
                  </div>
                  <div className="project-stat">
                    <span className="stat-value">
                      {project.scenes.reduce((acc, scene) => acc + (scene.shots?.length || 0), 0)}
                    </span>
                    <span className="stat-label">Shots</span>
                  </div>
                </div>
                <div className="project-footer">
                  <div className="project-date">
                    <Calendar size={14} />
                    {new Date(project.updatedAt).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {showNewProjectModal && (
        <div className="modal-overlay" onClick={() => setShowNewProjectModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Create New Project</h2>
            <div className="modal-content">
              <div className="input-group">
                <label>Project Name</label>
                <input
                  type="text"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="Enter project name"
                  autoFocus
                />
              </div>
              <div className="input-group">
                <label>Description</label>
                <textarea
                  value={newProjectDescription}
                  onChange={(e) => setNewProjectDescription(e.target.value)}
                  placeholder="Enter project description"
                  rows={4}
                />
              </div>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowNewProjectModal(false)}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={handleCreateProject}
                disabled={!newProjectName.trim()}
              >
                Create Project
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
