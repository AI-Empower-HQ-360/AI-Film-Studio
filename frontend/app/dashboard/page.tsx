import { redirect } from 'next/navigation'
import { createServerSupabaseClient } from '@/lib/supabase/server'
import SignOutButton from '@/components/auth/SignOutButton'

export default async function DashboardPage() {
  const supabase = await createServerSupabaseClient()
  
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/login')
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="bg-white shadow-lg rounded-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
          
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Welcome back!</h2>
            <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
              <p className="text-gray-700 mb-2">
                <strong>Email:</strong> {user.email}
              </p>
              <p className="text-gray-700 mb-2">
                <strong>User ID:</strong> {user.id}
              </p>
              <p className="text-gray-700 mb-2">
                <strong>Email Confirmed:</strong>{' '}
                <span className={user.email_confirmed_at ? 'text-green-600' : 'text-yellow-600'}>
                  {user.email_confirmed_at ? 'Yes' : 'No - Please check your email'}
                </span>
              </p>
              <p className="text-gray-700">
                <strong>Account Created:</strong> {new Date(user.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Getting Started</h2>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-700 mb-4">
                Welcome to AI Film Studio! Here&apos;s what you can do:
              </p>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                <li>Create AI-powered films from text scripts</li>
                <li>Generate stunning visuals with SDXL models</li>
                <li>Compose and render professional-quality videos</li>
                <li>Manage your projects and credits</li>
              </ul>
              <p className="text-gray-600 mt-4 text-sm">
                Note: Film creation features are coming soon. Stay tuned!
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <SignOutButton />
          </div>
        </div>
      </div>
    </main>
  )
}
