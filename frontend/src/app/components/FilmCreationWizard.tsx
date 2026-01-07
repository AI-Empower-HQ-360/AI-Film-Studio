'use client';
import { useState, useRef } from 'react';

interface FilmProject {
  id: string;
  title: string;
  script: string;
  settings: {
    duration: '30' | '45' | '60' | '90';
    style: 'realistic' | 'animated' | 'cinematic' | 'documentary';
    mood: 'dramatic' | 'comedic' | 'suspenseful' | 'romantic' | 'action';
    resolution: '720p' | '1080p' | '4k';
  };
  status: 'draft' | 'processing' | 'completed' | 'failed';
}

interface FilmCreationWizardProps {
  onClose?: () => void;
  onProjectCreate?: (project: FilmProject) => void;
}

export default function FilmCreationWizard({ onClose, onProjectCreate }: FilmCreationWizardProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [projectData, setProjectData] = useState<Partial<FilmProject>>({
    title: '',
    script: '',
    settings: {
      duration: '60',
      style: 'cinematic',
      mood: 'dramatic',
      resolution: '1080p'
    },
    status: 'draft'
  });

  const totalSteps = 4;

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'text/plain') {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setProjectData(prev => ({
          ...prev,
          script: content,
          title: prev.title || file.name.replace('.txt', '')
        }));
      };
      reader.readAsText(file);
    }
  };

  const handleGenerateFilm = async () => {
    setIsProcessing(true);
    try {
      // In a real app, this would call your API
      const newProject: FilmProject = {
        id: Date.now().toString(),
        title: projectData.title || 'Untitled Project',
        script: projectData.script || '',
        settings: projectData.settings!,
        status: 'processing'
      };
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      onProjectCreate?.(newProject);
      onClose?.();
    } catch (error) {
      console.error('Error generating film:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">Create Your Film</h2>
              <p className="text-slate-400">Let&apos;s start with your script and basic details</p>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Project Title
              </label>
              <input
                type="text"
                value={projectData.title || ''}
                onChange={(e) => setProjectData(prev => ({ ...prev, title: e.target.value }))}
                placeholder="My Awesome Film"
                className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Script
              </label>
              <div className="space-y-3">
                <textarea
                  value={projectData.script || ''}
                  onChange={(e) => setProjectData(prev => ({ ...prev, script: e.target.value }))}
                  placeholder="Enter your script here... Describe scenes, characters, and dialogue."
                  rows={8}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-sky-500 resize-none"
                />
                <div className="flex items-center justify-between">
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
                  >
                    📄 Upload Script File
                  </button>
                  <span className="text-sm text-slate-400">
                    {projectData.script?.length || 0} characters
                  </span>
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">Film Settings</h2>
              <p className="text-slate-400">Configure how your film will be generated</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-3">Duration</label>
                <div className="space-y-2">
                  {[
                    { value: '30', label: '30 seconds - Quick & punchy' },
                    { value: '60', label: '60 seconds - Balanced storytelling' },
                    { value: '90', label: '90 seconds - Detailed narrative' }
                  ].map((option) => (
                    <label key={option.value} className="flex items-center space-x-3 cursor-pointer">
                      <input
                        type="radio"
                        name="duration"
                        value={option.value}
                        checked={projectData.settings?.duration === option.value}
                        onChange={(e) => setProjectData(prev => ({
                          ...prev,
                          settings: { ...prev.settings!, duration: e.target.value as '30' | '45' | '60' | '90' }
                        }))}
                        className="text-sky-500 focus:ring-sky-500"
                      />
                      <span className="text-slate-300">{option.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-3">Visual Style</label>
                <select
                  value={projectData.settings?.style || 'cinematic'}
                  onChange={(e) => setProjectData(prev => ({
                    ...prev,
                    settings: { ...prev.settings!, style: e.target.value as 'realistic' | 'animated' | 'cinematic' | 'documentary' }
                  }))}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="realistic">Realistic</option>
                  <option value="animated">Animated</option>
                  <option value="cinematic">Cinematic</option>
                  <option value="documentary">Documentary</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-3">Mood/Tone</label>
                <select
                  value={projectData.settings?.mood || 'dramatic'}
                  onChange={(e) => setProjectData(prev => ({
                    ...prev,
                    settings: { ...prev.settings!, mood: e.target.value as 'dramatic' | 'comedic' | 'suspenseful' | 'romantic' | 'action' }
                  }))}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="dramatic">Dramatic</option>
                  <option value="comedic">Comedic</option>
                  <option value="suspenseful">Suspenseful</option>
                  <option value="romantic">Romantic</option>
                  <option value="action">Action</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-3">Resolution</label>
                <select
                  value={projectData.settings?.resolution || '1080p'}
                  onChange={(e) => setProjectData(prev => ({
                    ...prev,
                    settings: { ...prev.settings!, resolution: e.target.value as '720p' | '1080p' | '4k' }
                  }))}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="720p">720p (Faster generation)</option>
                  <option value="1080p">1080p (Balanced quality)</option>
                  <option value="4k">4K (Highest quality)</option>
                </select>
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">Review & Preview</h2>
              <p className="text-slate-400">Check your project details before generation</p>
            </div>

            <div className="bg-slate-800 rounded-lg p-6 space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">{projectData.title}</h3>
                <div className="grid md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-slate-400">Duration:</span>
                    <span className="text-white ml-2">{projectData.settings?.duration}s</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Style:</span>
                    <span className="text-white ml-2 capitalize">{projectData.settings?.style}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Mood:</span>
                    <span className="text-white ml-2 capitalize">{projectData.settings?.mood}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Resolution:</span>
                    <span className="text-white ml-2">{projectData.settings?.resolution}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="text-white font-medium mb-2">Script Preview:</h4>
                <div className="bg-slate-900 p-4 rounded border border-slate-600 max-h-32 overflow-y-auto">
                  <p className="text-slate-300 text-sm whitespace-pre-wrap">
                    {projectData.script?.slice(0, 300)}
                    {(projectData.script?.length || 0) > 300 && '...'}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-900/20 border border-yellow-700/50 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <span className="text-yellow-400 text-xl">⚡</span>
                <div>
                  <h4 className="text-yellow-400 font-medium">Generation Time</h4>
                  <p className="text-slate-300 text-sm">
                    Estimated generation time: 3-5 minutes. You&apos;ll receive a notification when your film is ready.
                  </p>
                </div>
              </div>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="text-center space-y-6">
            {isProcessing ? (
              <>
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-sky-500 mx-auto"></div>
                <h2 className="text-2xl font-bold text-white">Generating Your Film...</h2>
                <p className="text-slate-400">AI is analyzing your script and creating your film. This may take a few minutes.</p>
                <div className="bg-slate-800 rounded-lg p-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-300">Progress</span>
                    <span className="text-sky-400">Processing...</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2 mt-2">
                    <div className="bg-gradient-to-r from-sky-500 to-purple-500 h-2 rounded-full animate-pulse" style={{ width: '45%' }}></div>
                  </div>
                </div>
              </>
            ) : (
              <>
                <div className="text-6xl mb-4">🎬</div>
                <h2 className="text-2xl font-bold text-white">Ready to Generate!</h2>
                <p className="text-slate-400 max-w-md mx-auto">
                  Your film settings look great. Click the button below to start the AI generation process.
                </p>
              </>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return projectData.title?.trim() && projectData.script?.trim();
      case 2:
        return true; // Settings have defaults
      case 3:
        return true;
      case 4:
        return !isProcessing;
      default:
        return false;
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 rounded-xl border border-slate-700 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <div className="flex items-center gap-4">
            <h1 className="text-xl font-bold text-white">Film Creation Wizard</h1>
            <div className="flex items-center gap-2">
              {Array.from({ length: totalSteps }, (_, i) => (
                <div
                  key={i}
                  className={`w-2 h-2 rounded-full transition-colors ${
                    i + 1 <= currentStep ? 'bg-sky-500' : 'bg-slate-600'
                  }`}
                />
              ))}
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors"
            disabled={isProcessing}
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-6 min-h-96">
          {renderStep()}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-slate-700">
          <div className="text-sm text-slate-400">
            Step {currentStep} of {totalSteps}
          </div>
          
          <div className="flex gap-3">
            {currentStep > 1 && (
              <button
                onClick={handleBack}
                disabled={isProcessing}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 text-white rounded-lg transition-colors"
              >
                Back
              </button>
            )}
            
            {currentStep < totalSteps ? (
              <button
                onClick={handleNext}
                disabled={!canProceed() || isProcessing}
                className="px-6 py-2 bg-sky-600 hover:bg-sky-700 disabled:opacity-50 text-white rounded-lg transition-colors"
              >
                Next
              </button>
            ) : (
              <button
                onClick={handleGenerateFilm}
                disabled={!canProceed()}
                className="px-6 py-2 bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 disabled:opacity-50 text-white rounded-lg transition-all"
              >
                {isProcessing ? 'Generating...' : 'Generate Film'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}