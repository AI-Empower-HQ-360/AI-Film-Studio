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
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <SignOutButton />
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">User Information</h2>
          <dl className="space-y-2">
            <div>
              <dt className="font-medium text-gray-700">Email:</dt>
              <dd className="text-gray-600">{user.email}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">User ID:</dt>
              <dd className="text-gray-600 text-sm font-mono">{user.id}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">Email Confirmed:</dt>
              <dd className="text-gray-600">
                {user.email_confirmed_at ? (
                  <span className="text-green-600">✓ Yes</span>
                ) : (
                  <span className="text-yellow-600">⚠ Pending</span>
                )}
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  )
}
