'use client';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { useAuth } from '../lib/AuthContext';
import Navigation from '../components/Navigation';
import FilmCreationWizard from '../components/FilmCreationWizard';
import ProjectGrid from '../components/ProjectGrid';
import VideoPlayerModal from '../components/VideoPlayerModal';

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const searchParams = useSearchParams();
  const [activeTab, setActiveTab] = useState('overview');
  const [showFilmWizard, setShowFilmWizard] = useState(false);
  const [selectedProject, setSelectedProject] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);

  // Handle tab switching via URL parameters
  useEffect(() => {
    const tab = searchParams.get('tab');
    if (tab && ['overview', 'content', 'usage', 'account'].includes(tab)) {
      setActiveTab(tab);
    }
  }, [searchParams]);

  // Redirect to sign in if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      window.location.href = '/signin';
    }
  }, [isLoading, isAuthenticated]);

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Don't render dashboard if not authenticated
  if (!isAuthenticated || !user) {
    return null;
  }

  // Mock data - in a real app, this would come from an API
  const userStats = {
    totalFilms: 24,
    monthlyGenerations: 12,
    monthlyLimit: 25,
    remainingCredits: 13,
    subscriptionPlan: 'Standard',
    memberSince: 'December 2025'
  };

  // Initialize mock projects
  useEffect(() => {
    const mockProjects = [
      {
        id: '1',
        title: 'Epic Adventure Trailer',
        script: 'A hero embarks on an epic journey to save the kingdom from darkness...',
        settings: {
          duration: '60' as const,
          style: 'cinematic' as const,
          mood: 'dramatic' as const,
          resolution: '1080p' as const,
        },
        status: 'completed' as const,
        createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        completedAt: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        thumbnailUrl: '/api/placeholder/400/225',
        videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
      },
      {
        id: '2',
        title: 'Mystery Horror Scene',
        script: 'In a dark and stormy night, strange sounds echo through the abandoned mansion...',
        settings: {
          duration: '45' as const,
          style: 'realistic' as const,
          mood: 'suspenseful' as const,
          resolution: '1080p' as const,
        },
        status: 'processing' as const,
        createdAt: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: '3',
        title: 'Romantic Comedy Short',
        script: 'Two people meet in a coffee shop and sparks fly in the most unexpected way...',
        settings: {
          duration: '30' as const,
          style: 'animated' as const,
          mood: 'comedic' as const,
          resolution: '720p' as const,
        },
        status: 'draft' as const,
        createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: '4',
        title: 'Action Sequence',
        script: 'Cars chase through the city streets in an adrenaline-pumping sequence...',
        settings: {
          duration: '90' as const,
          style: 'cinematic' as const,
          mood: 'action' as const,
          resolution: '4k' as const,
        },
        status: 'completed' as const,
        createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
        completedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        thumbnailUrl: '/api/placeholder/400/225',
        videoUrl: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4'
      }
    ];
    setProjects(mockProjects);
  }, []);

  const handleCreateProject = (project: any) => {
    setProjects(prev => [project, ...prev]);
  };

  const handleProjectSelect = (project: any) => {
    setSelectedProject(project);
  };

  const handleProjectDelete = (projectId: string) => {
    setProjects(prev => prev.filter(p => p.id !== projectId));
  };

  const handleProjectEdit = (project: any) => {
    // In a real app, this would open an edit modal or navigate to an edit page
    console.log('Edit project:', project);
  };

  // Account Information
  const accountInfo = {
    email: 'creator@example.com',
    lastLogin: '2 hours ago',
    accountType: 'Standard',
    twoFactorEnabled: true,
    emailVerified: true
  };

  // Usage Data
  const usageData = {
    totalGpuHours: 24.5,
    averageJobDuration: '3.2 min',
    creditsConsumed: 187,
    totalCredits: 250,
    storageUsed: '2.4 GB',
    storageLimit: '10 GB'
  };

  // Content Statistics
  const contentStats = {
    totalScripts: 45,
    uploadedImages: 23,
    generatedVideos: 18,
    generatedImages: 142,
    audioFiles: 12
  };

  const recentFilms = [
    {
      id: 1,
      title: 'Epic Adventure Trailer',
      status: 'Completed',
      createdAt: '2 hours ago',
      thumbnail: '🎬',
      duration: '45s'
    },
    {
      id: 2,
      title: 'Mystery Horror Scene',
      status: 'Processing',
      createdAt: '5 hours ago',
      thumbnail: '🎭',
      duration: '60s'
    },
    {
      id: 3,
      title: 'Romantic Comedy Intro',
      status: 'Completed',
      createdAt: '1 day ago',
      thumbnail: '❤️',
      duration: '30s'
    },
    {
      id: 4,
      title: 'Sci-Fi Action Sequence',
      status: 'Failed',
      createdAt: '2 days ago',
      thumbnail: '🚀',
      duration: '75s'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'Processing':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'Failed':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      default:
        return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  const templates = [
    { id: 1, name: 'Action Thriller', icon: '⚡', description: 'High-energy action sequences' },
    { id: 2, name: 'Romance Drama', icon: '💕', description: 'Emotional storytelling' },
    { id: 3, name: 'Comedy Sketch', icon: '😄', description: 'Light-hearted humor' },
    { id: 4, name: 'Sci-Fi Epic', icon: '🌌', description: 'Futuristic adventures' },
    { id: 5, name: 'Horror Mystery', icon: '👻', description: 'Suspenseful thrills' },
    { id: 6, name: 'Documentary', icon: '📹', description: 'Real-world narratives' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      {/* Navigation */}
      <Navigation currentPage="dashboard" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Welcome back, {user.firstName}! 🎥</h1>
          <p className="text-slate-400">Manage your films and create new cinematic experiences</p>
          
          {/* Tab Navigation */}
          <div className="mt-6 border-b border-slate-700">
            <div className="flex space-x-8">
              {[
                { id: 'overview', label: 'Overview', icon: '📊' },
                { id: 'content', label: 'My Content', icon: '🎬' },
                { id: 'usage', label: 'Usage & Analytics', icon: '📈' },
                { id: 'account', label: 'Account', icon: '⚙️' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`pb-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-sky-500 text-sky-400'
                      : 'border-transparent text-slate-400 hover:text-slate-300'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content - Conditional Rendering Based on Active Tab */}
        {activeTab === 'overview' && (
          <>
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">Total Films</p>
                    <p className="text-2xl font-bold text-white">{userStats.totalFilms}</p>
                  </div>
                  <div className="w-12 h-12 bg-sky-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🎬</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">This Month</p>
                    <p className="text-2xl font-bold text-white">{userStats.monthlyGenerations}/{userStats.monthlyLimit}</p>
                  </div>
                  <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">📊</span>
                  </div>
                </div>
                <div className="mt-3">
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-sky-500 to-purple-600 h-2 rounded-full" 
                      style={{ width: `${(userStats.monthlyGenerations / userStats.monthlyLimit) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">Plan</p>
                    <p className="text-2xl font-bold text-white">{userStats.subscriptionPlan}</p>
                  </div>
                  <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">⭐</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">Member Since</p>
                    <p className="text-lg font-bold text-white">{userStats.memberSince}</p>
                  </div>
                  <div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🎯</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions and Recent Films */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 mb-8">
                  <h2 className="text-xl font-semibold text-white mb-6">Quick Actions</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <button className="bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white p-4 rounded-xl font-semibold transition-all shadow-lg shadow-sky-500/25 text-left">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">✨</span>
                        <div>
                          <p className="font-semibold">Create New Film</p>
                          <p className="text-sm opacity-80">Start with a script or template</p>
                        </div>
                      </div>
                    </button>

                    <button className="bg-slate-700 hover:bg-slate-600 text-white p-4 rounded-xl font-semibold transition-colors border border-slate-600 text-left">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">📂</span>
                        <div>
                          <p className="font-semibold">My Films</p>
                          <p className="text-sm opacity-80">View all your creations</p>
                        </div>
                      </div>
                    </button>
                  </div>
                </div>

                {/* Recent Films */}
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-semibold text-white">Recent Films</h2>
                    <button 
                      onClick={() => setActiveTab('content')} 
                      className="text-sky-400 hover:text-sky-300 transition-colors text-sm"
                    >
                      View All
                    </button>
                  </div>

                  <div className="space-y-4">
                    {recentFilms.map((film) => (
                      <div key={film.id} className="bg-slate-700/30 border border-slate-600 rounded-lg p-4 hover:bg-slate-700/50 transition-colors">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <span className="text-2xl">{film.thumbnail}</span>
                            <div>
                              <h3 className="font-semibold text-white">{film.title}</h3>
                              <p className="text-slate-400 text-sm">{film.createdAt} • {film.duration}</p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-3">
                            <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(film.status)}`}>
                              {film.status}
                            </span>
                            <button className="text-slate-400 hover:text-white transition-colors">
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                {/* Templates */}
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                  <h2 className="text-xl font-semibold text-white mb-4">Film Templates</h2>
                  <div className="grid grid-cols-2 gap-3">
                    {templates.map((template) => (
                      <button
                        key={template.id}
                        className="bg-slate-700/30 hover:bg-slate-700/50 border border-slate-600 rounded-lg p-3 transition-colors text-left"
                      >
                        <div className="text-center">
                          <span className="text-2xl block mb-2">{template.icon}</span>
                          <p className="text-white text-sm font-medium mb-1">{template.name}</p>
                          <p className="text-slate-400 text-xs">{template.description}</p>
                        </div>
                      </button>
                    ))}
                  </div>
                  
                  {/* Create Film Action */}
                  <div className="mt-6">
                    <button
                      onClick={() => setShowFilmWizard(true)}
                      className="w-full bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-4 py-3 rounded-lg font-medium transition-all shadow-lg shadow-sky-500/25"
                    >
                      🎬 Create New Film
                    </button>
                  </div>
                </div>

                {/* Usage & Billing */}
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                  <h2 className="text-xl font-semibold text-white mb-4">Usage & Billing</h2>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-slate-400 text-sm">Monthly Usage</span>
                        <span className="text-white font-semibold">{userStats.monthlyGenerations}/{userStats.monthlyLimit}</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-sky-500 to-purple-600 h-2 rounded-full" 
                          style={{ width: `${(userStats.monthlyGenerations / userStats.monthlyLimit) * 100}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-slate-600">
                      <Link 
                        href="/pricing" 
                        className="w-full bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-4 py-3 rounded-lg font-medium transition-all shadow-lg shadow-sky-500/25 text-center block"
                      >
                        Upgrade Plan
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Content Tab */}
        {activeTab === 'content' && (
          <div className="space-y-6">
            {/* Create New Film Button */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-white">My Films</h1>
                <p className="text-slate-400">Manage and create your AI-generated films</p>
              </div>
              <button
                onClick={() => setShowFilmWizard(true)}
                className="px-6 py-3 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white rounded-lg font-medium transition-all shadow-lg shadow-sky-500/25"
              >
                + Create New Film
              </button>
            </div>

            {/* Project Grid */}
            <ProjectGrid
              projects={projects}
              onProjectSelect={handleProjectSelect}
              onProjectDelete={handleProjectDelete}
              onProjectEdit={handleProjectEdit}
            />
          </div>
        )}

        {/* Usage & Analytics Tab */}
        {activeTab === 'usage' && (
          <div className="space-y-8">
            {/* Usage Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">GPU Hours Used</p>
                    <p className="text-2xl font-bold text-white">{usageData.totalGpuHours}h</p>
                  </div>
                  <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">⚡</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">Avg Job Duration</p>
                    <p className="text-2xl font-bold text-white">{usageData.averageJobDuration}</p>
                  </div>
                  <div className="w-12 h-12 bg-sky-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">⏱️</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">Credits Used</p>
                    <p className="text-2xl font-bold text-white">{usageData.creditsConsumed}</p>
                  </div>
                  <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🏆</span>
                  </div>
                </div>
                <div className="mt-3">
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-sky-500 to-purple-600 h-2 rounded-full" 
                      style={{ width: `${(usageData.creditsConsumed / usageData.totalCredits) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm">Success Rate</p>
                    <p className="text-2xl font-bold text-white">94%</p>
                  </div>
                  <div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">📈</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Detailed Usage Data */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-6">Job Duration Analytics</h2>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Shortest Job</span>
                    <span className="text-white font-semibold">45s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Longest Job</span>
                    <span className="text-white font-semibold">8m 32s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Average Queue Time</span>
                    <span className="text-white font-semibold">2m 15s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Peak Usage Hour</span>
                    <span className="text-white font-semibold">2-3 PM EST</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-6">Resource Consumption</h2>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-slate-400 text-sm">GPU Memory Usage</span>
                      <span className="text-white font-semibold">8.2 GB avg</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-purple-500 to-pink-600 h-2 rounded-full" style={{ width: '68%' }}></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-slate-400 text-sm">CPU Usage</span>
                      <span className="text-white font-semibold">45% avg</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-sky-500 to-purple-600 h-2 rounded-full" style={{ width: '45%' }}></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-slate-400 text-sm">Network I/O</span>
                      <span className="text-white font-semibold">1.2 GB</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-green-500 to-sky-600 h-2 rounded-full" style={{ width: '32%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Account Tab */}
        {activeTab === 'account' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="space-y-6">
              {/* Account Information */}
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-6">Account Information</h2>
                <div className="space-y-4">
                  <div className="flex justify-between items-center py-3 border-b border-slate-600">
                    <div>
                      <p className="text-white font-medium">Email Address</p>
                      <p className="text-slate-400 text-sm">{accountInfo.email}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      {accountInfo.emailVerified && (
                        <span className="text-green-400 text-sm">✓ Verified</span>
                      )}
                      <button className="text-sky-400 hover:text-sky-300 text-sm">Edit</button>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center py-3 border-b border-slate-600">
                    <div>
                      <p className="text-white font-medium">Last Login</p>
                      <p className="text-slate-400 text-sm">{accountInfo.lastLogin}</p>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center py-3 border-b border-slate-600">
                    <div>
                      <p className="text-white font-medium">Account Type</p>
                      <p className="text-slate-400 text-sm">{accountInfo.accountType} Plan</p>
                    </div>
                    <Link href="/pricing" className="text-sky-400 hover:text-sky-300 text-sm">
                      Upgrade
                    </Link>
                  </div>
                  
                  <div className="flex justify-between items-center py-3">
                    <div>
                      <p className="text-white font-medium">Two-Factor Authentication</p>
                      <p className="text-slate-400 text-sm">
                        {accountInfo.twoFactorEnabled ? 'Enabled' : 'Disabled'}
                      </p>
                    </div>
                    <button className="text-sky-400 hover:text-sky-300 text-sm">
                      {accountInfo.twoFactorEnabled ? 'Disable' : 'Enable'}
                    </button>
                  </div>
                </div>
              </div>

              {/* Payment Information */}
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-6">Payment Information</h2>
                <div className="space-y-4">
                  <div className="bg-slate-700/30 border border-slate-600 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">💳</span>
                        <div>
                          <h3 className="font-semibold text-white">Payment Method</h3>
                          <p className="text-slate-400 text-sm">•••• •••• •••• 4242</p>
                        </div>
                      </div>
                      <button className="text-sky-400 hover:text-sky-300 transition-colors text-sm">Update</button>
                    </div>
                  </div>
                  
                  <div className="bg-slate-700/30 border border-slate-600 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">📊</span>
                        <div>
                          <h3 className="font-semibold text-white">Billing History</h3>
                          <p className="text-slate-400 text-sm">View past invoices and payments</p>
                        </div>
                      </div>
                      <button className="text-sky-400 hover:text-sky-300 transition-colors text-sm">View</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              {/* Security Settings */}
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-6">Security & Privacy</h2>
                <div className="space-y-4">
                  <button className="w-full bg-slate-700/30 hover:bg-slate-700/50 border border-slate-600 rounded-lg p-4 text-left transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">🔒</span>
                        <div>
                          <h3 className="font-semibold text-white">Change Password</h3>
                          <p className="text-slate-400 text-sm">Update your account password</p>
                        </div>
                      </div>
                      <span className="text-slate-400">→</span>
                    </div>
                  </button>
                  
                  <button className="w-full bg-slate-700/30 hover:bg-slate-700/50 border border-slate-600 rounded-lg p-4 text-left transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">🛡️</span>
                        <div>
                          <h3 className="font-semibold text-white">Privacy Settings</h3>
                          <p className="text-slate-400 text-sm">Manage data sharing preferences</p>
                        </div>
                      </div>
                      <span className="text-slate-400">→</span>
                    </div>
                  </button>
                  
                  <button className="w-full bg-slate-700/30 hover:bg-slate-700/50 border border-slate-600 rounded-lg p-4 text-left transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">📱</span>
                        <div>
                          <h3 className="font-semibold text-white">Active Sessions</h3>
                          <p className="text-slate-400 text-sm">Manage logged in devices</p>
                        </div>
                      </div>
                      <span className="text-slate-400">→</span>
                    </div>
                  </button>
                </div>
              </div>

              {/* Data Export & Deletion */}
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-6">Data Management</h2>
                <div className="space-y-4">
                  <button className="w-full bg-slate-700/30 hover:bg-slate-700/50 border border-slate-600 rounded-lg p-4 text-left transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">📦</span>
                        <div>
                          <h3 className="font-semibold text-white">Export Data</h3>
                          <p className="text-slate-400 text-sm">Download all your content and data</p>
                        </div>
                      </div>
                      <span className="text-slate-400">→</span>
                    </div>
                  </button>
                  
                  <button className="w-full bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 rounded-lg p-4 text-left transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">🗑️</span>
                        <div>
                          <h3 className="font-semibold text-red-400">Delete Account</h3>
                          <p className="text-red-300/70 text-sm">Permanently delete your account and data</p>
                        </div>
                      </div>
                      <span className="text-red-400">→</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Modals */}
      {showFilmWizard && (
        <FilmCreationWizard
          onClose={() => setShowFilmWizard(false)}
          onProjectCreate={handleCreateProject}
        />
      )}
      
      {selectedProject && (
        <VideoPlayerModal
          project={selectedProject}
          onClose={() => setSelectedProject(null)}
          onDownload={(project) => console.log('Download:', project)}
          onShare={(project) => console.log('Share:', project)}
        />
      )}
    </div>
  );
}