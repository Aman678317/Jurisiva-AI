import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import './App.css';

export default function App() {
  const [currentView, setCurrentView] = useState<'landing' | 'app'>('landing');

  return (
    <div className="app-root">
      {currentView === 'landing' ? (
        <LandingPage onLaunchApp={() => setCurrentView('app')} />
      ) : (
        <Dashboard onBackToLanding={() => setCurrentView('landing')} />
      )}
    </div>
  );
}
