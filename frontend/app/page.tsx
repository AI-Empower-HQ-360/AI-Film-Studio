import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🎬 AI Film Studio
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Transform your scripts into cinematic videos with AI
          </p>
          
          <div className="flex gap-4 justify-center">
            <Link
              href="/signup"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="bg-white text-blue-600 px-8 py-3 rounded-lg font-medium border-2 border-blue-600 hover:bg-blue-50 transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>

        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">📝 Write Scripts</h3>
            <p className="text-gray-600">Create compelling stories with AI-assisted writing</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">🎨 Generate Scenes</h3>
            <p className="text-gray-600">AI creates stunning visuals for each scene</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">🎥 Export Video</h3>
            <p className="text-gray-600">Download your film in high quality MP4</p>
          </div>
        </div>
      </div>
    </main>
  )
}
