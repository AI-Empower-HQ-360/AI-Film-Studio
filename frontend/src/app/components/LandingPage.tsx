'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Navigation from './Navigation';

export default function LandingPage() {
  const router = useRouter();
  const [script, setScript] = useState('');
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [showScriptInput, setShowScriptInput] = useState(false);
  const [inputMode, setInputMode] = useState<'script' | 'youtube'>('script');

  const validateYoutubeUrl = (url: string) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;
    return youtubeRegex.test(url);
  };

  const handleQuickStart = () => {
    if (inputMode === 'script' && script.trim()) {
      sessionStorage.setItem('quickStartScript', script);
      router.push('/dashboard');
    } else if (inputMode === 'youtube' && youtubeUrl.trim() && validateYoutubeUrl(youtubeUrl)) {
      sessionStorage.setItem('quickStartYoutubeUrl', youtubeUrl);
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
                {/* Mode Toggle */}
                <div className="flex gap-2 mb-4 bg-slate-900 rounded-lg p-1">
                  <button
                    onClick={() => setInputMode('script')}
                    className={`flex-1 px-4 py-2 rounded-md font-medium transition-all ${
                      inputMode === 'script'
                        ? 'bg-gradient-to-r from-sky-500 to-purple-600 text-white shadow-lg'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    📝 Write Script
                  </button>
                  <button
                    onClick={() => setInputMode('youtube')}
                    className={`flex-1 px-4 py-2 rounded-md font-medium transition-all ${
                      inputMode === 'youtube'
                        ? 'bg-gradient-to-r from-red-500 to-pink-600 text-white shadow-lg'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    🎥 YouTube Reference
                  </button>
                </div>

                {inputMode === 'script' ? (
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
                ) : (
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      🎬 Paste a YouTube URL to use as creative reference
                    </label>
                    <input
                      type="url"
                      value={youtubeUrl}
                      onChange={(e) => setYoutubeUrl(e.target.value)}
                      placeholder="https://www.youtube.com/watch?v=..."
                      className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20"
                    />
                    <div className="mt-3 bg-blue-900/30 border border-blue-700/50 rounded-lg p-3">
                      <div className="flex items-start gap-2">
                        <span className="text-blue-400 text-lg">ℹ️</span>
                        <div>
                          <p className="text-sm text-blue-200 font-medium">How it works:</p>
                          <p className="text-xs text-slate-300 mt-1">
                            AI will analyze the video as creative inspiration and generate <strong>brand new original content</strong> with unique characters and storyline. No content will be copied.
                          </p>
                        </div>
                      </div>
                    </div>
                    {youtubeUrl && !validateYoutubeUrl(youtubeUrl) && (
                      <p className="text-sm text-red-400 mt-2">Please enter a valid YouTube URL</p>
                    )}
                  </div>
                )}

                <div className="flex gap-3">
                  <button
                    onClick={handleQuickStart}
                    disabled={
                      inputMode === 'script' 
                        ? !script.trim() 
                        : !youtubeUrl.trim() || !validateYoutubeUrl(youtubeUrl)
                    }
                    className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all ${
                      (inputMode === 'script' ? script.trim() : youtubeUrl.trim() && validateYoutubeUrl(youtubeUrl))
                        ? 'bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white shadow-lg shadow-sky-500/25'
                        : 'bg-slate-700 text-slate-400 cursor-not-allowed'
                    }`}
                  >
                    {(inputMode === 'script' ? script.trim() : youtubeUrl.trim() && validateYoutubeUrl(youtubeUrl))
                      ? '🚀 Create Film Now' 
                      : inputMode === 'script' 
                        ? 'Enter script to continue' 
                        : 'Enter YouTube URL to continue'}
                  </button>
                  <button
                    onClick={() => {
                      setShowScriptInput(false);
                      setScript('');
                      setYoutubeUrl('');
                      setInputMode('script');
                    }}
                    className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
              
              {/* Quick Tips */}
              <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
                {inputMode === 'script' ? (
                  <>
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
                  </>
                ) : (
                  <>
                    <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
                      <span className="text-xs font-semibold text-red-400">🎬 TIP</span>
                      <p className="text-sm text-slate-300 mt-1">Use as inspiration only</p>
                    </div>
                    <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
                      <span className="text-xs font-semibold text-pink-400">✨ TIP</span>
                      <p className="text-sm text-slate-300 mt-1">AI creates original content</p>
                    </div>
                    <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
                      <span className="text-xs font-semibold text-orange-400">🎨 TIP</span>
                      <p className="text-sm text-slate-300 mt-1">New characters & story</p>
                    </div>
                  </>
                )}
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

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold bg-gradient-to-r from-sky-400 to-purple-500 bg-clip-text text-transparent mb-2">
                10K+
              </div>
              <p className="text-slate-400">Films Created</p>
            </div>
            <div>
              <div className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent mb-2">
                30-90s
              </div>
              <p className="text-slate-400">Generation Time</p>
            </div>
            <div>
              <div className="text-4xl font-bold bg-gradient-to-r from-pink-400 to-orange-500 bg-clip-text text-transparent mb-2">
                99.9%
              </div>
              <p className="text-slate-400">Uptime</p>
            </div>
            <div>
              <div className="text-4xl font-bold bg-gradient-to-r from-green-400 to-cyan-500 bg-clip-text text-transparent mb-2">
                4K
              </div>
              <p className="text-slate-400">Max Resolution</p>
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

      {/* Use Cases Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">
            Perfect For
          </h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-16">
            Transform your creative ideas across multiple industries
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 hover:border-sky-500/50 transition-all hover:transform hover:scale-105">
              <div className="text-4xl mb-4">🎥</div>
              <h3 className="text-xl font-semibold text-white mb-3">Content Creators</h3>
              <p className="text-slate-400 mb-4">
                Create engaging social media videos, YouTube content, and promotional materials in minutes.
              </p>
              <ul className="space-y-2 text-sm text-slate-400">
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Social media videos
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> YouTube intros
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Brand storytelling
                </li>
              </ul>
            </div>

            <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 hover:border-purple-500/50 transition-all hover:transform hover:scale-105">
              <div className="text-4xl mb-4">🏢</div>
              <h3 className="text-xl font-semibold text-white mb-3">Businesses</h3>
              <p className="text-slate-400 mb-4">
                Generate marketing videos, product demos, and training materials cost-effectively.
              </p>
              <ul className="space-y-2 text-sm text-slate-400">
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Product demos
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Training videos
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Ad campaigns
                </li>
              </ul>
            </div>

            <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 hover:border-pink-500/50 transition-all hover:transform hover:scale-105">
              <div className="text-4xl mb-4">🎬</div>
              <h3 className="text-xl font-semibold text-white mb-3">Filmmakers</h3>
              <p className="text-slate-400 mb-4">
                Rapid prototyping, storyboarding, and concept visualization for your next project.
              </p>
              <ul className="space-y-2 text-sm text-slate-400">
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Storyboard previews
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Concept pitches
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Visual prototypes
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-4">
            Powered by Cutting-Edge AI
          </h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-16">
            Built on enterprise-grade technology stack for reliability and performance
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 text-center">
              <div className="text-3xl mb-3">🎨</div>
              <h4 className="text-lg font-semibold text-white mb-2">Stable Diffusion XL</h4>
              <p className="text-sm text-slate-400">High-quality image generation</p>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 text-center">
              <div className="text-3xl mb-3">☁️</div>
              <h4 className="text-lg font-semibold text-white mb-2">AWS Cloud</h4>
              <p className="text-sm text-slate-400">Scalable infrastructure</p>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 text-center">
              <div className="text-3xl mb-3">⚡</div>
              <h4 className="text-lg font-semibold text-white mb-2">GPU Acceleration</h4>
              <p className="text-sm text-slate-400">Fast processing power</p>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 text-center">
              <div className="text-3xl mb-3">🔒</div>
              <h4 className="text-lg font-semibold text-white mb-2">Enterprise Security</h4>
              <p className="text-sm text-slate-400">Your data protected</p>
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
      <footer className="py-16 px-4 sm:px-6 lg:px-8 border-t border-slate-700 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            {/* Brand Column */}
            <div className="md:col-span-1">
              <div className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-purple-500 bg-clip-text text-transparent mb-4">
                🎬 AI Film Studio
              </div>
              <p className="text-slate-400 text-sm mb-4">
                Transform your scripts into cinematic short films using cutting-edge AI technology.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="text-slate-400 hover:text-sky-400 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
                <a href="#" className="text-slate-400 hover:text-purple-400 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="text-slate-400 hover:text-pink-400 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="text-slate-400 hover:text-red-400 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                </a>
              </div>
            </div>

            {/* Product Column */}
            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-3 text-sm">
                <li><Link href="#features" className="text-slate-400 hover:text-white transition-colors">Features</Link></li>
                <li><Link href="/pricing" className="text-slate-400 hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="/dashboard" className="text-slate-400 hover:text-white transition-colors">Dashboard</Link></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">API Access</a></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Documentation</a></li>
              </ul>
            </div>

            {/* Company Column */}
            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-3 text-sm">
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Press Kit</a></li>
              </ul>
            </div>

            {/* Legal Column */}
            <div>
              <h3 className="text-white font-semibold mb-4">Legal</h3>
              <ul className="space-y-3 text-sm">
                <li><Link href="/privacy" className="text-slate-400 hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link href="/terms" className="text-slate-400 hover:text-white transition-colors">Terms of Service</Link></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">Cookie Policy</a></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">GDPR</a></li>
                <li><a href="#" className="text-slate-400 hover:text-white transition-colors">License</a></li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="pt-8 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between">
            <div className="text-slate-500 text-sm mb-4 md:mb-0">
              © 2026 AI Film Studio by AI-Empower-HQ-360. All rights reserved.
            </div>
            <div className="flex items-center gap-6 text-sm text-slate-400">
              <span>Made with ❤️ using AWS, Next.js & Stable Diffusion</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
