import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          🎬 AI Film Studio
        </h1>
        <p className="text-xl text-gray-700 mb-8">
          Transform text scripts into cinematic short films using AI-powered image/video generation
        </p>
        <p className="text-lg text-gray-600 mb-12 max-w-2xl mx-auto">
          Create professional-quality films (30-90 seconds) with our cloud-native platform 
          that leverages cutting-edge AI models for scene generation, composition, and rendering.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link 
            href="/signup"
            className="bg-primary-600 hover:bg-primary-700 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors duration-200 w-full sm:w-auto"
          >
            Get Started
          </Link>
          <Link 
            href="/login"
            className="bg-white hover:bg-gray-50 text-primary-600 font-bold py-3 px-8 rounded-lg text-lg border-2 border-primary-600 transition-colors duration-200 w-full sm:w-auto"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-3">🎨</div>
            <h3 className="text-lg font-semibold mb-2 text-gray-800">AI-Powered Generation</h3>
            <p className="text-gray-600">
              Advanced SDXL models create stunning visuals from your script descriptions
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="text-lg font-semibold mb-2 text-gray-800">Fast & Scalable</h3>
            <p className="text-gray-600">
              Cloud-native architecture with GPU acceleration for rapid film production
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-3">🎯</div>
            <h3 className="text-lg font-semibold mb-2 text-gray-800">Production-Ready</h3>
            <p className="text-gray-600">
              Enterprise-grade infrastructure with monitoring, auto-scaling, and high availability
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
