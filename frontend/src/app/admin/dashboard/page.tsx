'use client';

import Link from 'next/link';
import Navigation from '../../components/Navigation';

/* FR-040: Admin Dashboard. System health, user stats, jobs, queue depth. UI: /admin/dashboard */

export default function AdminDashboardPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <Navigation />
      <main className="pt-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>
          <Link href="/admin/moderation" className="text-sky-400 hover:text-sky-300 text-sm font-medium">
            Content Moderation →
          </Link>
        </div>
        <p className="text-slate-400 mb-8">
          FR-040: Admins view system health, total users, active users, jobs processed, CPU/GPU/storage usage,
          failed job count, real-time queue depth.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { label: 'Total Users', value: '—', desc: 'From User service' },
            { label: 'Active Users', value: '—', desc: 'Last 24h' },
            { label: 'Jobs Processed', value: '—', desc: 'All time' },
            { label: 'Queue Depth', value: '—', desc: 'Real-time SQS' },
          ].map((s) => (
            <div key={s.label} className="bg-slate-800/50 rounded-xl border border-slate-700 p-6">
              <p className="text-slate-400 text-sm">{s.label}</p>
              <p className="text-2xl font-bold text-white mt-1">{s.value}</p>
              <p className="text-slate-500 text-xs mt-1">{s.desc}</p>
            </div>
          ))}
        </div>
        <div className="mt-8">
          <Link href="/dashboard" className="text-sky-400 hover:text-sky-300">
            ← Back to Dashboard
          </Link>
        </div>
      </main>
    </div>
  );
}
