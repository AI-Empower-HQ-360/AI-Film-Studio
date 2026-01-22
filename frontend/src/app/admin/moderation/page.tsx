'use client';

import Link from 'next/link';
import Navigation from '../../components/Navigation';

/* FR-042: Content Moderation. Admin review queue, approve/reject projects. UI: /admin/moderation */

export default function AdminModerationPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <Navigation />
      <main className="pt-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-white">Content Moderation</h1>
          <Link href="/admin/dashboard" className="text-sky-400 hover:text-sky-300 text-sm font-medium">
            ← Admin Dashboard
          </Link>
        </div>
        <p className="text-slate-400 mb-8">
          FR-042: Admins review flagged scripts (auto-flagging of inappropriate keywords), approve or reject
          projects, notify users of violations.
        </p>
        <div className="bg-slate-800/50 rounded-xl border border-slate-700 p-8 text-center">
          <p className="text-slate-400">Review queue placeholder. Connect to moderation API when ready.</p>
          <Link href="/dashboard" className="mt-4 inline-block text-sky-400 hover:text-sky-300">
            ← Back to Dashboard
          </Link>
        </div>
      </main>
    </div>
  );
}
