'use client';
import Link from 'next/link';

interface NavigationProps {
  currentPage?: string;
  className?: string;
}

export default function Navigation({ currentPage, className = '' }: NavigationProps) {

  const baseNavClass = "bg-slate-900/80 backdrop-blur-md border-b border-slate-700";
  const fullClassName = className ? `${baseNavClass} ${className}` : baseNavClass;

  return (
    <nav className={fullClassName}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-purple-500 bg-clip-text text-transparent hover:scale-105 transition-transform">
              🎬 AI Film Studio
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              href="/#features" 
              className={`transition-colors ${
                currentPage === 'features' 
                  ? 'text-white font-medium border-b-2 border-sky-500' 
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              Features
            </Link>
            
            <Link 
              href="/#how-it-works" 
              className={`transition-colors ${
                currentPage === 'how-it-works' 
                  ? 'text-white font-medium border-b-2 border-sky-500' 
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              How It Works
            </Link>
            
            <Link 
              href="/pricing" 
              className={`transition-colors ${
                currentPage === 'pricing' 
                  ? 'text-white font-medium border-b-2 border-sky-500' 
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              Pricing
            </Link>

            {/* Navigation Links */}
            <Link 
              href="/dashboard" 
              className={`transition-colors ${
                currentPage === 'dashboard' 
                  ? 'text-white font-medium border-b-2 border-sky-500' 
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              Dashboard
            </Link>
            <Link href="/signin" className="text-slate-300 hover:text-white transition-colors">
              Sign In
            </Link>
            <Link href="/signup" className="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
              Sign Up
            </Link>
          </div>

          {/* Mobile Navigation */}
          <div className="md:hidden">
            <Link href="/signin" className="text-slate-300 hover:text-white text-sm transition-colors">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}