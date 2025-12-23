'use client';

import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/auth';
import ScriptEditor from '@/components/ScriptEditor';
import JobProgress from '@/components/JobProgress';
import VideoPreview from '@/components/VideoPreview';

export default function Home() {
  const { user, isLoading: authLoading, loadUser, login, register, logout } = useAuthStore();
  const [currentJobId, setCurrentJobId] = useState<string>('');
  const [showAuth, setShowAuth] = useState<'login' | 'register'>('login');
  
  // Form states
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (showAuth === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName);
      }
    } catch (err) {
      // Error is handled in the store
    }
  };

  if (authLoading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse">Loading...</div>
      </main>
    );
  }

  if (!user) {
    return (
      <main className="min-h-screen flex items-center justify-center p-4">
        <div className="card max-w-md w-full">
          <h1 className="text-3xl font-bold mb-6 text-center">AI Film Studio Hub</h1>
          
          <form onSubmit={handleAuth} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                required
              />
            </div>

            {showAuth === 'register' && (
              <div>
                <label htmlFor="fullName" className="block text-sm font-medium mb-2">
                  Full Name
                </label>
                <input
                  id="fullName"
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="input"
                />
              </div>
            )}

            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                required
              />
            </div>

            <button type="submit" className="btn-primary w-full">
              {showAuth === 'login' ? 'Login' : 'Register'}
            </button>
          </form>

          <div className="mt-4 text-center">
            <button
              onClick={() => setShowAuth(showAuth === 'login' ? 'register' : 'login')}
              className="text-primary-600 hover:underline text-sm"
            >
              {showAuth === 'login'
                ? 'Need an account? Register'
                : 'Already have an account? Login'}
            </button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold mb-2">AI Film Studio Hub</h1>
            <p className="text-gray-600">Welcome, {user.email}</p>
          </div>
          <button onClick={logout} className="btn-secondary">
            Logout
          </button>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Script Editor */}
          <div>
            <ScriptEditor onJobCreated={setCurrentJobId} />
          </div>

          {/* Right Column - Job Progress & Video Preview */}
          <div className="space-y-8">
            {currentJobId && (
              <>
                <JobProgress jobId={currentJobId} />
                <VideoPreview jobId={currentJobId} />
              </>
            )}
            {!currentJobId && (
              <div className="card">
                <p className="text-gray-600 text-center">
                  Create a project to see job progress and video preview here.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
