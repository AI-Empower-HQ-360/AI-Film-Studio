import Navigation from "@/app/components/Navigation";

export default function Docs() {
  const endpoints = [
    {
      method: "POST",
      path: "/v1/generate",
      description: "Generate a video from a text script",
      params: ["script", "duration", "voice", "style"]
    },
    {
      method: "GET",
      path: "/v1/videos/:id",
      description: "Get video generation status and download URL",
      params: ["id"]
    },
    {
      method: "POST",
      path: "/v1/characters",
      description: "Generate character images",
      params: ["description", "count", "style"]
    },
    {
      method: "GET",
      path: "/v1/voices",
      description: "List available voice options",
      params: []
    }
  ];

  const sdks = [
    {
      name: "Python",
      icon: "🐍",
      code: `pip install aifilmstudio

from aifilmstudio import AIFilmStudio

client = AIFilmStudio(api_key="YOUR_API_KEY")
video = client.generate(
    script="Your story here...",
    duration=60,
    voice="professional-male-1"
)`
    },
    {
      name: "Node.js",
      icon: "📦",
      code: `npm install aifilmstudio

const AIFilmStudio = require('aifilmstudio');

const client = new AIFilmStudio({
  apiKey: 'YOUR_API_KEY'
});

const video = await client.generate({
  script: 'Your story here...',
  duration: 60,
  voice: 'professional-male-1'
});`
    },
    {
      name: ".NET",
      icon: "🔷",
      code: `dotnet add package AIFilmStudio

using AIFilmStudio;

var client = new AIFilmStudioClient("YOUR_API_KEY");
var video = await client.GenerateAsync(new VideoRequest
{
    Script = "Your story here...",
    Duration = 60,
    Voice = "professional-male-1"
});`
    }
  ];

  return (
    <div className="min-h-screen">
      <Navigation className="fixed top-0 left-0 right-0 z-50" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            API{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Documentation
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Integrate AI Film Studio into your applications with our powerful RESTful API.
          </p>
        </div>
      </section>

      {/* Quick Start */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-8">Quick Start</h2>
          
          <div className="bg-slate-900 rounded-xl p-6 border border-slate-700 mb-8">
            <h3 className="text-xl font-semibold text-white mb-4">1. Get Your API Key</h3>
            <p className="text-slate-300 mb-4">
              Sign up for an account and navigate to Settings → API Keys to generate your API key.
            </p>
            <div className="bg-slate-800 rounded-lg p-4 font-mono text-sm text-sky-400">
              sk_live_1234567890abcdefghijklmnopqrstuv
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-700 mb-8">
            <h3 className="text-xl font-semibold text-white mb-4">2. Make Your First Request</h3>
            <p className="text-slate-300 mb-4">
              Send a POST request to generate your first video:
            </p>
            <div className="bg-slate-800 rounded-lg p-4 font-mono text-sm text-slate-300 overflow-x-auto">
              <pre>{`curl -X POST https://api.aifilmstudio.com/v1/generate \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "script": "A young explorer discovers a hidden world beneath the ocean.",
    "duration": 60,
    "voice": "professional-female-2",
    "style": "cinematic"
  }'`}</pre>
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-700">
            <h3 className="text-xl font-semibold text-white mb-4">3. Poll for Results</h3>
            <p className="text-slate-300 mb-4">
              Video generation is asynchronous. Poll the status endpoint with the job ID:
            </p>
            <div className="bg-slate-800 rounded-lg p-4 font-mono text-sm text-slate-300 overflow-x-auto">
              <pre>{`curl https://api.aifilmstudio.com/v1/videos/job_abc123 \\
  -H "Authorization: Bearer YOUR_API_KEY"

# Response
{
  "id": "job_abc123",
  "status": "completed",
  "video_url": "https://cdn.aifilmstudio.com/videos/...",
  "duration": 60,
  "created_at": "2026-01-15T10:30:00Z"
}`}</pre>
            </div>
          </div>
        </div>
      </section>

      {/* API Endpoints */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-8">API Endpoints</h2>
          
          <div className="space-y-4">
            {endpoints.map((endpoint, index) => (
              <div key={index} className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
                <div className="flex items-center gap-3 mb-3">
                  <span className={`px-3 py-1 rounded-lg font-mono text-sm font-bold ${
                    endpoint.method === 'POST' 
                      ? 'bg-green-500/20 text-green-400' 
                      : 'bg-sky-500/20 text-sky-400'
                  }`}>
                    {endpoint.method}
                  </span>
                  <span className="font-mono text-white">{endpoint.path}</span>
                </div>
                <p className="text-slate-400 mb-3">{endpoint.description}</p>
                {endpoint.params.length > 0 && (
                  <div className="flex gap-2 flex-wrap">
                    {endpoint.params.map((param, idx) => (
                      <span key={idx} className="px-2 py-1 bg-slate-700 rounded text-xs font-mono text-slate-300">
                        {param}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SDKs */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-4">Official SDKs</h2>
          <p className="text-slate-400 mb-12">
            Use our official SDKs for easier integration with your favorite programming language.
          </p>

          <div className="grid lg:grid-cols-3 gap-6">
            {sdks.map((sdk, index) => (
              <div key={index} className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden">
                <div className="p-6 border-b border-slate-700">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{sdk.icon}</span>
                    <h3 className="text-xl font-semibold text-white">{sdk.name}</h3>
                  </div>
                </div>
                <div className="p-6">
                  <pre className="text-xs text-slate-300 font-mono overflow-x-auto">
                    {sdk.code}
                  </pre>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Rate Limits */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-8">Rate Limits & Quotas</h2>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-2">Free Tier</h3>
              <p className="text-3xl font-bold text-sky-400 mb-2">10</p>
              <p className="text-slate-400">requests per hour</p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-2">Pro Tier</h3>
              <p className="text-3xl font-bold text-purple-400 mb-2">100</p>
              <p className="text-slate-400">requests per hour</p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-2">Enterprise</h3>
              <p className="text-3xl font-bold text-pink-400 mb-2">Custom</p>
              <p className="text-slate-400">unlimited requests</p>
            </div>
          </div>
        </div>
      </section>

      {/* Webhooks */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-4">Webhooks</h2>
          <p className="text-slate-400 mb-8">
            Configure webhooks to receive real-time notifications when videos are completed.
          </p>

          <div className="bg-slate-900 rounded-xl p-6 border border-slate-700">
            <h3 className="text-xl font-semibold text-white mb-4">Configure Webhook</h3>
            <div className="bg-slate-800 rounded-lg p-4 font-mono text-sm text-slate-300 overflow-x-auto mb-4">
              <pre>{`curl -X POST https://api.aifilmstudio.com/v1/webhooks \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "url": "https://yourapp.com/webhooks/video-completed",
    "events": ["video.completed", "video.failed"]
  }'`}</pre>
            </div>

            <h3 className="text-xl font-semibold text-white mb-4 mt-8">Webhook Payload</h3>
            <div className="bg-slate-800 rounded-lg p-4 font-mono text-sm text-slate-300 overflow-x-auto">
              <pre>{`{
  "event": "video.completed",
  "data": {
    "id": "job_abc123",
    "video_url": "https://cdn.aifilmstudio.com/videos/...",
    "duration": 60,
    "created_at": "2026-01-15T10:30:00Z",
    "completed_at": "2026-01-15T10:32:45Z"
  }
}`}</pre>
            </div>
          </div>
        </div>
      </section>

      {/* Support */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Need Help?</h2>
          <p className="text-slate-300 mb-8">
            Our support team is here to help you integrate AI Film Studio into your application.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="/contact" 
              className="bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all shadow-lg"
            >
              Contact Support
            </a>
            <a 
              href="https://github.com/AI-Empower-HQ-360/AI-Film-Studio" 
              target="_blank"
              rel="noopener noreferrer"
              className="bg-slate-700 hover:bg-slate-600 text-white px-8 py-4 rounded-xl font-semibold transition-colors flex items-center justify-center gap-2"
            >
              <span>View on GitHub</span>
              <span>→</span>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
