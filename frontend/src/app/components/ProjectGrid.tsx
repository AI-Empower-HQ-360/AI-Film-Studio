'use client';
import { useState } from 'react';
import Link from 'next/link';

interface FilmProject {
  id: string;
  title: string;
  script: string;
  settings: {
    duration: '30' | '60' | '90';
    style: 'realistic' | 'animated' | 'cinematic' | 'documentary';
    mood: 'dramatic' | 'comedic' | 'suspenseful' | 'romantic' | 'action';
    resolution: '720p' | '1080p' | '4k';
  };
  status: 'draft' | 'processing' | 'completed' | 'failed';
  createdAt: string;
  completedAt?: string;
  thumbnailUrl?: string;
  videoUrl?: string;
}

interface ProjectGridProps {
  projects: FilmProject[];
  onProjectSelect?: (project: FilmProject) => void;
  onProjectDelete?: (projectId: string) => void;
  onProjectEdit?: (project: FilmProject) => void;
}

export default function ProjectGrid({ projects, onProjectSelect, onProjectDelete, onProjectEdit }: ProjectGridProps) {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'name'>('newest');
  const [filterStatus, setFilterStatus] = useState<'all' | 'draft' | 'processing' | 'completed' | 'failed'>('all');

  const getStatusIcon = (status: FilmProject['status']) => {
    switch (status) {
      case 'draft': return '📝';
      case 'processing': return '⚡';
      case 'completed': return '✅';
      case 'failed': return '❌';
      default: return '📄';
    }
  };

  const getStatusColor = (status: FilmProject['status']) => {
    switch (status) {
      case 'draft': return 'text-slate-400 bg-slate-700';
      case 'processing': return 'text-yellow-400 bg-yellow-900/30';
      case 'completed': return 'text-green-400 bg-green-900/30';
      case 'failed': return 'text-red-400 bg-red-900/30';
      default: return 'text-slate-400 bg-slate-700';
    }
  };

  const filteredProjects = projects
    .filter(project => filterStatus === 'all' || project.status === filterStatus)
    .sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
        case 'oldest':
          return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
        case 'name':
          return a.title.localeCompare(b.title);
        default:
          return 0;
      }
    });

  const ProjectCard = ({ project }: { project: FilmProject }) => (
    <div className="bg-slate-800 rounded-lg border border-slate-700 hover:border-slate-600 transition-all group">
      {/* Thumbnail/Preview */}
      <div className="aspect-video bg-slate-900 rounded-t-lg relative overflow-hidden">
        {project.thumbnailUrl ? (
          <img
            src={project.thumbnailUrl}
            alt={project.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-4xl mb-2">{getStatusIcon(project.status)}</div>
              <p className="text-slate-500 text-sm">{project.status === 'processing' ? 'Generating...' : 'No preview'}</p>
            </div>
          </div>
        )}
        
        {/* Status overlay */}
        <div className="absolute top-2 right-2">
          <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(project.status)}`}>
            {project.status === 'processing' && (
              <span className="inline-block w-2 h-2 bg-current rounded-full animate-pulse mr-1"></span>
            )}
            {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
          </span>
        </div>

        {/* Hover overlay */}
        <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <div className="flex gap-2">
            {project.status === 'completed' && (
              <button
                onClick={() => onProjectSelect?.(project)}
                className="px-3 py-2 bg-sky-600 hover:bg-sky-700 text-white rounded text-sm font-medium transition-colors"
              >
                ▶ Play
              </button>
            )}
            <button
              onClick={() => onProjectEdit?.(project)}
              className="px-3 py-2 bg-slate-600 hover:bg-slate-700 text-white rounded text-sm font-medium transition-colors"
            >
              ✎ Edit
            </button>
          </div>
        </div>
      </div>

      {/* Project Info */}
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-semibold text-white truncate mr-2">{project.title}</h3>
          <button
            onClick={() => onProjectDelete?.(project.id)}
            className="text-slate-400 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100"
          >
            🗑️
          </button>
        </div>
        
        <div className="text-sm text-slate-400 space-y-1">
          <div className="flex items-center gap-4">
            <span>{project.settings.duration}s</span>
            <span className="capitalize">{project.settings.style}</span>
            <span>{project.settings.resolution}</span>
          </div>
          <div>
            Created {new Date(project.createdAt).toLocaleDateString()}
          </div>
          {project.completedAt && (
            <div>
              Completed {new Date(project.completedAt).toLocaleDateString()}
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const ProjectListItem = ({ project }: { project: FilmProject }) => (
    <div className="bg-slate-800 rounded-lg border border-slate-700 hover:border-slate-600 transition-all p-4">
      <div className="flex items-center gap-4">
        {/* Thumbnail */}
        <div className="w-24 h-14 bg-slate-900 rounded flex items-center justify-center flex-shrink-0">
          {project.thumbnailUrl ? (
            <img src={project.thumbnailUrl} alt={project.title} className="w-full h-full object-cover rounded" />
          ) : (
            <span className="text-2xl">{getStatusIcon(project.status)}</span>
          )}
        </div>

        {/* Project Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-1">
            <h3 className="font-semibold text-white truncate">{project.title}</h3>
            <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(project.status)}`}>
              {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
            </span>
          </div>
          <div className="text-sm text-slate-400 flex items-center gap-4">
            <span>{project.settings.duration}s</span>
            <span className="capitalize">{project.settings.style}</span>
            <span>{project.settings.resolution}</span>
            <span>•</span>
            <span>{new Date(project.createdAt).toLocaleDateString()}</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          {project.status === 'completed' && (
            <button
              onClick={() => onProjectSelect?.(project)}
              className="px-3 py-1 bg-sky-600 hover:bg-sky-700 text-white rounded text-sm transition-colors"
            >
              ▶ Play
            </button>
          )}
          <button
            onClick={() => onProjectEdit?.(project)}
            className="px-3 py-1 bg-slate-600 hover:bg-slate-700 text-white rounded text-sm transition-colors"
          >
            ✎ Edit
          </button>
          <button
            onClick={() => onProjectDelete?.(project.id)}
            className="text-slate-400 hover:text-red-400 transition-colors p-1"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  );

  if (projects.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🎬</div>
        <h3 className="text-xl font-semibold text-white mb-2">No projects yet</h3>
        <p className="text-slate-400 mb-6">Create your first AI film to get started!</p>
        <Link 
          href="/dashboard?tab=content"
          className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white rounded-lg font-medium transition-all"
        >
          Create Your First Film
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <h2 className="text-xl font-semibold text-white">
            My Projects ({filteredProjects.length})
          </h2>
        </div>
        
        <div className="flex items-center gap-4">
          {/* Filter */}
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value as any)}
            className="px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-sky-500"
          >
            <option value="all">All Status</option>
            <option value="draft">Draft</option>
            <option value="processing">Processing</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>

          {/* Sort */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-sky-500"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="name">Name A-Z</option>
          </select>

          {/* View Mode */}
          <div className="flex rounded-lg border border-slate-600 overflow-hidden">
            <button
              onClick={() => setViewMode('grid')}
              className={`px-3 py-2 text-sm font-medium transition-colors ${
                viewMode === 'grid' 
                  ? 'bg-sky-600 text-white' 
                  : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              ⊞ Grid
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-3 py-2 text-sm font-medium transition-colors ${
                viewMode === 'list' 
                  ? 'bg-sky-600 text-white' 
                  : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              ☰ List
            </button>
          </div>
        </div>
      </div>

      {/* Projects */}
      {viewMode === 'grid' ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredProjects.map(project => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      ) : (
        <div className="space-y-3">
          {filteredProjects.map(project => (
            <ProjectListItem key={project.id} project={project} />
          ))}
        </div>
      )}
    </div>
  );
}