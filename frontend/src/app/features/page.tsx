import Navigation from "@/app/components/Navigation";

export default function Features() {
  const mainFeatures = [
    {
      title: "Script to Video AI",
      description: "Transform any text script into a cinematic short film. Our AI understands narrative structure, character development, and visual storytelling.",
      icon: "📝",
      details: [
        "Natural language script processing",
        "Story arc analysis and optimization",
        "Character consistency across scenes",
        "Automatic scene breakdown"
      ]
    },
    {
      title: "Character Image Generation",
      description: "Generate photo-realistic character images using Stable Diffusion XL with cultural awareness and contextual understanding.",
      icon: "👤",
      details: [
        "Culturally diverse character generation",
        "Context-aware appearance (same character, different settings)",
        "Consistent character features across scenes",
        "High-resolution 4K output"
      ]
    },
    {
      title: "AI Voice Synthesis",
      description: "Professional voice acting with ElevenLabs, OpenAI TTS, and Azure Speech. Choose from 100+ voices in 50+ languages.",
      icon: "🎙️",
      details: [
        "100+ professional voice options",
        "50+ language support",
        "Emotion and tone control",
        "Custom voice cloning (coming soon)"
      ]
    },
    {
      title: "Lip-sync Animation",
      description: "Industry-leading lip-sync technology using WAV2LIP, SadTalker, and FOMM for perfectly synchronized character speech.",
      icon: "💬",
      details: [
        "Frame-perfect lip synchronization",
        "Multiple model options (WAV2LIP, SadTalker, FOMM)",
        "Natural facial expressions",
        "GPU-accelerated processing"
      ]
    },
    {
      title: "Music & Sound Design",
      description: "AI-generated background music and sound effects tailored to your story's mood and pacing.",
      icon: "🎵",
      details: [
        "Mood-based music generation",
        "Custom sound effects library",
        "Automatic audio mixing",
        "Royalty-free licensing"
      ]
    },
    {
      title: "Multilingual Subtitles",
      description: "Automatic subtitle generation in 100+ languages with precise timing and formatting using Whisper ASR.",
      icon: "🌐",
      details: [
        "100+ language support",
        "Whisper large-v3 accuracy",
        "Customizable subtitle styling",
        "SRT, VTT, and embedded formats"
      ]
    }
  ];

  const technicalFeatures = [
    {
      title: "GPU-Accelerated Processing",
      description: "Lightning-fast video generation with NVIDIA A100 and T4 GPUs",
      icon: "⚡"
    },
    {
      title: "Cloud-Native Architecture",
      description: "Built on AWS with auto-scaling for high availability",
      icon: "☁️"
    },
    {
      title: "4K Resolution Output",
      description: "Export videos in up to 4K resolution for professional use",
      icon: "🎬"
    },
    {
      title: "99.9% Uptime SLA",
      description: "Enterprise-grade reliability with multi-region deployment",
      icon: "✅"
    },
    {
      title: "API Access",
      description: "RESTful API for seamless integration with your workflow",
      icon: "🔌"
    },
    {
      title: "Secure & Private",
      description: "SOC 2 compliant with end-to-end encryption",
      icon: "🔒"
    }
  ];

  const workflow = [
    {
      step: "01",
      title: "Write Your Script",
      description: "Start with a simple text script. Our AI handles the rest.",
      color: "from-sky-500 to-blue-600"
    },
    {
      step: "02",
      title: "AI Analysis",
      description: "Our system analyzes characters, scenes, and narrative structure.",
      color: "from-blue-500 to-purple-600"
    },
    {
      step: "03",
      title: "Image Generation",
      description: "Stable Diffusion XL creates photo-realistic character images.",
      color: "from-purple-500 to-pink-600"
    },
    {
      step: "04",
      title: "Video Creation",
      description: "Transform static images into dynamic video sequences.",
      color: "from-pink-500 to-rose-600"
    },
    {
      step: "05",
      title: "Voice & Lip-sync",
      description: "Add professional voice acting with perfect lip synchronization.",
      color: "from-rose-500 to-orange-600"
    },
    {
      step: "06",
      title: "Music & Audio",
      description: "AI-generated music and sound effects enhance your story.",
      color: "from-orange-500 to-amber-600"
    },
    {
      step: "07",
      title: "Final Export",
      description: "Get your completed film with subtitles in multiple languages.",
      color: "from-amber-500 to-yellow-600"
    }
  ];

  return (
    <div className="min-h-screen">
      <Navigation className="fixed top-0 left-0 right-0 z-50" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            Powerful Features for{" "}
            <span className="bg-gradient-to-r from-sky-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Every Creator
            </span>
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            A complete AI-powered filmmaking pipeline that transforms your stories into professional-quality videos.
          </p>
        </div>
      </section>

      {/* 7-Stage Workflow */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">7-Stage AI Pipeline</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Our advanced pipeline processes your script through seven specialized stages to create cinematic films.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {workflow.map((stage, index) => (
              <div key={index} className="relative group">
                <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-slate-600 transition-all h-full">
                  <div className={`inline-block px-4 py-2 rounded-lg bg-gradient-to-r ${stage.color} text-white font-bold text-sm mb-4`}>
                    {stage.step}
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">{stage.title}</h3>
                  <p className="text-sm text-slate-400">{stage.description}</p>
                </div>
                {index < workflow.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2 text-slate-600 text-2xl">
                    →
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Main Features */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Core Features</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Everything you need to create professional-quality AI films from start to finish.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {mainFeatures.map((feature, index) => (
              <div key={index} className="bg-slate-800/50 rounded-xl p-8 border border-slate-700 hover:border-sky-500/50 transition-all">
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                <p className="text-slate-400 mb-6">{feature.description}</p>
                <ul className="space-y-2">
                  {feature.details.map((detail, idx) => (
                    <li key={idx} className="text-sm text-slate-300 flex items-start">
                      <span className="text-sky-400 mr-2">✓</span>
                      {detail}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technical Features */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Technical Excellence</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Enterprise-grade infrastructure built for scale, performance, and reliability.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {technicalFeatures.map((feature, index) => (
              <div key={index} className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 flex items-start gap-4">
                <div className="text-3xl">{feature.icon}</div>
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-sm text-slate-400">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* API Preview */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-white mb-4">Developer-Friendly API</h2>
              <p className="text-slate-300 mb-6">
                Integrate AI Film Studio into your applications with our powerful RESTful API. Generate videos programmatically with just a few lines of code.
              </p>
              <ul className="space-y-3 mb-8">
                <li className="text-slate-300 flex items-start">
                  <span className="text-sky-400 mr-2">✓</span>
                  RESTful API with comprehensive documentation
                </li>
                <li className="text-slate-300 flex items-start">
                  <span className="text-sky-400 mr-2">✓</span>
                  Python, Node.js, and .NET SDKs
                </li>
                <li className="text-slate-300 flex items-start">
                  <span className="text-sky-400 mr-2">✓</span>
                  Webhook support for async processing
                </li>
                <li className="text-slate-300 flex items-start">
                  <span className="text-sky-400 mr-2">✓</span>
                  Rate limiting and usage analytics
                </li>
              </ul>
              <a 
                href="/docs" 
                className="inline-block bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-all"
              >
                View API Documentation
              </a>
            </div>
            <div className="bg-slate-900 rounded-xl p-6 border border-slate-700 font-mono text-sm overflow-x-auto">
              <pre className="text-slate-300">
{`import requests

# Generate a video from script
response = requests.post(
  'https://api.aifilmstudio.com/v1/generate',
  headers={
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  json={
    'script': 'Your story here...',
    'duration': 60,
    'voice': 'professional-male-1',
    'style': 'cinematic'
  }
)

video_url = response.json()['video_url']
print(f'Video ready: {video_url}')`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Create Your First Film?</h2>
          <p className="text-slate-300 mb-8">
            Join thousands of creators using AI Film Studio to bring their stories to life.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="/signup" 
              className="bg-gradient-to-r from-sky-500 to-purple-600 hover:from-sky-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all shadow-lg"
            >
              Start Free Trial
            </a>
            <a 
              href="/pricing" 
              className="bg-slate-700 hover:bg-slate-600 text-white px-8 py-4 rounded-xl font-semibold transition-colors"
            >
              View Pricing
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
