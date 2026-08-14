import React, { useState } from 'react';

export default function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/matters');
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ error: 'Backend server offline. Run: python -m uvicorn app.main:app --reload' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
      <header style={{ borderBottom: '2px solid #2563eb', paddingBottom: '1rem', marginBottom: '2rem' }}>
        <h1 style={{ color: '#1e293b', margin: 0 }}>🏛️ Jurisiva AI</h1>
        <p style={{ color: '#64748b', marginTop: '0.5rem' }}>
          India-First Legal & Property Intelligence Platform
        </p>
      </header>

      <main>
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
          <input
            type="text"
            placeholder="Search Survey No. 42/1 Devanahalli or Ask Legal Copilot..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ flex: 1, padding: '0.75rem', borderRadius: '0.375rem', border: '1px solid #cbd5e1' }}
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            style={{
              backgroundColor: '#2563eb',
              color: '#ffffff',
              padding: '0.75rem 1.5rem',
              border: 'none',
              borderRadius: '0.375rem',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {response && (
          <div style={{ background: '#f8fafc', padding: '1rem', borderRadius: '0.375rem', border: '1px solid #e2e8f0' }}>
            <h3 style={{ marginTop: 0 }}>API Result:</h3>
            <pre style={{ overflowX: 'auto' }}>{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
}
