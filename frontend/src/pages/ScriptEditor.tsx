import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Save, Wand2, FileText, ArrowRight } from 'lucide-react';
import { useAppStore } from '../store';
import { scriptApi } from '../utils/api';
import './ScriptEditor.css';

const ScriptEditor: React.FC = () => {
  const navigate = useNavigate();
  const { currentProject, setScript } = useAppStore();
  const [content, setContent] = useState(currentProject?.script?.content || '');
  const [title, setTitle] = useState(currentProject?.script?.title || '');
  const [author, setAuthor] = useState(currentProject?.script?.author || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatePrompt, setGeneratePrompt] = useState('');

  if (!currentProject) {
    return (
      <div className="container">
        <div className="empty-state">
          <FileText size={64} />
          <h3>No Project Selected</h3>
          <p>Please create or select a project from the dashboard</p>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const handleSave = () => {
    const script = {
      id: currentProject.script?.id || crypto.randomUUID(),
      title,
      content,
      author,
      createdAt: currentProject.script?.createdAt || new Date(),
      updatedAt: new Date(),
    };
    setScript(script);
  };

  const handleGenerate = async () => {
    if (!generatePrompt.trim()) return;
    
    setIsGenerating(true);
    try {
      const script = await scriptApi.generate(generatePrompt);
      setTitle(script.title);
      setContent(script.content);
      setAuthor(script.author);
      setGeneratePrompt('');
    } catch (error) {
      console.error('Failed to generate script:', error);
      alert('Failed to generate script. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleProceedToScenes = () => {
    handleSave();
    navigate('/scenes');
  };

  const wordCount = content.split(/\s+/).filter(w => w.length > 0).length;
  const estimatedMinutes = Math.ceil(wordCount / 250);

  return (
    <div className="container">
      <div className="script-editor">
        <div className="script-header">
          <div>
            <h1>Script Editor</h1>
            <p className="subtitle">Write or generate your film script</p>
          </div>
          <div className="script-actions">
            <button className="btn btn-secondary" onClick={handleSave}>
              <Save size={20} />
              Save Script
            </button>
            <button
              className="btn btn-primary"
              onClick={handleProceedToScenes}
              disabled={!content.trim()}
            >
              Proceed to Scenes
              <ArrowRight size={20} />
            </button>
          </div>
        </div>

        <div className="script-generator card">
          <div className="generator-header">
            <Wand2 size={24} />
            <div>
              <h3>AI Script Generator</h3>
              <p>Describe your story idea and let AI generate a script for you</p>
            </div>
          </div>
          <div className="generator-form">
            <textarea
              value={generatePrompt}
              onChange={(e) => setGeneratePrompt(e.target.value)}
              placeholder="e.g., A sci-fi story about a lone astronaut discovering alien life on Mars..."
              rows={3}
              disabled={isGenerating}
            />
            <button
              className="btn btn-primary"
              onClick={handleGenerate}
              disabled={!generatePrompt.trim() || isGenerating}
            >
              {isGenerating ? (
                <>Generating...</>
              ) : (
                <>
                  <Wand2 size={20} />
                  Generate Script
                </>
              )}
            </button>
          </div>
        </div>

        <div className="script-metadata">
          <div className="input-group">
            <label>Script Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter script title"
            />
          </div>
          <div className="input-group">
            <label>Author</label>
            <input
              type="text"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              placeholder="Enter author name"
            />
          </div>
        </div>

        <div className="script-content-wrapper">
          <div className="script-stats">
            <div className="stat">
              <span className="stat-label">Words</span>
              <span className="stat-value">{wordCount.toLocaleString()}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Est. Reading Time</span>
              <span className="stat-value">{estimatedMinutes} min</span>
            </div>
          </div>
          <div className="script-content">
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write your script here or use the AI generator above...

INT. COFFEE SHOP - DAY

The camera pans across a busy coffee shop. We see ALEX (30s), sitting alone at a corner table, typing on a laptop."
              className="script-textarea"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScriptEditor;
