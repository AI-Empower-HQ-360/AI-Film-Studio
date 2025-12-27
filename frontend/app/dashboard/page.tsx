import { createServerSupabaseClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import SignOutButton from '@/components/auth/SignOutButton'

export default async function DashboardPage() {
  const supabase = await createServerSupabaseClient()

  const {
    data: { user },
  } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="bg-white shadow-sm rounded-lg mb-8">
          <div className="px-6 py-4 flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">🎬</span>
              <h1 className="text-2xl font-bold text-gray-900">AI Film Studio</h1>
            </div>
            <SignOutButton />
          </div>
        </header>

        {/* Main Content */}
        <div className="bg-white shadow-lg rounded-lg p-8">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome to Your Dashboard
            </h2>
            <p className="text-gray-600">
              Start creating your AI-powered films
            </p>
          </div>

          {/* User Info Card */}
          <div className="bg-gradient-to-r from-primary-50 to-indigo-50 rounded-lg p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Account Information
            </h3>
            <div className="space-y-2">
              <div className="flex items-center">
                <span className="text-gray-600 font-medium w-32">Email:</span>
                <span className="text-gray-900">{user.email}</span>
              </div>
              <div className="flex items-center">
                <span className="text-gray-600 font-medium w-32">User ID:</span>
                <span className="text-gray-900 font-mono text-sm">{user.id}</span>
              </div>
              <div className="flex items-center">
                <span className="text-gray-600 font-medium w-32">Status:</span>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-3 gap-6">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors cursor-pointer">
              <div className="text-4xl mb-4">📝</div>
              <h4 className="font-semibold text-gray-900 mb-2">New Project</h4>
              <p className="text-sm text-gray-600">Start a new film project</p>
            </div>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors cursor-pointer">
              <div className="text-4xl mb-4">📁</div>
              <h4 className="font-semibold text-gray-900 mb-2">My Projects</h4>
              <p className="text-sm text-gray-600">View your projects</p>
            </div>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors cursor-pointer">
              <div className="text-4xl mb-4">⚙️</div>
              <h4 className="font-semibold text-gray-900 mb-2">Settings</h4>
              <p className="text-sm text-gray-600">Manage your account</p>
            </div>
          </div>

          {/* Info Banner */}
          <div className="mt-8 bg-blue-50 border-l-4 border-primary-600 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-primary-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-primary-700">
                  This is your dashboard. Full project functionality will be available soon.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
