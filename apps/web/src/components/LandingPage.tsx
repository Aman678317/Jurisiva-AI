import React, { useState, useEffect } from 'react';

interface LandingPageProps {
  onLaunchApp: () => void;
}

export default function LandingPage({ onLaunchApp }: LandingPageProps) {
  const [query, setQuery] = useState('What is the extent of Survey No 42/1 Devanahalli?');
  const [apiStatus, setApiStatus] = useState<string>('Checking...');
  const [searchResult, setSearchResult] = useState<any>(null);

  // Ping FastAPI Backend
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/health')
      .then(res => res.json())
      .then(() => {
        setApiStatus('● Backend Connected (200 OK)');
      })
      .catch(() => {
        setApiStatus('● Backend Offline (Start uvicorn server)');
      });
  }, []);

  const handleQuickSearch = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/health');
      const data = await res.json();
      setSearchResult(data);
    } catch (err) {
      setSearchResult({ error: 'Backend server offline. Run: python -m uvicorn services.api.app.main:app --reload' });
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-main)', color: '#ffffff' }}>
      {/* Landing Navbar */}
      <nav className="landing-navbar">
        <div className="brand-logo">
          <span>🏛️</span> Jurisiva AI
        </div>
        <ul className="nav-links">
          <li className="nav-link-item">Search Property</li>
          <li className="nav-link-item">Verify Deeds</li>
          <li className="nav-link-item">Case Law</li>
          <li className="nav-link-item">AI Assistant</li>
        </ul>
        <button className="btn-primary" onClick={onLaunchApp}>
          Launch Platform OS →
        </button>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div style={{ fontSize: '0.85rem', color: '#34d399', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '0.75rem' }}>
          {apiStatus}
        </div>
        <h1 className="hero-heading">
          INDIA-FIRST LEGAL & PROPERTY INTELLIGENCE OS
        </h1>
        <p className="hero-subtext">
          Harvey-inspired • Multilingual Indic OCR • Title Chain Reconstruction • Citation-Grounded RAG Assistant
        </p>

        {/* Hero Feature Card */}
        <div className="hero-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <span style={{ fontSize: '2rem' }}>📜</span>
              <div>
                <h3 style={{ margin: 0, color: '#ffffff' }}>Indic Legal Deed Scanner & Title Chain AI</h3>
                <p style={{ margin: '0.25rem 0 0 0', color: '#38bdf8', fontSize: '0.85rem' }}>Target: Survey No. 42/1 Hissa 2 Devanahalli</p>
              </div>
            </div>
            <span style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#34d399', border: '1px solid #10b981', padding: '0.35rem 0.85rem', borderRadius: '9999px', fontSize: '0.85rem', fontWeight: 600 }}>
              ● Core Engines Active
            </span>
          </div>

          <div className="grid-features">
            <div className="feature-box">
              <h4>📄 Indic Document OCR</h4>
              <p>Kannada, Marathi, Hindi & English layout block extraction & Survey No normalization.</p>
            </div>
            <div className="feature-box">
              <h4>🏡 Title Chain Graph</h4>
              <p>Chronological flow reconstruction (1985 Sale → 2010 Mortgage → 2018 Sale Deed).</p>
            </div>
            <div className="feature-box">
              <h4>🤖 Citation RAG AI</h4>
              <p>Evidence Sufficiency Gate enforcing zero hallucination with verified source chips.</p>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '2rem' }}>
            <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
              Enterprise Data Isolation & SOC 2 Ready
            </div>
            <button className="btn-primary" onClick={onLaunchApp}>
              Enter Workspace OS →
            </button>
          </div>
        </div>

        {/* Quick Interactive Search Bar */}
        <div style={{ width: '100%', maxWidth: '750px', background: '#131b2e', border: '1px solid #1e293b', borderRadius: '12px', padding: '1.5rem', textAlign: 'left', marginBottom: '3rem' }}>
          <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.1rem', color: '#ffffff' }}>⚡ Interactive Legal Query Test</h3>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{ flex: 1, background: '#0f172a', border: '1px solid #334155', color: '#ffffff', padding: '0.75rem', borderRadius: '6px' }}
            />
            <button className="btn-primary" onClick={handleQuickSearch}>Run Query</button>
          </div>

          {searchResult && (
            <div style={{ marginTop: '1rem', background: '#0b1120', padding: '1rem', borderRadius: '6px', border: '1px solid #1e293b' }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#38bdf8' }}>Backend API Response:</h4>
              <pre style={{ margin: 0, fontSize: '0.85rem' }}>{JSON.stringify(searchResult, null, 2)}</pre>
            </div>
          )}
        </div>

        {/* Features Grid */}
        <section className="features-section">
          <h2 className="section-title">ENGINEERED FOR INDIAN LEGAL & PROPERTY TEAMS</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🛡️</div>
              <h3>Zero-Hallucination RAG</h3>
              <p>Automated Evidence Sufficiency Gate checks every proposition against uploaded source chunks, issuing explicit refusals when evidence is missing.</p>
            </div>
            <div className="feature-card">
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📄</div>
              <h3>Multilingual Indic Processing</h3>
              <p>Supports scanned & native PDFs across English, Kannada, Marathi, Hindi, Tamil, and Telugu with automatic Survey Number normalization.</p>
            </div>
            <div className="feature-card">
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🏡</div>
              <h3>Title Conflict Detector</h3>
              <p>Reconstructs chronological deed chains and flags area extent mismatches, unreleased mortgages, and unrecorded title breaks.</p>
            </div>
          </div>
        </section>
      </section>
    </div>
  );
}
