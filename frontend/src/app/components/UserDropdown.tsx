'use client';
import Link from 'next/link';
import { useState, useRef, useEffect } from 'react';

interface UserDropdownProps {
  user: {
    firstName: string;
    lastName: string;
    email: string;
    avatar?: string;
  };
}

export default function UserDropdown({ user }: UserDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSignOut = async () => {
    try {
      // Clear any stored auth data
      localStorage.removeItem('auth_token');
      // Redirect to signin
      window.location.href = '/signin';
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const initials = `${user.firstName.charAt(0)}${user.lastName.charAt(0)}`;

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-8 h-8 rounded-full bg-gradient-to-r from-sky-500 to-purple-600 flex items-center justify-center text-white font-semibold cursor-pointer hover:scale-105 transition-transform focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-slate-900"
      >
        {user.avatar ? (
          <img 
            src={user.avatar} 
            alt={`${user.firstName} ${user.lastName}`}
            className="w-8 h-8 rounded-full"
          />
        ) : (
          initials
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-slate-800 border border-slate-700 rounded-xl shadow-lg z-50">
          {/* User Info */}
          <div className="px-4 py-3 border-b border-slate-700">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-sky-500 to-purple-600 flex items-center justify-center text-white font-semibold">
                {user.avatar ? (
                  <img 
                    src={user.avatar} 
                    alt={`${user.firstName} ${user.lastName}`}
                    className="w-10 h-10 rounded-full"
                  />
                ) : (
                  initials
                )}
              </div>
              <div>
                <p className="text-white font-medium">{user.firstName} {user.lastName}</p>
                <p className="text-slate-400 text-sm">{user.email}</p>
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <div className="py-2">
            <Link
              href="/dashboard"
              className="flex items-center px-4 py-3 text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors"
              onClick={() => setIsOpen(false)}
            >
              <span className="mr-3">📊</span>
              Dashboard
            </Link>
            
            <Link
              href="/dashboard?tab=account"
              className="flex items-center px-4 py-3 text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors"
              onClick={() => setIsOpen(false)}
            >
              <span className="mr-3">⚙️</span>
              Account Settings
            </Link>
            
            <Link
              href="/pricing"
              className="flex items-center px-4 py-3 text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors"
              onClick={() => setIsOpen(false)}
            >
              <span className="mr-3">⭐</span>
              Upgrade Plan
            </Link>
            
            <hr className="my-2 border-slate-700" />
            
            <button
              onClick={handleSignOut}
              className="w-full flex items-center px-4 py-3 text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors text-left"
            >
              <span className="mr-3">🚪</span>
              Sign Out
            </button>
          </div>
        </div>
      )}
    </div>
  );
}