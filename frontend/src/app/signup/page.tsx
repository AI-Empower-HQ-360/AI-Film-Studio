'use client';
import Link from 'next/link';
import Navigation from '../components/Navigation';

export default function SignUpPage() {
  const handleGetStarted = () => {
    // No authentication needed - direct access
    window.location.href = '/dashboard';
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <Navigation />

      <div className="flex items-center justify-center px-4 sm:px-6 lg:px-8 py-20">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-2">Create your account</h2>
            <p className="text-slate-400">Start creating amazing AI films today</p>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-8">
            <button
              onClick={handleGetStarted}
              className="w-full bg-sky-500 hover:bg-sky-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Get Started
            </button>

            <div className="mt-6 text-center">
              <p className="text-slate-400 text-sm">
                Already have an account?{' '}
                <Link href="/signin" className="text-sky-400 hover:text-sky-300 font-medium">
                  Sign in
                </Link>
              </p>
            </div>

            <div className="mt-6 pt-6 border-t border-slate-600">
              <p className="text-slate-500 text-xs text-center">
                By signing up, you agree to our{' '}
                <Link href="/terms" className="text-sky-400 hover:text-sky-300">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link href="/privacy" className="text-sky-400 hover:text-sky-300">
                  Privacy Policy
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}