import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <div className="text-2xl font-bold text-primary-600">
            🎬 AI Film Studio
          </div>
          <div className="space-x-4">
            <Link
              href="/login"
              className="text-gray-700 hover:text-primary-600 font-medium"
            >
              Login
            </Link>
            <Link
              href="/signup"
              className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 font-medium"
            >
              Sign Up
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Transform Your Scripts into
            <span className="text-primary-600"> Cinematic Films</span>
          </h1>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
            AI-powered platform that turns your text scripts into professional short films
            with intelligent scene generation and video composition.
          </p>
          <div className="flex justify-center gap-4">
            <Link
              href="/signup"
              className="bg-primary-600 text-white px-8 py-4 rounded-lg hover:bg-primary-700 font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
            >
              Get Started Free
            </Link>
            <Link
              href="/login"
              className="bg-white text-primary-600 px-8 py-4 rounded-lg hover:bg-gray-50 font-semibold text-lg shadow-lg hover:shadow-xl transition-all border-2 border-primary-600"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-24 grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🎨</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              AI-Powered Generation
            </h3>
            <p className="text-gray-600">
              Advanced AI models create stunning visuals from your script descriptions
            </p>
          </div>
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Fast Processing
            </h3>
            <p className="text-gray-600">
              GPU-accelerated rendering delivers your films in minutes, not hours
            </p>
          </div>
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🎬</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Professional Quality
            </h3>
            <p className="text-gray-600">
              Cinematic composition and intelligent scene transitions
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-24 max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>
          <div className="space-y-6">
            <div className="flex items-start gap-4 bg-white p-6 rounded-lg shadow">
              <div className="flex-shrink-0 w-10 h-10 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h4 className="font-bold text-lg text-gray-900 mb-2">Write Your Script</h4>
                <p className="text-gray-600">
                  Create your story with scene descriptions and dialogue
                </p>
              </div>
            </div>
            <div className="flex items-start gap-4 bg-white p-6 rounded-lg shadow">
              <div className="flex-shrink-0 w-10 h-10 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h4 className="font-bold text-lg text-gray-900 mb-2">AI Generates Scenes</h4>
                <p className="text-gray-600">
                  Our AI creates visuals for each scene automatically
                </p>
              </div>
            </div>
            <div className="flex items-start gap-4 bg-white p-6 rounded-lg shadow">
              <div className="flex-shrink-0 w-10 h-10 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h4 className="font-bold text-lg text-gray-900 mb-2">Download Your Film</h4>
                <p className="text-gray-600">
                  Get your professional-quality video ready to share
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 mt-24 border-t border-gray-200">
        <div className="text-center text-gray-600">
          <p>&copy; 2024 AI Film Studio. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
