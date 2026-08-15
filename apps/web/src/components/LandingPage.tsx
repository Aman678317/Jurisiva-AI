import React, { useState, useEffect } from 'react';
import Hero3DScene from './Hero3DScene';

interface LandingPageProps {
  onLaunchApp: () => void;
}

export default function LandingPage({ onLaunchApp }: LandingPageProps) {
  const [apiStatus, setApiStatus] = useState<string>('Connecting to Jurisiva AI Engine...');
  const [showNewCaseModal, setShowNewCaseModal] = useState<boolean>(false);
  const [isTransitioning, setIsTransitioning] = useState<boolean>(false);
  const [caseName, setCaseName] = useState<string>('Title Diligence — Survey No. 42/1 Hissa 2 Devanahalli');
  const [propertyAddress, setPropertyAddress] = useState<string>('Devanahalli Village, Kasaba Hobli, Bengaluru Rural District, Karnataka');
  const [clientName, setClientName] = useState<string>('State Bank of India (Adv. Rajesh Sharma)');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/health')
      .then(res => res.json())
      .then(() => setApiStatus('● Jurisiva Legal AI Engine Online (200 OK)'))
      .catch(() => setApiStatus('● Jurisiva Legal AI Engine Ready (Standalone Mode)'));
  }, []);

  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const triggerCinematicTransition = () => {
    setIsTransitioning(true);
    setTimeout(() => {
      setIsTransitioning(false);
      onLaunchApp();
    }, 900);
  };

  const handleCreateCaseSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShowNewCaseModal(false);
    triggerCinematicTransition();
  };

  return (
    <div style={{ minHeight: '100vh', background: '#080d19', color: '#f8fafc', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', position: 'relative', overflowX: 'hidden' }}>
      
      {/* Cinematic Courtroom 3D Transition Overlay */}
      {isTransitioning && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            background: 'radial-gradient(circle at center, #1e293b 0%, #080d19 100%)',
            zIndex: 9999,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            animation: 'fadeInZoom 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards',
          }}
        >
          <div style={{ fontSize: '3.5rem', marginBottom: '1rem', animation: 'pulse 1s infinite' }}>🏛️</div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#ffffff', margin: '0 0 0.5rem 0' }}>
            Initializing Property Case Workspace...
          </h2>
          <p style={{ color: '#38bdf8', fontSize: '0.95rem' }}>
            Anchoring deed evidence, OCR parameters & 33-year ownership graph
          </p>
        </div>
      )}

      {/* 1. Header / Navigation */}
      <header style={{ borderBottom: '1px solid rgba(51, 65, 85, 0.45)', background: 'rgba(11, 17, 32, 0.85)', backdropFilter: 'blur(16px)', position: 'sticky', top: 0, zIndex: 100 }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0.85rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer' }} onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: 'linear-gradient(135deg, #2563eb, #1d4ed8)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.25rem', boxShadow: '0 0 15px rgba(37, 99, 235, 0.5)' }}>
              🏛️
            </div>
            <div>
              <span style={{ fontSize: '1.3rem', fontWeight: 800, letterSpacing: '-0.02em', color: '#ffffff' }}>Jurisiva</span>
              <span style={{ fontSize: '1.3rem', fontWeight: 800, color: '#38bdf8' }}>.ai</span>
            </div>
          </div>

          <nav style={{ display: 'flex', gap: '1.75rem', alignItems: 'center' }}>
            <a href="#how-it-works" onClick={(e) => { e.preventDefault(); scrollToSection('how-it-works'); }} style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.9rem', fontWeight: 500 }}>How It Works</a>
            <a href="#ocr-language" onClick={(e) => { e.preventDefault(); scrollToSection('ocr-language'); }} style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.9rem', fontWeight: 500 }}>OCR + Multilingual</a>
            <a href="#ownership-chain" onClick={(e) => { e.preventDefault(); scrollToSection('ownership-chain'); }} style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.9rem', fontWeight: 500 }}>Ownership Chain</a>
            <a href="#comparison" onClick={(e) => { e.preventDefault(); scrollToSection('comparison'); }} style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.9rem', fontWeight: 500 }}>Comparison</a>
            <a href="#risk-engine" onClick={(e) => { e.preventDefault(); scrollToSection('risk-engine'); }} style={{ color: '#94a3b8', textDecoration: 'none', fontSize: '0.9rem', fontWeight: 500 }}>Risk Engine</a>

            <button 
              onClick={() => setShowNewCaseModal(true)}
              style={{ background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)', color: '#ffffff', border: 'none', padding: '0.65rem 1.35rem', borderRadius: '8px', fontSize: '0.9rem', fontWeight: 700, cursor: 'pointer', boxShadow: '0 4px 15px rgba(37, 99, 235, 0.4)' }}
            >
              Start a Property Case →
            </button>
          </nav>
        </div>
      </header>

      {/* 2. Hero Section with Interactive 3D Courtroom Scene */}
      <section style={{ maxWidth: '1200px', margin: '0 auto', padding: '4rem 2rem 3rem 2rem', textAlign: 'center' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(30, 41, 59, 0.6)', border: '1px solid rgba(56, 189, 248, 0.3)', padding: '0.35rem 1rem', borderRadius: '9999px', fontSize: '0.85rem', color: '#38bdf8', marginBottom: '1.25rem', fontWeight: 600, backdropFilter: 'blur(8px)' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', display: 'inline-block', boxShadow: '0 0 8px #10b981' }}></span>
          {apiStatus}
        </div>

        <h1 style={{ fontSize: '3.8rem', fontWeight: 800, letterSpacing: '-0.03em', lineHeight: 1.15, maxWidth: '950px', margin: '0 auto 1.25rem auto', background: 'linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Understand Every Property Document.
        </h1>

        <p style={{ fontSize: '1.25rem', color: '#94a3b8', maxWidth: '780px', margin: '0 auto 2rem auto', lineHeight: 1.6 }}>
          Jurisiva AI reads, compares, connects and analyzes property papers so you can understand ownership, risks and missing evidence faster.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '2.5rem' }}>
          <button 
            onClick={() => setShowNewCaseModal(true)}
            style={{ background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)', color: '#ffffff', border: 'none', padding: '0.95rem 2.25rem', borderRadius: '8px', fontSize: '1.05rem', fontWeight: 700, cursor: 'pointer', boxShadow: '0 8px 25px rgba(37, 99, 235, 0.45)' }}
          >
            Start a Property Case →
          </button>
          <button 
            onClick={() => scrollToSection('how-it-works')}
            style={{ background: 'rgba(30, 41, 59, 0.7)', color: '#f8fafc', border: '1px solid #334155', padding: '0.95rem 1.75rem', borderRadius: '8px', fontSize: '1.05rem', fontWeight: 600, cursor: 'pointer', backdropFilter: 'blur(8px)' }}
          >
            See How It Works ↓
          </button>
        </div>

        {/* VISUAL 01 — INTERACTIVE 3D HERO COURTROOM EXPERIENCE */}
        <Hero3DScene onStartCase={() => setShowNewCaseModal(true)} />
      </section>

      {/* 3. Section 2: How It Works + VISUAL 02 */}
      <section id="how-it-works" style={{ maxWidth: '1200px', margin: '0 auto', padding: '5rem 2rem', borderTop: '1px solid rgba(51, 65, 85, 0.4)' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>4-STEP PROCESS</span>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>How It Works</h2>
          <p style={{ color: '#94a3b8', fontSize: '1.1rem', maxWidth: '650px', margin: '0 auto' }}>From raw documents to an evidence-backed due diligence report.</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '3rem' }}>
          <div style={{ background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '12px', padding: '1.5rem', backdropFilter: 'blur(12px)' }}>
            <div style={{ fontSize: '0.8rem', color: '#38bdf8', fontWeight: 700, marginBottom: '0.5rem' }}>01 UPLOAD</div>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: '0 0 0.5rem 0' }}>Upload</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.5, margin: 0 }}>Upload property papers.</p>
          </div>

          <div style={{ background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '12px', padding: '1.5rem', backdropFilter: 'blur(12px)' }}>
            <div style={{ fontSize: '0.8rem', color: '#38bdf8', fontWeight: 700, marginBottom: '0.5rem' }}>02 UNDERSTAND</div>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: '0 0 0.5rem 0' }}>Understand</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.5, margin: 0 }}>AI extracts text, language, people, dates and property information.</p>
          </div>

          <div style={{ background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '12px', padding: '1.5rem', backdropFilter: 'blur(12px)' }}>
            <div style={{ fontSize: '0.8rem', color: '#38bdf8', fontWeight: 700, marginBottom: '0.5rem' }}>03 ANALYZE</div>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: '0 0 0.5rem 0' }}>Analyze</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.5, margin: 0 }}>AI connects documents and identifies inconsistencies and risks.</p>
          </div>

          <div style={{ background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '12px', padding: '1.5rem', backdropFilter: 'blur(12px)' }}>
            <div style={{ fontSize: '0.8rem', color: '#38bdf8', fontWeight: 700, marginBottom: '0.5rem' }}>04 DECIDE</div>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: '0 0 0.5rem 0' }}>Decide</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', lineHeight: 1.5, margin: 0 }}>Generate evidence-backed findings and a due-diligence report.</p>
          </div>
        </div>

        {/* VISUAL 02 — DOCUMENT UPLOAD */}
        <div style={{ background: 'rgba(15, 23, 42, 0.85)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '1.75rem', backdropFilter: 'blur(12px)' }}>
          <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1rem' }}>VISUAL 02 — DOCUMENT UPLOAD & INGESTION INTERFACE</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.5rem', alignItems: 'center' }}>
            <div className="upload-dropzone" style={{ border: '2px dashed #334155', borderRadius: '10px', padding: '2rem', textAlign: 'center', background: '#0b1120' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>📥</div>
              <div style={{ fontWeight: 700, color: '#ffffff', fontSize: '1.1rem' }}>Drop Property Papers (PDF, Scans, JPG, Photos)</div>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.25rem' }}>Supports old stamp papers and handwritten deeds</div>
            </div>
            <div>
              <div style={{ fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '0.5rem' }}>Processing Pipeline Status:</div>
              <div style={{ background: '#080d19', padding: '1rem', borderRadius: '8px', fontSize: '0.85rem', color: '#34d399', lineHeight: 1.6, border: '1px solid #1e293b' }}>
                ✓ Registered_Sale_Deed_1985.pdf (300 DPI Indic OCR)<br />
                ✓ Mutation_Extract_1986.jpg (Kannada Script Normalization)<br />
                ✓ Mortgage_Deed_2010.pdf (SARFAESI Charge Detection)<br />
                ● Processing Indicator: 100% Ingested & Linked
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Section 3: OCR + Multilingual + VISUAL 03 */}
      <section id="ocr-language" style={{ background: 'rgba(15, 23, 42, 0.65)', borderTop: '1px solid rgba(51, 65, 85, 0.4)', borderBottom: '1px solid rgba(51, 65, 85, 0.4)', padding: '5rem 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>INDIC MULTILINGUAL OCR</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>Old papers. Multiple languages. One workspace.</h2>
            <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>Original scanned document ➔ OCR ➔ detected language ➔ translated text ➔ structured fields.</p>
          </div>

          {/* VISUAL 03 — OCR + LANGUAGE */}
          <div style={{ background: '#0b1120', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '1.75rem' }}>
            <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1rem' }}>VISUAL 03 — OCR + MULTILINGUAL EXTRACTION (ORIGINAL EVIDENCE PRESERVED)</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.25rem' }}>
              <div style={{ background: '#fffbeb', color: '#78350f', border: '1px solid #ca8a04', borderRadius: '8px', padding: '1rem', fontFamily: 'Georgia, serif', fontSize: '0.8rem', lineHeight: 1.5 }}>
                <div style={{ fontWeight: 800, borderBottom: '1px solid #ca8a04', paddingBottom: '0.3rem', marginBottom: '0.5rem' }}>ORIGINAL SCANNED PAGE</div>
                <p>ಕರ್ನಾಟಕ ಸರ್ಕಾರ • ಕ್ರಯ ಪತ್ರ</p>
                <p>ಸರ್ವೆ ನಂ: 42/1 ಹಿಸ್ಸಾ 2</p>
                <p>ವಿಸ್ತೀರ್ಣ: 2 ಎಕರೆ 24 ಗುಂಟೆ</p>
                <p>ಮಾರಾಟಗಾರ: ವೆಂಕಟಪ್ಪ</p>
              </div>

              <div style={{ background: '#080d19', border: '1px solid #1e293b', borderRadius: '8px', padding: '1rem', fontSize: '0.85rem' }}>
                <div style={{ color: '#38bdf8', fontWeight: 700, marginBottom: '0.5rem' }}>DETECTED LANGUAGE: KANNADA (kn)</div>
                <div style={{ color: '#cbd5e1', lineHeight: 1.6 }}>
                  <strong>English Translation:</strong><br />
                  Deed of Absolute Sale<br />
                  Survey No: 42/1 Hissa 2<br />
                  Extent: 2 Acres 24 Guntas<br />
                  Executant: Venkatappa
                </div>
              </div>

              <div style={{ background: '#080d19', border: '1px solid #10b981', borderRadius: '8px', padding: '1rem', fontSize: '0.85rem' }}>
                <div style={{ color: '#34d399', fontWeight: 700, marginBottom: '0.5rem' }}>STRUCTURED EXTRACTED FIELDS</div>
                <div style={{ color: '#cbd5e1', lineHeight: 1.6 }}>
                  • <strong>Survey:</strong> 42/1 Hissa 2<br />
                  • <strong>Area:</strong> 2A 24G (104,544 Sq.Ft)<br />
                  • <strong>Confidence:</strong> 96.8%<br />
                  • <strong>Status:</strong> Original Preserved
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Section 4: Property Facts */}
      <section id="property-facts" style={{ maxWidth: '1200px', margin: '0 auto', padding: '5rem 2rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>STRUCTURED PROPERTY FACTS</span>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>Every Fact Backed by Page Evidence</h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
          <div className="card" style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)' }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700 }}>OWNER</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', margin: '0.25rem 0' }}>Sri. Venkatappa</div>
            <div style={{ fontSize: '0.75rem', color: '#38bdf8' }}>Doc #1234/1985 (Pg 1) • 98% Conf</div>
          </div>
          <div className="card" style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)' }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700 }}>SURVEY NUMBER</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', margin: '0.25rem 0' }}>42/1 Hissa 2</div>
            <div style={{ fontSize: '0.75rem', color: '#38bdf8' }}>Doc #1234/1985 (Pg 3) • 99% Conf</div>
          </div>
          <div className="card" style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)' }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700 }}>AREA / EXTENT</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', margin: '0.25rem 0' }}>2 Acres 24 Guntas</div>
            <div style={{ fontSize: '0.75rem', color: '#38bdf8' }}>Doc #1234/1985 (Pg 3) • 97% Conf</div>
          </div>
          <div className="card" style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(51, 65, 85, 0.5)' }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700 }}>REGISTRATION NUMBER</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', margin: '0.25rem 0' }}>1234/1985-86</div>
            <div style={{ fontSize: '0.75rem', color: '#38bdf8' }}>SRO Devanahalli (Pg 1) • 99% Conf</div>
          </div>
        </div>
      </section>

      {/* 6. Section 5: Ownership Chain + VISUAL 04 */}
      <section id="ownership-chain" style={{ background: 'rgba(15, 23, 42, 0.65)', borderTop: '1px solid rgba(51, 65, 85, 0.4)', borderBottom: '1px solid rgba(51, 65, 85, 0.4)', padding: '5rem 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>GENEALOGY & TITLE DEVOLUTION</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>See how ownership moved.</h2>
          </div>

          {/* VISUAL 04 — OWNERSHIP CHAIN */}
          <div style={{ background: '#0b1120', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '2rem', maxWidth: '750px', margin: '0 auto' }}>
            <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1.5rem', textAlign: 'center' }}>
              VISUAL 04 — CLICKABLE OWNERSHIP CHAIN (OPENS SOURCE DOC & EXTRACTED EVIDENCE)
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ background: '#080d19', border: '2px solid #3b82f6', borderRadius: '8px', padding: '1rem', cursor: 'pointer' }} onClick={onLaunchApp}>
                <div style={{ color: '#38bdf8', fontSize: '0.75rem', fontWeight: 700 }}>OWNER A (1985)</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff' }}>Sri. Venkatappa (Absolute Title Holder)</div>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.2rem' }}>Source: Registered Sale Deed #1234/1985 (Page 2) [Click to inspect]</div>
              </div>

              <div style={{ textAlign: 'center', color: '#38bdf8', fontWeight: 800 }}>↓ [Absolute Sale Transfer]</div>

              <div style={{ background: '#080d19', border: '2px solid #3b82f6', borderRadius: '8px', padding: '1rem', cursor: 'pointer' }} onClick={onLaunchApp}>
                <div style={{ color: '#38bdf8', fontSize: '0.75rem', fontWeight: 700 }}>OWNER B (1986)</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff' }}>Sri. Krishnappa S/o Venkatappa</div>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.2rem' }}>Source: Mutation Extract M.R. No. 14/1986 under Sec 128 KLR Act</div>
              </div>

              <div style={{ textAlign: 'center', color: '#fbbf24', fontWeight: 800 }}>↓ [Inheritance & 2010 SBI Loan]</div>

              <div style={{ background: '#080d19', border: '2px solid #ef4444', borderRadius: '8px', padding: '1rem', cursor: 'pointer' }} onClick={onLaunchApp}>
                <div style={{ color: '#f87171', fontSize: '0.75rem', fontWeight: 700 }}>CURRENT OWNER (2018)</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff' }}>Sri. Anand Kumar (Current Claimant)</div>
                <div style={{ fontSize: '0.8rem', color: '#fca5a5', marginTop: '0.2rem' }}>Source: Sale Deed #890/2018 (Page 4) • ⚠️ 14 Guntas Shortage Detected</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Section 6: Property Timeline + VISUAL 08 */}
      <section id="timeline-section" style={{ maxWidth: '1200px', margin: '0 auto', padding: '5rem 2rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>CHRONOLOGICAL RECONSTRUCTION</span>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>Property Timeline</h2>
        </div>

        {/* VISUAL 08 — PROPERTY TIMELINE */}
        <div style={{ background: 'rgba(15, 23, 42, 0.85)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '2rem' }}>
          <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1.5rem' }}>VISUAL 08 — TRANSACTION & MUTATION TIMELINE</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1rem', textAlign: 'center' }}>
            <div style={{ background: '#080d19', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
              <div style={{ color: '#38bdf8', fontWeight: 800, fontSize: '1.25rem' }}>1998</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', marginTop: '0.25rem' }}>Original Ownership</div>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
              <div style={{ color: '#38bdf8', fontWeight: 800, fontSize: '1.25rem' }}>2005</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', marginTop: '0.25rem' }}>Sale Transfer</div>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
              <div style={{ color: '#38bdf8', fontWeight: 800, fontSize: '1.25rem' }}>2012</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', marginTop: '0.25rem' }}>Inheritance / Khata</div>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #334155', borderRadius: '8px', padding: '1rem' }}>
              <div style={{ color: '#38bdf8', fontWeight: 800, fontSize: '1.25rem' }}>2019</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', marginTop: '0.25rem' }}>Registration</div>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #10b981', borderRadius: '8px', padding: '1rem' }}>
              <div style={{ color: '#34d399', fontWeight: 800, fontSize: '1.25rem' }}>2026</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', marginTop: '0.25rem' }}>Current Record</div>
            </div>
          </div>
        </div>
      </section>

      {/* 8. Section 7: Document Comparison + VISUAL 05 */}
      <section id="comparison" style={{ background: 'rgba(15, 23, 42, 0.65)', borderTop: '1px solid rgba(51, 65, 85, 0.4)', borderBottom: '1px solid rgba(51, 65, 85, 0.4)', padding: '5rem 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>SIDE-BY-SIDE DIFF</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>Compare documents side by side.</h2>
          </div>

          {/* VISUAL 05 — DOCUMENT COMPARISON */}
          <div style={{ background: '#0b1120', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '2rem' }}>
            <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1rem' }}>VISUAL 05 — DOCUMENT COMPARISON & DISCREPANCY DETECTOR</div>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '0.75rem', background: '#080d19', color: '#94a3b8' }}>Field / Clause</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem', background: '#080d19', color: '#94a3b8' }}>Document A (1985 Deed)</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem', background: '#080d19', color: '#94a3b8' }}>Document B (2018 Deed)</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem', background: '#080d19', color: '#94a3b8' }}>Difference Severity</th>
                </tr>
              </thead>
              <tbody>
                <tr style={{ borderBottom: '1px solid #1e293b' }}>
                  <td style={{ padding: '0.75rem' }}><strong>Survey Number</strong></td>
                  <td style={{ padding: '0.75rem' }}>Survey No. 124/2 (Pg 3)</td>
                  <td style={{ padding: '0.75rem' }}>Survey No. 124/3 (Pg 7)</td>
                  <td style={{ padding: '0.75rem' }}><strong style={{ color: '#ef4444' }}>HIGH IMPORTANCE</strong></td>
                </tr>
                <tr style={{ borderBottom: '1px solid #1e293b' }}>
                  <td style={{ padding: '0.75rem' }}><strong>Property Area</strong></td>
                  <td style={{ padding: '0.75rem' }}>2 Acres 24 Guntas</td>
                  <td style={{ padding: '0.75rem' }}>2 Acres 10 Guntas</td>
                  <td style={{ padding: '0.75rem' }}><strong style={{ color: '#ef4444' }}>CRITICAL (-14 Guntas)</strong></td>
                </tr>
                <tr>
                  <td style={{ padding: '0.75rem' }}><strong>Boundaries</strong></td>
                  <td style={{ padding: '0.75rem' }}>Sy No 42/2 (Govindappa)</td>
                  <td style={{ padding: '0.75rem' }}>Private Layout Road</td>
                  <td style={{ padding: '0.75rem' }}><strong style={{ color: '#f59e0b' }}>MEDIUM (Boundary Shift)</strong></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* 9. Section 8: Risk Engine + VISUAL 06 */}
      <section id="risk-engine" style={{ maxWidth: '1200px', margin: '0 auto', padding: '5rem 2rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#ef4444', fontWeight: 700 }}>RISK CLASSIFICATION</span>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>Forensic Legal Risk Engine</h2>
        </div>

        {/* VISUAL 06 — RISK ANALYSIS */}
        <div style={{ background: 'rgba(15, 23, 42, 0.85)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '2rem' }}>
          <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1rem' }}>VISUAL 06 — RISK ANALYSIS & EVIDENCE CITATIONS</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
            <div style={{ background: '#080d19', border: '1px solid #ef4444', borderRadius: '8px', padding: '1rem' }}>
              <span style={{ fontSize: '0.75rem', background: '#7f1d1d', color: '#fecaca', padding: '0.2rem 0.5rem', borderRadius: '4px', fontWeight: 700 }}>CRITICAL</span>
              <h4 style={{ margin: '0.5rem 0 0.25rem 0', color: '#ffffff' }}>Encumbrance Risk</h4>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: 0 }}>Active unreleased SBI ₹50L mortgage on record.</p>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #f59e0b', borderRadius: '8px', padding: '1rem' }}>
              <span style={{ fontSize: '0.75rem', background: '#78350f', color: '#fde68a', padding: '0.2rem 0.5rem', borderRadius: '4px', fontWeight: 700 }}>HIGH</span>
              <h4 style={{ margin: '0.5rem 0 0.25rem 0', color: '#ffffff' }}>Boundary / Area Risk</h4>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: 0 }}>14 Guntas shortfall between 1985 and 2018 deeds.</p>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #3b82f6', borderRadius: '8px', padding: '1rem' }}>
              <span style={{ fontSize: '0.75rem', background: '#1e3a8a', color: '#93c5fd', padding: '0.2rem 0.5rem', borderRadius: '4px', fontWeight: 700 }}>MEDIUM</span>
              <h4 style={{ margin: '0.5rem 0 0.25rem 0', color: '#ffffff' }}>Identity / Heir Risk</h4>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: 0 }}>Missing Tahsildar Family Tree (Vamshavruksha).</p>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #10b981', borderRadius: '8px', padding: '1rem' }}>
              <span style={{ fontSize: '0.75rem', background: '#064e3b', color: '#a7f3d0', padding: '0.2rem 0.5rem', borderRadius: '4px', fontWeight: 700 }}>LOW</span>
              <h4 style={{ margin: '0.5rem 0 0.25rem 0', color: '#ffffff' }}>Registration Risk</h4>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: 0 }}>Stamp duty paid in full and recorded in Book 1.</p>
            </div>
          </div>
        </div>
      </section>

      {/* 10. Section 9: Evidence-First AI + VISUAL 07 */}
      <section id="evidence-panel" style={{ background: 'rgba(15, 23, 42, 0.65)', borderTop: '1px solid rgba(51, 65, 85, 0.4)', borderBottom: '1px solid rgba(51, 65, 85, 0.4)', padding: '5rem 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>ZERO HALLUCINATION</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>AI answers backed by your documents.</h2>
          </div>

          {/* VISUAL 07 — EVIDENCE PANEL */}
          <div style={{ background: '#0b1120', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '2rem', maxWidth: '750px', margin: '0 auto' }}>
            <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1rem' }}>VISUAL 07 — EVIDENCE-GROUNDED AI ANSWER CARD</div>
            <div style={{ background: '#080d19', border: '1px solid #334155', borderRadius: '8px', padding: '1.25rem' }}>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8', fontWeight: 700 }}>QUESTION:</div>
              <div style={{ fontSize: '1rem', color: '#ffffff', fontWeight: 600, margin: '0.25rem 0 0.75rem 0' }}>Who is the current owner?</div>
              
              <div style={{ fontSize: '0.85rem', color: '#34d399', fontWeight: 700 }}>ANSWER:</div>
              <div style={{ fontSize: '0.95rem', color: '#f8fafc', lineHeight: 1.5, margin: '0.25rem 0 0.75rem 0' }}>
                The latest identified owner is Sri. Anand Kumar, who purchased 2 Acres 10 Guntas in Survey No. 42/1 Hissa 2.
              </div>

              <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.8rem', color: '#38bdf8', borderTop: '1px solid #1e293b', paddingTop: '0.5rem' }}>
                <span><strong>SOURCE:</strong> Registered Sale Deed 2018</span>
                <span><strong>PAGE:</strong> Page 7</span>
                <span><strong>CONFIDENCE:</strong> 92%</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 11. Section 10: Legal Research + VISUAL 09 */}
      <section id="legal-research" style={{ maxWidth: '1200px', margin: '0 auto', padding: '5rem 2rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>APEX COURT PRECEDENT GRAPH</span>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>AI Legal Research Workspace</h2>
          <p style={{ color: '#94a3b8' }}>Clearly distinguishing Document Evidence from Legal Research from AI Interpretation.</p>
        </div>

        {/* VISUAL 09 — LEGAL RESEARCH */}
        <div style={{ background: 'rgba(15, 23, 42, 0.85)', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '2rem' }}>
          <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700, marginBottom: '1rem' }}>VISUAL 09 — LEGAL RESEARCH & CITATION AUTHORITY</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            <div style={{ background: '#080d19', border: '1px solid #334155', borderRadius: '8px', padding: '1.25rem' }}>
              <h4 style={{ color: '#38bdf8', margin: '0 0 0.5rem 0' }}>🏛️ 2023 INSC 891 — Anandram vs. LAO Bangalore Rural</h4>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5, margin: 0 }}>
                <strong>Ratio Decidendi:</strong> Where deed extent differs from revenue settlement akarband, official physical spot durasti survey prevails over unrectified boundaries under Section 106 KLR Act.
              </p>
            </div>
            <div style={{ background: '#080d19', border: '1px solid #334155', borderRadius: '8px', padding: '1.25rem' }}>
              <h4 style={{ color: '#fbbf24', margin: '0 0 0.5rem 0' }}>🏦 2018 7 SCC 446 — Indian Bank vs. Blue Jaggers Estates</h4>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5, margin: 0 }}>
                <strong>SARFAESI Rule:</strong> A registered simple mortgage remains enforceable against any subsequent purchaser until an official Discharge Deed is executed by the secured creditor.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 12. Section 11: Final Report + VISUAL 10 */}
      <section id="final-report" style={{ background: 'rgba(15, 23, 42, 0.65)', borderTop: '1px solid rgba(51, 65, 85, 0.4)', borderBottom: '1px solid rgba(51, 65, 85, 0.4)', padding: '5rem 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>COURT-READY DELIVERABLE</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>From documents to a decision-ready report.</h2>
          </div>

          {/* VISUAL 10 — DUE DILIGENCE REPORT */}
          <div style={{ background: '#0b1120', border: '1px solid rgba(51, 65, 85, 0.5)', borderRadius: '14px', padding: '2rem', maxWidth: '850px', margin: '0 auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <div>
                <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 700 }}>VISUAL 10 — PROPERTY DUE DILIGENCE REPORT</div>
                <h3 style={{ margin: '0.25rem 0 0 0', color: '#ffffff' }}>Title Assessment Dossier: Survey No. 42/1 Hissa 2</h3>
              </div>
              <button 
                onClick={onLaunchApp}
                style={{ background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)', color: '#ffffff', border: 'none', padding: '0.6rem 1.25rem', borderRadius: '6px', fontSize: '0.85rem', fontWeight: 700, cursor: 'pointer' }}
              >
                Generate Due Diligence Report (PDF) →
              </button>
            </div>

            <div style={{ background: '#080d19', padding: '1.25rem', borderRadius: '8px', fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6, border: '1px solid #1e293b' }}>
              • <strong>1. Executive Summary:</strong> Conditional Marketable Title subject to Bank Discharge Deed & Durasti Demarcation.<br />
              • <strong>2. Property Details:</strong> Survey No. 42/1 Hissa 2, Devanahalli Taluk, Bengaluru Rural District (2A 24G Khuski).<br />
              • <strong>3. Ownership History:</strong> 1985 Venkatappa ➔ 1986 Krishnappa ➔ 2018 Anand Kumar.<br />
              • <strong>4. Identified Issues:</strong> 14 Guntas Shortfall • Active SBI ₹50L Mortgage.<br />
              • <strong>5. Missing Documents:</strong> Registered Mortgage Discharge Deed, ADLR 11E Survey Map, Family Tree.<br />
      {/* Courtroom & Chambers Gallery Showcase */}
      <section style={{ maxWidth: '1200px', margin: '0 auto', padding: '5rem 2rem', borderTop: '1px solid rgba(51, 65, 85, 0.4)' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>GROUND TRUTH IN PRACTICE</span>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0' }}>Built for High Courts, Benches & Law Chambers</h2>
          <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>Designed specifically for the precision standards of Indian advocates and litigating counsel.</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1.3fr 1fr', gap: '1.5rem' }}>
          <div style={{ position: 'relative', borderRadius: '12px', overflow: 'hidden', border: '1px solid #334155', minHeight: '380px', background: '#0b1120' }}>
            <video autoPlay muted loop playsInline poster="http://127.0.0.1:8000/api/v1/media/supreme-court.jpg" className="jurisiva-video">
              <source src="assets/video/courtroom-walk.mp4" type="video/mp4" />
            </video>
            <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(11,17,32,0.1) 0%, rgba(11,17,32,0.85) 100%)', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', padding: '1.5rem' }}>
              <span style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Courtroom Intelligence</span>
              <h3 style={{ margin: '0.25rem 0', color: '#ffffff', fontSize: '1.3rem' }}>Apex & High Court Bench Trial Intelligence</h3>
              <p style={{ color: '#94a3b8', fontSize: '0.85rem', margin: 0 }}>Direct integration with eCourts and NJDG records for instant case status and citations.</p>
            </div>
          </div>

          <div style={{ position: 'relative', borderRadius: '12px', overflow: 'hidden', border: '1px solid #334155', minHeight: '380px', background: '#0b1120' }}>
            <video autoPlay muted loop playsInline poster="http://127.0.0.1:8000/api/v1/media/advocates.jpg" className="jurisiva-video">
              <source src="assets/video/brand-film.mp4" type="video/mp4" />
            </video>
            <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(11,17,32,0.1) 0%, rgba(11,17,32,0.85) 100%)', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', padding: '1.5rem' }}>
              <span style={{ fontSize: '0.75rem', color: '#34d399', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Advocate Workspace</span>
              <h3 style={{ margin: '0.25rem 0', color: '#ffffff', fontSize: '1.3rem' }}>Chamber Due Diligence & Briefs</h3>
              <p style={{ color: '#94a3b8', fontSize: '0.85rem', margin: 0 }}>Collaborative multi-advocate workspaces with Indic OCR translation and title genealogy.</p>
            </div>
          </div>
        </div>
      </section>

      {/* 13. Final CTA Banner */}
      <section style={{ maxWidth: '1200px', margin: '0 auto', padding: '6rem 2rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem', alignItems: 'center' }}>
          <div>
            <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: '#38bdf8', fontWeight: 700 }}>GET STARTED</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#ffffff', margin: '0.5rem 0 1rem' }}>
              Bring evidence-grounded AI into your chambers.
            </h2>
            <p style={{ color: '#94a3b8', fontSize: '1.1rem', marginBottom: '2rem', lineHeight: 1.6 }}>
              Jurisiva AI is onboarding litigation chambers, senior partners, and in-house real-estate legal teams across India for accelerated property due diligence and title intelligence.
            </p>
            <button 
              onClick={() => setShowNewCaseModal(true)}
              style={{ background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)', color: '#ffffff', border: 'none', padding: '1rem 2.5rem', borderRadius: '8px', fontSize: '1.1rem', fontWeight: 700, cursor: 'pointer', boxShadow: '0 8px 25px rgba(37, 99, 235, 0.45)' }}
            >
              Start a Property Case →
            </button>
          </div>

          <div style={{ position: 'relative', borderRadius: '12px', overflow: 'hidden', border: '1px solid #334155', minHeight: '340px', background: '#0b1120', boxShadow: '0 25px 50px -12px rgba(0,0,0,0.8)' }}>
            <img 
              src="http://127.0.0.1:8000/api/v1/media/senior_partner.jpg" 
              onError={(e) => { (e.currentTarget as HTMLImageElement).src = '/images/senior_partner.jpg'; }}
              alt="Senior Managing Partner in Chambers" 
              style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
            />
            <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(11,17,32,0.1) 0%, rgba(11,17,32,0.92) 100%)', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', padding: '1.5rem' }}>
              <span style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Senior Counsel Endorsement</span>
              <h3 style={{ margin: '0.25rem 0', color: '#ffffff', fontSize: '1.15rem' }}>"Jurisiva gives our chambers certainty before any opinion leaves our desk."</h3>
              <p style={{ color: '#94a3b8', fontSize: '0.82rem', margin: 0 }}>Senior Managing Partner • Real Estate & Dispute Resolution Chambers</p>
            </div>
          </div>
        </div>
      </section>

      {/* NEW CASE MODAL */}
      {showNewCaseModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(8px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '12px', padding: '2rem', maxWidth: '550px', width: '90%', boxShadow: '0 25px 50px -12px rgba(0,0,0,0.8)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontSize: '1.5rem' }}>📁</span>
                <h3 style={{ margin: 0, color: '#ffffff', fontSize: '1.25rem' }}>Create New Property Case</h3>
              </div>
              <button onClick={() => setShowNewCaseModal(false)} style={{ background: 'transparent', border: 'none', color: '#94a3b8', fontSize: '1.25rem', cursor: 'pointer' }}>✕</button>
            </div>

            <form onSubmit={handleCreateCaseSubmit}>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '0.35rem' }}>Case Name</label>
                <input 
                  type="text" 
                  value={caseName} 
                  onChange={(e) => setCaseName(e.target.value)} 
                  required 
                  style={{ width: '100%', padding: '0.75rem', background: '#1e293b', border: '1px solid #334155', borderRadius: '6px', color: '#ffffff' }}
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '0.35rem' }}>Property Address / Survey Details</label>
                <input 
                  type="text" 
                  value={propertyAddress} 
                  onChange={(e) => setPropertyAddress(e.target.value)} 
                  required 
                  style={{ width: '100%', padding: '0.75rem', background: '#1e293b', border: '1px solid #334155', borderRadius: '6px', color: '#ffffff' }}
                />
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '0.35rem' }}>Client / Lead Advocate</label>
                <input 
                  type="text" 
                  value={clientName} 
                  onChange={(e) => setClientName(e.target.value)} 
                  style={{ width: '100%', padding: '0.75rem', background: '#1e293b', border: '1px solid #334155', borderRadius: '6px', color: '#ffffff' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
                <button type="button" className="btn-secondary" onClick={() => setShowNewCaseModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary">Create Case & Open Workspace →</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer style={{ borderTop: '1px solid rgba(51, 65, 85, 0.4)', background: '#080d19', padding: '2.5rem 2rem' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: '#64748b', fontSize: '0.85rem' }}>
          <div>© 2026 Jurisiva AI Platforms Inc. All rights reserved. Built for Legal Advocates & Real Estate Developers.</div>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            <span>Privacy Policy</span>
            <span>Security Compliance</span>
            <span>API Docs</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
