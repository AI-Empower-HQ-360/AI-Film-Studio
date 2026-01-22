'use client';

import Link from 'next/link';
import { useState } from 'react';
import Navigation from '../components/Navigation';

/* FR-003: Password Reset. Send reset link to email, expires 1h. POST /api/v1/auth/forgot-password */

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      // TODO: POST /api/v1/auth/forgot-password { email }
      await new Promise((r) => setTimeout(r, 500));
      setSubmitted(true);
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <Navigation />

      <div className="flex items-center justify-center px-4 sm:px-6 lg:px-8 py-20">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-2">Forgot password?</h2>
            <p className="text-slate-400">
              Enter your email and we&apos;ll send you a link to reset your password. Link expires in 1 hour.
            </p>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-8">
            {submitted ? (
              <div className="text-center space-y-4">
                <p className="text-slate-300">
                  If an account exists for <strong className="text-white">{email}</strong>, you&apos;ll receive a
                  password reset link shortly.
                </p>
                <Link href="/signin" className="inline-block text-sky-400 hover:text-sky-300 font-medium">
                  Back to Sign in
                </Link>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="forgot-email" className="block text-sm font-medium text-slate-300 mb-1">
                    Email
                  </label>
                  <input
                    id="forgot-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-600 text-white placeholder-slate-500 focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                    required
                  />
                </div>
                {error && (
                  <p className="text-sm text-red-400" role="alert">
                    {error}
                  </p>
                )}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-sky-500 hover:bg-sky-600 disabled:opacity-50 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  {loading ? 'Sending…' : 'Send reset link'}
                </button>
              </form>
            )}

            <div className="mt-6 text-center">
              <Link href="/signin" className="text-sm text-sky-400 hover:text-sky-300">
                Back to Sign in
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
