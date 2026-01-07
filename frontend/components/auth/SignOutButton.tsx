'use client'

import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

export default function SignOutButton() {
  const router = useRouter()
  const supabase = createClient()

  const handleSignOut = async () => {
    await supabase.auth.signOut()
    router.push('/login')
    router.refresh()
  }

  return (
    <button
      onClick={handleSignOut}
      className="bg-red-600 text-white rounded-lg py-2 px-4 font-medium hover:bg-red-700 transition-colors"
    >
      Sign Out
    </button>
  )
}
