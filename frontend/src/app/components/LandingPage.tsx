'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Navigation from './Navigation';

export default function LandingPage() {
  const router = useRouter();
  const [script, setScript] = useState('');
  const [showScriptInput, setShowScriptInput] = useState(false);

  const handleQuickStart = () => {
    if (script.trim()) {
      // Save script to session storage and redirect to dashboard
      sessionStorage.setItem('quickStartScript', script);
      router.push('/dashboard');
    } else {
      setShowScriptInput(true);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <Navigation className="fixed top-0 left-0 right-0 z-50" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
            Transform Your Scripts into{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Cinematic Films
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto mb-10">
            AI-powered platform that converts text scripts into stunning short films 
            (30-90 seconds) using cutting-edge AI image and video generation technology.
          </p>

          {/* Quick Script Input Section */}
          {!showScriptInput ? (
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-10">
              <Link href="/signup" className="w-full sm:w-auto bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all shadow-lg shadow-sky-500/25 text-center">
                Start Creating Free
              </Link>
              <button 
                onClick={() => setShowScriptInput(true)}
                className="w-full sm:w-auto bg-slate-700 hover:bg-slate-600 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-colors border border-slate-600"
              >
                Try with Your Script
              </button>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto mb-10">
              <div className="bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 border border-slate-700 shadow-2xl">
                <div className="mb-4">
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    ✨ Paste your script here to get started (up to 10,000 characters)
                  </label>
                  <textarea
                    value={script}
                    onChange={(e) => setScript(e.target.value)}
                    maxLength={10000}
                    placeholder="Example: A hero stands on a cliff at sunset, looking at the vast ocean. The wind blows through their hair as they take a deep breath, ready to face their destiny..."
                    className="w-full h-40 px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20 resize-none"
                  />
                  <div className="flex items-center justify-between mt-2">
                    <span className={`text-sm ${script.length > 9500 ? 'text-orange-400' : 'text-slate-400'}`}>
                      {script.length.toLocaleString()} / 10,000 characters
                    </span>
                    <span className="text-sm text-slate-400">
                      {script.trim() ? '30-90 seconds recommended' : ''}
                    </span>
                  </div>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={handleQuickStart}
                    disabled={!script.trim()}
                    className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all ${
                      script.trim()
                        ? 'bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white shadow-lg shadow-sky-500/25'
                        : 'bg-slate-700 text-slate-400 cursor-not-allowed'
                    }`}
                  >
                    {script.trim() ? '🚀 Create Film Now' : 'Enter script to continue'}
                  </button>
                  <button
                    onClick={() => {
                      setShowScriptInput(false);
                      setScript('');
                    }}
                    className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
              
              {/* Quick Tips */}
              <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
                  <span className="text-xs font-semibold text-sky-400">💡 TIP</span>
                  <p className="text-sm text-slate-300 mt-1">Include visual details</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
                  <span className="text-xs font-semibold text-purple-400">💡 TIP</span>
                  <p className="text-sm text-slate-300 mt-1">Describe emotions & mood</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
                  <span className="text-xs font-semibold text-pink-400">💡 TIP</span>
                  <p className="text-sm text-slate-300 mt-1">Keep it 30-90 seconds</p>
                </div>
              </div>
            </div>
          )}
          
          {/* Hero Image Placeholder */}
          <div className="mt-16 relative">
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 border border-slate-700 shadow-2xl max-w-4xl mx-auto">
              <div className="aspect-video bg-slate-800 rounded-lg flex items-center justify-center border border-slate-600">
                <div className="text-center">
                  <div className="text-6xl mb-4">🎥</div>
                  <p className="text-slate-400">Your AI-generated film preview</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">
            Powerful Features
          </h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-16">
            Everything you need to transform your creative vision into stunning visual content
          </p>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-sky-500/50 transition-colors">
              <div className="w-12 h-12 bg-sky-500/20 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">📝</span>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Script Analysis</h3>
              <p className="text-slate-400">
                AI analyzes your script to identify scenes, characters, and visual elements for optimal generation.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-purple-500/50 transition-colors">
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🎨</span>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Storyboard Generation</h3>
              <p className="text-slate-400">
                Automatically creates visual storyboards using Stable Diffusion XL for each scene.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-pink-500/50 transition-colors">
              <div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🎬</span>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Video Composition</h3>
              <p className="text-slate-400">
                AI composes generated images into smooth video sequences with professional transitions.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-green-500/50 transition-colors">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🎵</span>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Audio Generation</h3>
              <p className="text-slate-400">
                Add AI-generated music and sound effects that match your video&apos;s mood and pacing.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-orange-500/50 transition-colors">
              <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">GPU Acceleration</h3>
              <p className="text-slate-400">
                Powered by enterprise-grade GPU infrastructure for fast, high-quality generation.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-cyan-500/50 transition-colors">
              <div className="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">☁️</span>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Cloud-Native</h3>
              <p className="text-slate-400">
                Built on AWS for reliability, scalability, and global content delivery.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">
            How It Works
          </h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-16">
            From script to screen in four simple steps
          </p>

          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-sky-500 rounded-full flex items-center justify-center text-2xl font-bold text-white mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Upload Script</h3>
              <p className="text-slate-400">
                Paste or upload your text script in any format
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center text-2xl font-bold text-white mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">AI Analysis</h3>
              <p className="text-slate-400">
                AI parses scenes, characters, and visual elements
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-pink-500 rounded-full flex items-center justify-center text-2xl font-bold text-white mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Generate Media</h3>
              <p className="text-slate-400">
                SDXL and video models create your visual content
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center text-2xl font-bold text-white mx-auto mb-4">
                4
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Download Film</h3>
              <p className="text-slate-400">
                Get your finished MP4 ready to share
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center bg-gradient-to-br from-sky-900/50 to-purple-900/50 rounded-2xl p-12 border border-slate-700">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to Create Your First AI Film?
          </h2>
          <p className="text-slate-300 mb-8 max-w-2xl mx-auto">
            Join thousands of creators, filmmakers, and storytellers who are already using AI Film Studio to bring their visions to life.
          </p>
          <Link href="/signup" className="bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all shadow-lg shadow-sky-500/25 inline-block">
            Get Started for Free
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 lg:px-8 border-t border-slate-700">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-purple-500 bg-clip-text text-transparent mb-4 md:mb-0">
              🎬 AI Film Studio
            </div>
            <div className="flex items-center space-x-6 text-slate-400">
              <a href="#" className="hover:text-white transition-colors">Privacy</a>
              <a href="#" className="hover:text-white transition-colors">Terms</a>
              <a href="#" className="hover:text-white transition-colors">Contact</a>
            </div>
          </div>
          <div className="mt-8 text-center text-slate-500 text-sm">
            © 2026 AI Film Studio by AI-Empower-HQ-360. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
