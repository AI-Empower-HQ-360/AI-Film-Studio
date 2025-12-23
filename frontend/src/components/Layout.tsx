import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Film, FileText, Clapperboard, Video, Download, Home } from 'lucide-react';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/script', icon: FileText, label: 'Script' },
    { path: '/scenes', icon: Clapperboard, label: 'Scenes' },
    { path: '/shots', icon: Video, label: 'Shots' },
    { path: '/export', icon: Download, label: 'Export' },
  ];

  return (
    <div className="layout">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <Film size={32} />
            <h1>AI Film Studio</h1>
          </div>
          <nav className="nav">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-item ${isActive ? 'active' : ''}`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </header>
      <main className="main-content">{children}</main>
    </div>
  );
};

export default Layout;
