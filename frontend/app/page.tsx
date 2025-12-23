import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            AI Film Studio
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Transform your scripts into stunning AI-generated films
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/demo"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
            >
              Try Demo
            </Link>
            <Link
              href="/docs"
              className="bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-gray-50 transition-colors font-semibold border-2 border-blue-600"
            >
              View Docs
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🎬</div>
            <h3 className="text-xl font-semibold mb-2">Script to Film</h3>
            <p className="text-gray-600">
              Enter your script and watch it transform into a complete video with scenes, transitions, and effects.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">🎙️</div>
            <h3 className="text-xl font-semibold mb-2">Voice & Music</h3>
            <p className="text-gray-600">
              Automatic voice narration synthesis and background music generation for your films.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-4">📦</div>
            <h3 className="text-xl font-semibold mb-2">Ready to Download</h3>
            <p className="text-gray-600">
              High-quality MP4 files with secure signed URLs, ready to share or publish.
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-3xl font-bold mb-6 text-center">How It Works</h2>
          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                1
              </div>
              <div>
                <h4 className="font-semibold text-lg mb-1">Write Your Script</h4>
                <p className="text-gray-600">Create your story, scene by scene</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                2
              </div>
              <div>
                <h4 className="font-semibold text-lg mb-1">AI Processing</h4>
                <p className="text-gray-600">
                  Content moderation, image generation, video composition, voice synthesis, and music creation
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                3
              </div>
              <div>
                <h4 className="font-semibold text-lg mb-1">Download & Share</h4>
                <p className="text-gray-600">Get your completed film in HD quality</p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-16 text-center">
          <h2 className="text-3xl font-bold mb-4">Features</h2>
          <div className="grid md:grid-cols-2 gap-4 max-w-3xl mx-auto">
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="font-semibold">✓ JWT Authentication</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="font-semibold">✓ Cost Governance</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="font-semibold">✓ Content Moderation</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="font-semibold">✓ Job State Machine</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="font-semibold">✓ Real-time Progress Tracking</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="font-semibold">✓ Signed URL Downloads</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

