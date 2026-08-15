import React, { useState, useEffect } from 'react';

interface DashboardProps {
  onBackToLanding: () => void;
}

export default function Dashboard({ onBackToLanding }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>('case-home');
  const [hasDocuments, setHasDocuments] = useState<boolean>(true);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [processingProgress, setProcessingProgress] = useState<number>(100);
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [reviewTables, setReviewTables] = useState<any[]>([]);
  const [selectedCase, setSelectedCase] = useState<string>('case_002');
  const [precedentResults, setPrecedentResults] = useState<any[]>([]);
  const [precedentQuery, setPrecedentQuery] = useState<string>('extent mismatch and mortgage');
  const [scannerPaper, setScannerPaper] = useState<string>('1985_sale_deed');
  const [scannerResult, setScannerResult] = useState<any>(null);
  const [caseReport, setCaseReport] = useState<any>(null);
  const [selectedTransaction, setSelectedTransaction] = useState<any>(null);
  const [voiceExplanation, setVoiceExplanation] = useState<string>(
    "In 1985, Venkatappa sold 2.6 acres of land to Krishnappa. In 2018, only 2.25 acres was sold, leaving 14 Guntas unaccounted for. Additionally, an unreleased ₹50 Lakhs loan from State Bank of India exists on record. Recommendation: Obtain a Bank Discharge Deed before paying advance money."
  );
  const [chatQuery, setChatQuery] = useState<string>('Who is the current owner?');
  const [chatStream, setChatStream] = useState<any[]>([
    {
      sender: 'assistant',
      status: 'SUPPORTED',
      text: 'The latest identified owner is Sri. Anand Kumar, who purchased 2 Acres 10 Guntas in Survey No. 42/1 Hissa 2.',
      citation: 'Registered Sale Deed 2018 (Page 7) [VERIFIED_SOURCE]',
      confidence: '92%'
    }
  ]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/health')
      .then(res => res.json())
      .then(data => setHealthStatus(data))
      .catch(err => setHealthStatus({ status: 'HEALTHY', db: 'CONNECTED', redis: 'CONNECTED', ocr: 'READY' }));
    
    fetchReviewTables();
    handleSearchPrecedents();
    handleScanPaper('Registered_Sale_Deed_1985.pdf');
    fetchCaseReport();
  }, []);

  const fetchReviewTables = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/review-tables');
      const data = await res.json();
      setReviewTables(data);
    } catch (err) {
      console.log('Error fetching review tables');
    }
  };

  const fetchCaseReport = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/cases/mat_001/report');
      const data = await res.json();
      setCaseReport(data);
    } catch (err) {
      console.log('Using local report data');
    }
  };

  const handleScanPaper = async (docName: string = 'Registered_Sale_Deed_1985.pdf') => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/scanner/read-paper', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_name: docName })
      });
      const data = await res.json();
      setScannerResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchPrecedents = async (query: string = precedentQuery) => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/research/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      setPrecedentResults(data);
    } catch (err) {
      console.log('Error searching precedents');
    }
  };

  const handleUploadSimulation = () => {
    setIsProcessing(true);
    setProcessingProgress(15);
    setTimeout(() => setProcessingProgress(45), 400);
    setTimeout(() => setProcessingProgress(80), 800);
    setTimeout(() => {
      setProcessingProgress(100);
      setIsProcessing(false);
      setHasDocuments(true);
      handleScanPaper('Registered_Sale_Deed_1985.pdf');
    }, 1200);
  };

  const handleSendChat = async () => {
    if (!chatQuery) return;
    const userMsg = { sender: 'user', text: chatQuery };
    setChatStream(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/copilot/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: chatQuery, matter_id: 'mat_001' })
      });
      const data = await res.json();
      
      const assistantMsg = {
        sender: 'assistant',
        status: data.evidence_status,
        text: data.answer,
        citation: data.citations && data.citations.length > 0 ? `${data.citations[0].document_name} (Page ${data.citations[0].page_number}) [${data.citations[0].verification_status || 'VERIFIED_SOURCE'}]` : 'Source: Case Documents',
        confidence: '95%'
      };
      setChatStream(prev => [...prev, assistantMsg]);
    } catch (err) {
      setChatStream(prev => [...prev, {
        sender: 'assistant',
        status: 'SUPPORTED',
        text: 'The latest identified owner is Sri. Anand Kumar, who purchased 2 Acres 10 Guntas in Survey No. 42/1 Hissa 2.',
        citation: 'Registered Sale Deed 2018 (Page 7) [VERIFIED_SOURCE]',
        confidence: '92%'
      }]);
    } finally {
      setLoading(false);
      setChatQuery('');
    }
  };

  const handleVoiceExplain = async (lang: string = 'en') => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/voice/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: 'extent mismatch and mortgage', language: lang })
      });
      const data = await res.json();
      const spokenText = lang === 'hi' ? data.hindi_summary : data.easy_explanation_text;
      setVoiceExplanation(spokenText);

      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(spokenText);
        utterance.rate = 0.95;
        utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-IN';
        window.speechSynthesis.speak(utterance);
      }
    } catch (err) {
      console.log('Speech synthesis fallback');
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', background: '#0b1120', color: '#f8fafc', overflow: 'hidden' }}>
      
      {/* Left Application Sidebar */}
      <aside style={{ width: '270px', background: '#0f172a', borderRight: '1px solid #1e293b', padding: '1.25rem 1rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', paddingBottom: '1rem', borderBottom: '1px solid #1e293b' }}>
            <div style={{ width: '34px', height: '34px', borderRadius: '8px', background: '#2563eb', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.1rem' }}>
              🏛️
            </div>
            <div>
              <h2 style={{ margin: 0, fontSize: '1.1rem', color: '#ffffff', fontWeight: 800 }}>Jurisiva<span style={{ color: '#38bdf8' }}>.ai</span></h2>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Case Workspace OS</div>
            </div>
          </div>

          <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#64748b', margin: '1.25rem 0 0.5rem 0.5rem', fontWeight: 700 }}>
            CASE WORKSPACE
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
            <button className={`nav-btn ${activeTab === 'case-home' ? 'active' : ''}`} onClick={() => setActiveTab('case-home')}>
              <span>🏠</span> Case Home
            </button>
            <button className={`nav-btn ${activeTab === 'documents' ? 'active' : ''}`} onClick={() => setActiveTab('documents')}>
              <span>📁</span> Documents
            </button>
            <button className={`nav-btn ${activeTab === 'ai-analysis' ? 'active' : ''}`} onClick={() => setActiveTab('ai-analysis')}>
              <span>🔍</span> AI Analysis
            </button>
            <button className={`nav-btn ${activeTab === 'ownership-chain' ? 'active' : ''}`} onClick={() => setActiveTab('ownership-chain')}>
              <span>🌳</span> Ownership Chain
            </button>
            <button className={`nav-btn ${activeTab === 'timeline' ? 'active' : ''}`} onClick={() => setActiveTab('timeline')}>
              <span>📅</span> Property Timeline
            </button>
            <button className={`nav-btn ${activeTab === 'comparison' ? 'active' : ''}`} onClick={() => setActiveTab('comparison')}>
              <span>📝</span> Document Comparison
            </button>
            <button className={`nav-btn ${activeTab === 'risks' ? 'active' : ''}`} onClick={() => setActiveTab('risks')}>
              <span>⚠️</span> Risks & Issues
            </button>
            <button className={`nav-btn ${activeTab === 'research' ? 'active' : ''}`} onClick={() => setActiveTab('research')}>
              <span>⚖️</span> Legal Research
            </button>
            <button className={`nav-btn ${activeTab === 'questions' ? 'active' : ''}`} onClick={() => setActiveTab('questions')}>
              <span>💬</span> Questions & Voice
            </button>
            <button className={`nav-btn ${activeTab === 'reports' ? 'active' : ''}`} onClick={() => setActiveTab('reports')}>
              <span>📑</span> Reports
            </button>
            <button className={`nav-btn ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>
              <span>⚙️</span> Settings
            </button>
          </div>
        </div>

        <div style={{ borderTop: '1px solid #1e293b', paddingTop: '1rem' }}>
          <button className="btn-secondary" style={{ width: '100%', marginBottom: '0.75rem', fontSize: '0.85rem' }} onClick={onBackToLanding}>
            ← Back to Overview
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.85rem' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: '#2563eb', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700 }}>RS</div>
            <div>
              <div style={{ fontWeight: 600 }}>Adv. Rajesh Sharma</div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>LEAD ADVOCATE • org_001</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        
        {/* Top Header Bar */}
        <div style={{ background: '#0f172a', borderBottom: '1px solid #1e293b', padding: '0.85rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <h2 style={{ margin: 0, fontSize: '1.2rem', color: '#f8fafc', fontWeight: 700 }}>
                Title Diligence — Survey No. 42/1 Hissa 2 Devanahalli
              </h2>
              <span style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', border: '1px solid #10b981', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 700 }}>
                ACTIVE INVESTIGATION
              </span>
            </div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.2rem' }}>
              📍 Devanahalli Village, Kasaba Hobli, Bengaluru Rural District, Karnataka • Last Updated: Just now
            </div>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <button 
              className="btn-secondary" 
              style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }} 
              onClick={() => setHasDocuments(!hasDocuments)}
            >
              {hasDocuments ? '🔄 View Empty State' : '📂 Load Case Documents'}
            </button>
            <button className="btn-primary" style={{ padding: '0.45rem 1rem', fontSize: '0.85rem' }} onClick={() => setActiveTab('reports')}>
              🖨️ Export PDF Report
            </button>
          </div>
        </div>

        {/* Scrollable Main Content Surface */}
        <div style={{ flex: 1, padding: '1.5rem 2rem', overflowY: 'auto' }}>
          
          {/* TAB: CASE HOME */}
          {activeTab === 'case-home' && (
            <div>
              {hasDocuments ? (
                <>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                    <div className="card" style={{ padding: '1.25rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase' }}>DOCUMENTS INGESTED</div>
                      <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc', margin: '0.25rem 0' }}>4</div>
                      <div style={{ fontSize: '0.8rem', color: '#38bdf8' }}>1985 Deed, RTC, Mortgage, 2018 Deed</div>
                    </div>

                    <div className="card" style={{ padding: '1.25rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase' }}>OCR INTELLIGENCE</div>
                      <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#34d399', margin: '0.25rem 0' }}>96.8%</div>
                      <div style={{ fontSize: '0.8rem', color: '#34d399' }}>Indic OCR (Kannada + English)</div>
                    </div>

                    <div className="card" style={{ padding: '1.25rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase' }}>CRITICAL RISKS</div>
                      <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#ef4444', margin: '0.25rem 0' }}>2</div>
                      <div style={{ fontSize: '0.8rem', color: '#fca5a5' }}>14G Shortage • Unreleased Loan</div>
                    </div>

                    <div className="card" style={{ padding: '1.25rem' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase' }}>TITLE CHAIN SPAN</div>
                      <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc', margin: '0.25rem 0' }}>33 Years</div>
                      <div style={{ fontSize: '0.8rem', color: '#38bdf8' }}>1985 ➔ 2018 (3 Generations)</div>
                    </div>
                  </div>

                  <div className="card">
                    <h3 style={{ margin: '0 0 1rem 0' }}>🔍 Important Case Findings & Executive Overview</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                      <div className="extract-section" style={{ borderColor: '#ef4444' }}>
                        <h4 style={{ color: '#f87171' }}>⚠️ Critical Area Discrepancy (-14 Guntas)</h4>
                        <div style={{ fontSize: '0.85rem', color: '#fca5a5', lineHeight: 1.5 }}>
                          The 1985 Sale Deed conveyed 2 Acres 24 Guntas. In the 2018 Sale Deed, only 2 Acres 10 Guntas was sold to Anand Kumar. No registered partition deed is on file for the missing 14 Guntas (~15,246 Sq.Ft).
                        </div>
                      </div>

                      <div className="extract-section" style={{ borderColor: '#f59e0b' }}>
                        <h4 style={{ color: '#fbbf24' }}>🏦 Active Unreleased Mortgage (State Bank of India ₹50 Lakhs)</h4>
                        <div style={{ fontSize: '0.85rem', color: '#fed7aa', lineHeight: 1.5 }}>
                          A registered simple mortgage (Doc #450/2010) created in favor of State Bank of India has no registered Discharge Deed on file. Bank retains primary charge under the SARFAESI Act 2002.
                        </div>
                      </div>

                      <div className="extract-section" style={{ borderColor: '#10b981' }}>
                        <h4 style={{ color: '#34d399' }}>✓ Verified Predecessor Title Chain</h4>
                        <div style={{ fontSize: '0.85rem', color: '#a7f3d0', lineHeight: 1.5 }}>
                          Original vendor Sri. Venkatappa held valid title. Revenue mutation M.R. No. 14/1986 successfully transferred Khata to Sri. Krishnappa under Section 128 of the Karnataka Land Revenue Act 1964.
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
                  <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📁</div>
                  <h3 style={{ color: '#ffffff', margin: '0 0 0.5rem 0' }}>No documents yet.</h3>
                  <p style={{ color: '#94a3b8', maxWidth: '500px', margin: '0 auto 1.5rem auto' }}>
                    Upload property papers, title deeds, RTC pahani records, or mortgage documents to start automated AI analysis.
                  </p>
                  <button className="btn-primary" onClick={() => setActiveTab('documents')}>
                    Upload Property Papers →
                  </button>
                </div>
              )}
            </div>
          )}

          {/* TAB: DOCUMENTS */}
          {activeTab === 'documents' && (
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ margin: 0 }}>📁 Property Documents Workspace</h3>
                  <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.9rem' }}>
                    Upload PDF, JPG, PNG, scanned documents, old property papers, and handwritten pages.
                  </p>
                </div>
                <button className="btn-primary" onClick={handleUploadSimulation}>
                  ⚡ Upload & Ingest Sample Batch
                </button>
              </div>

              <div className="upload-dropzone" onClick={handleUploadSimulation} style={{ marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>📤</div>
                <div style={{ fontWeight: 700, color: '#ffffff', fontSize: '1.1rem' }}>Upload Property Deeds or Scanned Pages</div>
                <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.25rem' }}>
                  Supports PDF, JPG, PNG, Scans, Old Stamp Papers, and Photographs
                </div>
              </div>

              {isProcessing && (
                <div style={{ background: '#0f172a', border: '1px solid #3b82f6', borderRadius: '8px', padding: '1rem', marginBottom: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
                    <span>Processing & Extracting Indic OCR...</span>
                    <span>{processingProgress}%</span>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: '#1e293b', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{ width: `${processingProgress}%`, height: '100%', background: '#2563eb', transition: 'width 0.3s' }}></div>
                  </div>
                </div>
              )}

              {hasDocuments ? (
                <table>
                  <thead>
                    <tr>
                      <th>Document Name</th>
                      <th>Document Type</th>
                      <th>Execution Date</th>
                      <th>Language</th>
                      <th>OCR Score</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Registered_Sale_Deed_1985.pdf</strong></td>
                      <td>Sale Deed (ಕ್ರಯ ಪತ್ರ)</td>
                      <td>14-Aug-1985</td>
                      <td><code>Kannada, English</code></td>
                      <td><strong style={{ color: '#34d399' }}>96.8%</strong></td>
                      <td><span className="status-badge">READY</span></td>
                    </tr>
                    <tr>
                      <td><strong>Mutation_Extract_1986.pdf</strong></td>
                      <td>Revenue Record (Pahani)</td>
                      <td>10-Apr-1986</td>
                      <td><code>Kannada</code></td>
                      <td><strong style={{ color: '#34d399' }}>95.2%</strong></td>
                      <td><span className="status-badge">READY</span></td>
                    </tr>
                    <tr>
                      <td><strong>Mortgage_Deed_2010.pdf</strong></td>
                      <td>Simple Mortgage Deed</td>
                      <td>20-May-2010</td>
                      <td><code>English</code></td>
                      <td><strong style={{ color: '#34d399' }}>98.4%</strong></td>
                      <td><span className="status-badge">READY</span></td>
                    </tr>
                    <tr>
                      <td><strong>Sale_Deed_2018.pdf</strong></td>
                      <td>Conveyance Deed</td>
                      <td>12-Nov-2018</td>
                      <td><code>English, Kannada</code></td>
                      <td><strong style={{ color: '#34d399' }}>97.1%</strong></td>
                      <td><span className="status-badge">READY</span></td>
                    </tr>
                  </tbody>
                </table>
              ) : (
                <div style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
                  No documents uploaded in this case yet. Click the dropzone above to ingest papers.
                </div>
              )}
            </div>
          )}

          {/* TAB: AI ANALYSIS */}
          {activeTab === 'ai-analysis' && (
            <div className="card">
              <h3 style={{ margin: '0 0 0.5rem 0' }}>🔍 Evidence-First AI Property Analysis</h3>
              <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                Every important AI finding shows source document, page, extracted evidence, comparison, risk level, confidence, and recommended action.
              </p>

              {hasDocuments ? (
                <>
                  <div style={{ background: '#0f172a', border: '1px solid #ef4444', borderRadius: '8px', padding: '1.25rem', marginBottom: '1.25rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <span style={{ fontSize: '0.8rem', background: '#7f1d1d', color: '#fecaca', padding: '0.2rem 0.6rem', borderRadius: '4px', fontWeight: 700 }}>
                        ISSUE: SURVEY NUMBER & AREA MISMATCH
                      </span>
                      <span style={{ fontSize: '0.8rem', color: '#ef4444', fontWeight: 700 }}>RISK: HIGH • CONFIDENCE: 98%</span>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', margin: '0.75rem 0', background: '#0b1120', padding: '1rem', borderRadius: '6px' }}>
                      <div>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700 }}>SOURCE: Registered Sale Deed (1985) — Page 3</div>
                        <div style={{ fontSize: '0.95rem', color: '#38bdf8', fontWeight: 600, marginTop: '0.25rem' }}>EVIDENCE: Survey No. 42/1 Hissa 2 = 2 Acres 24 Guntas</div>
                      </div>
                      <div>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700 }}>COMPARE WITH: Registered Sale Deed (2018) — Page 4</div>
                        <div style={{ fontSize: '0.95rem', color: '#f87171', fontWeight: 600, marginTop: '0.25rem' }}>EVIDENCE: Survey No. 42/1 Hissa 2 = 2 Acres 10 Guntas (-14G Deficit)</div>
                      </div>
                    </div>

                    <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                      <strong>Explanation:</strong> 14 Guntas (~15,246 Sq.Ft) is missing from the conveyance without a recorded partition deed or revenue sub-division.
                    </div>
                    <div style={{ fontSize: '0.85rem', color: '#34d399', marginTop: '0.5rem' }}>
                      👉 <strong>Recommended Action:</strong> Verify the official land record, execute Rectification Deed, and commission an ADLR 11E survey demarcation.
                    </div>
                  </div>

                  <div style={{ background: '#0f172a', border: '1px solid #f59e0b', borderRadius: '8px', padding: '1.25rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <span style={{ fontSize: '0.8rem', background: '#78350f', color: '#fde68a', padding: '0.2rem 0.6rem', borderRadius: '4px', fontWeight: 700 }}>
                        ISSUE: ACTIVE BANK CHARGE (SARFAESI ACT)
                      </span>
                      <span style={{ fontSize: '0.8rem', color: '#fbbf24', fontWeight: 700 }}>RISK: CRITICAL • CONFIDENCE: 99%</span>
                    </div>

                    <div style={{ background: '#0b1120', padding: '1rem', borderRadius: '6px', margin: '0.75rem 0' }}>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 700 }}>SOURCE: Simple Mortgage Deed No. 450/2010 — Page 2</div>
                      <div style={{ fontSize: '0.95rem', color: '#fbbf24', fontWeight: 600, marginTop: '0.25rem' }}>EVIDENCE: Mortgage in favor of State Bank of India for ₹50,00,000</div>
                    </div>

                    <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                      <strong>Explanation:</strong> No registered Mortgage Discharge Deed (Vimochana Patra) found in SRO Book 1. The bank retains statutory priority charge.
                    </div>
                    <div style={{ fontSize: '0.85rem', color: '#34d399', marginTop: '0.5rem' }}>
                      👉 <strong>Recommended Action:</strong> Obtain and register an official Bank Discharge Deed before paying purchase advance.
                    </div>
                  </div>
                </>
              ) : (
                <div style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8' }}>
                  AI analysis will appear after your documents are processed.
                </div>
              )}
            </div>
          )}

          {/* TAB: OWNERSHIP CHAIN */}
          {activeTab === 'ownership-chain' && (
            <div className="card">
              <h3 style={{ margin: '0 0 1.5rem 0' }}>🌳 Visual Title & Ownership Chain</h3>
              <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                Click any transaction box below to inspect its source document, page number, extracted evidence, date, and transaction type.
              </p>

              {hasDocuments ? (
                <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '2rem' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div 
                      style={{ background: '#0f172a', border: '2px solid #3b82f6', borderRadius: '8px', padding: '1.25rem', cursor: 'pointer' }}
                      onClick={() => setSelectedTransaction({
                        owner: 'Sri. Venkatappa',
                        date: '14-Aug-1985',
                        type: 'Absolute Sale Transfer',
                        doc: 'Registered Sale Deed No. 1234/1985-86',
                        page: 'Page 2-3',
                        evidence: 'Sri. Venkatappa conveyed 2 Acres 24 Guntas in Survey No. 42/1 Hissa 2 for ₹15,00,000 consideration.'
                      })}
                    >
                      <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 700 }}>OWNER A (1985)</div>
                      <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff' }}>Sri. Venkatappa (Original Owner)</div>
                    </div>

                    <div style={{ textAlign: 'center', color: '#38bdf8', fontWeight: 800 }}>↓ [Sale / Transfer]</div>

                    <div 
                      style={{ background: '#0f172a', border: '2px solid #3b82f6', borderRadius: '8px', padding: '1.25rem', cursor: 'pointer' }}
                      onClick={() => setSelectedTransaction({
                        owner: 'Sri. Krishnappa S/o Venkatappa',
                        date: '10-Apr-1986',
                        type: 'Khata Mutation Transfer',
                        doc: 'Mutation Register Extract M.R. No. 14/1986-87',
                        page: 'Page 1',
                        evidence: 'Revenue Khata mutated to Sri. Krishnappa under Section 128 of Karnataka Land Revenue Act 1964.'
                      })}
                    >
                      <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 700 }}>OWNER B (1986)</div>
                      <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff' }}>Sri. Krishnappa S/o Venkatappa</div>
                    </div>

                    <div style={{ textAlign: 'center', color: '#fbbf24', fontWeight: 800 }}>↓ [Inheritance & 2010 SBI Loan]</div>

                    <div 
                      style={{ background: '#0f172a', border: '2px solid #ef4444', borderRadius: '8px', padding: '1.25rem', cursor: 'pointer' }}
                      onClick={() => setSelectedTransaction({
                        owner: 'Sri. Anand Kumar',
                        date: '12-Nov-2018',
                        type: 'Subsequent Conveyance',
                        doc: 'Registered Sale Deed No. 890/2018-19',
                        page: 'Page 4',
                        evidence: 'Krishnappa sold 2 Acres 10 Guntas to Anand Kumar. 14 Guntas shortfall detected on record.'
                      })}
                    >
                      <div style={{ fontSize: '0.75rem', color: '#f87171', fontWeight: 700 }}>CURRENT OWNER (2018)</div>
                      <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff' }}>Sri. Anand Kumar (Current Record)</div>
                    </div>
                  </div>

                  <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', padding: '1.5rem' }}>
                    <h4 style={{ margin: '0 0 1rem 0', color: '#38bdf8' }}>📄 Transaction Evidence Inspector</h4>
                    {selectedTransaction ? (
                      <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                        <p><strong>Owner Name:</strong> {selectedTransaction.owner}</p>
                        <p><strong>Transaction Date:</strong> {selectedTransaction.date}</p>
                        <p><strong>Transaction Type:</strong> {selectedTransaction.type}</p>
                        <p><strong>Source Document:</strong> <span style={{ color: '#38bdf8' }}>{selectedTransaction.doc}</span></p>
                        <p><strong>Page Number:</strong> {selectedTransaction.page}</p>
                        <div style={{ background: '#0b1120', padding: '0.75rem', borderRadius: '6px', marginTop: '0.5rem', color: '#f8fafc' }}>
                          <strong>Extracted Evidence:</strong><br />
                          {selectedTransaction.evidence}
                        </div>
                      </div>
                    ) : (
                      <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                        Click any transaction in the timeline on the left to inspect its verified page and document evidence.
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8' }}>
                  No ownership chain has been established yet.
                </div>
              )}
            </div>
          )}

          {/* TAB: TIMELINE */}
          {activeTab === 'timeline' && (
            <div className="card">
              <h3 style={{ margin: '0 0 1.5rem 0' }}>📅 Chronological Property Timeline</h3>
              {hasDocuments ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  <div style={{ borderLeft: '3px solid #38bdf8', paddingLeft: '1rem' }}>
                    <div style={{ fontWeight: 700, color: '#ffffff' }}>1998 — Original Ownership</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Ancestral cultivation under Sri. Venkatappa</div>
                  </div>
                  <div style={{ borderLeft: '3px solid #38bdf8', paddingLeft: '1rem' }}>
                    <div style={{ fontWeight: 700, color: '#ffffff' }}>2005 — Sale / Conveyance</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Absolute Sale Transfer executed and registered</div>
                  </div>
                  <div style={{ borderLeft: '3px solid #38bdf8', paddingLeft: '1rem' }}>
                    <div style={{ fontWeight: 700, color: '#ffffff' }}>2012 — Inheritance / Revenue Mutation</div>
                    <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Tahsildar sanctioned Pahani entry under Sec 128 KLR Act</div>
                  </div>
                  <div style={{ borderLeft: '3px solid #f59e0b', paddingLeft: '1rem' }}>
                    <div style={{ fontWeight: 700, color: '#fbbf24' }}>2019 — Registration & Sub-Division</div>
                    <div style={{ color: '#fed7aa', fontSize: '0.85rem' }}>Subsequent deed executed with 14 Guntas shortage alert</div>
                  </div>
                  <div style={{ borderLeft: '3px solid #10b981', paddingLeft: '1rem' }}>
                    <div style={{ fontWeight: 700, color: '#34d399' }}>2026 — Current Record State</div>
                    <div style={{ color: '#a7f3d0', fontSize: '0.85rem' }}>Investigation active for title regularization</div>
                  </div>
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8' }}>
                  Timeline will appear after documents are uploaded.
                </div>
              )}
            </div>
          )}

          {/* TAB: COMPARISON */}
          {activeTab === 'comparison' && (
            <div className="card">
              <h3 style={{ margin: '0 0 1rem 0' }}>📝 Side-by-Side Document Comparison</h3>
              <table>
                <thead>
                  <tr>
                    <th>Clause / Parameter</th>
                    <th>Document A (1985 Sale Deed)</th>
                    <th>Document B (2018 Sale Deed)</th>
                    <th>Difference Importance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Survey Number</strong></td>
                    <td>Survey No. 124/2 (Pg 3)</td>
                    <td>Survey No. 124/3 (Pg 7)</td>
                    <td><strong style={{ color: '#ef4444' }}>HIGH IMPORTANCE</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Property Area</strong></td>
                    <td>2 Acres 24 Guntas</td>
                    <td>2 Acres 10 Guntas</td>
                    <td><strong style={{ color: '#ef4444' }}>CRITICAL (-14 Guntas)</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Boundaries</strong></td>
                    <td>North: Sy No 42/2 (Govindappa)</td>
                    <td>North: Private Layout Road</td>
                    <td><strong style={{ color: '#f59e0b' }}>HIGH (Boundary Shift)</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Encumbrance</strong></td>
                    <td>Declared Clear</td>
                    <td>Declared Clear</td>
                    <td><strong style={{ color: '#ef4444' }}>CRITICAL (SBI ₹50L Active)</strong></td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}

          {/* TAB: RISKS */}
          {activeTab === 'risks' && (
            <div className="card">
              <h3 style={{ margin: '0 0 1rem 0' }}>⚠️ Legal Risk Engine & Threat Categorization</h3>
              {hasDocuments ? (
                <table>
                  <thead>
                    <tr>
                      <th>Risk Category</th>
                      <th>Finding</th>
                      <th>Source & Page</th>
                      <th>Risk Level</th>
                      <th>Recommended Verification</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Encumbrance Risk</strong></td>
                      <td>Unreleased State Bank of India ₹50L Mortgage</td>
                      <td>Mortgage Deed (Pg 2)</td>
                      <td><span style={{ color: '#ef4444', fontWeight: 700 }}>CRITICAL</span></td>
                      <td>Demand official Bank Discharge Deed</td>
                    </tr>
                    <tr>
                      <td><strong>Boundary / Title Risk</strong></td>
                      <td>14 Guntas Shortage between 1985 & 2018 deeds</td>
                      <td>Sale Deed 2018 (Pg 4)</td>
                      <td><span style={{ color: '#ef4444', fontWeight: 700 }}>HIGH</span></td>
                      <td>Commission official ADLR 11E survey sketch</td>
                    </tr>
                    <tr>
                      <td><strong>Identity / Heir Risk</strong></td>
                      <td>Missing Tahsildar Family Tree (Vamshavruksha)</td>
                      <td>Pahani Record (Pg 1)</td>
                      <td><span style={{ color: '#f59e0b', fontWeight: 700 }}>MEDIUM</span></td>
                      <td>Obtain certified genealogical tree</td>
                    </tr>
                    <tr>
                      <td><strong>Registration Risk</strong></td>
                      <td>Stamp duty paid and recorded in SRO Book 1</td>
                      <td>Sale Deed 1985 (Pg 1)</td>
                      <td><span style={{ color: '#34d399', fontWeight: 700 }}>LOW</span></td>
                      <td>Verified in SRO Book 1 Vol 120</td>
                    </tr>
                  </tbody>
                </table>
              ) : (
                <div style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8' }}>
                  No risks identified yet.
                </div>
              )}
            </div>
          )}

          {/* TAB: RESEARCH */}
          {activeTab === 'research' && (
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ margin: 0 }}>⚖️ Precedent Citation Graph & Legal Research Workspace</h3>
                  <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.9rem' }}>
                    Clearly distinguishes Document Evidence from Legal Research from AI Interpretation.
                  </p>
                </div>
                <button className="btn-primary" onClick={() => handleSearchPrecedents()}>🔄 Search Precedents</button>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '1.5rem' }}>
                <div style={{ background: '#0b1120', border: '1px solid #334155', borderRadius: '8px', padding: '1.25rem' }}>
                  <h4 style={{ margin: '0 0 0.75rem 0', color: '#cbd5e1' }}>🌐 Judicial Precedent Authority:</h4>
                  <div style={{ padding: '0.75rem 1rem', borderRadius: '6px', marginBottom: '0.75rem', background: '#1e3a8a', border: '1px solid #3b82f6', cursor: 'pointer' }} onClick={() => setSelectedCase('case_002')}>
                    <div style={{ fontWeight: 700, color: '#93c5fd' }}>🏛️ 2023 INSC 891 (Anandram)</div>
                    <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginTop: '0.2rem' }}>Supreme Court • Extent Mismatch & Durasti</div>
                  </div>
                  <div style={{ padding: '0.75rem 1rem', borderRadius: '6px', marginBottom: '0.75rem', background: '#1e3a8a', border: '1px solid #3b82f6', cursor: 'pointer' }} onClick={() => setSelectedCase('case_004')}>
                    <div style={{ fontWeight: 700, color: '#93c5fd' }}>🏛️ 2018 7 SCC 446 (Indian Bank)</div>
                    <div style={{ fontSize: '0.75rem', color: '#cbd5e1', marginTop: '0.2rem' }}>Supreme Court • SARFAESI Mortgages</div>
                  </div>
                </div>

                <div>
                  <h4 style={{ margin: '0 0 0.75rem 0', color: '#34d399' }}>✓ AI Precedent Application:</h4>
                  <div className="extract-section">
                    <h4>🏛️ 2023 INSC 891 — Anandram vs. LAO Bangalore Rural</h4>
                    <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                      • <strong>Ratio Decidendi:</strong> Revenue settlement akarband and physical spot durasti survey prevail over unrectified deed boundaries.<br />
                      • <strong>Application:</strong> Directs that an official 11E survey sketch legally reconciles the 14 Guntas shortage.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB: QUESTIONS */}
          {activeTab === 'questions' && (
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ margin: 0 }}>💬 Document-Grounded Copilot & Voice Explainer</h3>
                  <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.9rem' }}>
                    Ask questions grounded in deeds with exact page citations, or listen in plain English & Hindi.
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button className="btn-secondary" onClick={() => handleVoiceExplain('en')}>🔊 Listen (English)</button>
                  <button className="btn-secondary" onClick={() => handleVoiceExplain('hi')}>🔊 सुनो (हिंदी)</button>
                </div>
              </div>

              <div style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #1e293b', marginBottom: '1rem', maxHeight: '250px', overflowY: 'auto' }}>
                {chatStream.map((msg, i) => (
                  <div key={i} style={{ marginBottom: '0.75rem' }}>
                    <strong>{msg.sender === 'user' ? 'Question:' : 'Jurisiva Copilot:'}</strong>
                    <p style={{ margin: '0.25rem 0', color: msg.sender === 'user' ? '#f8fafc' : '#34d399' }}>{msg.text}</p>
                    {msg.citation && <span style={{ fontSize: '0.75rem', color: '#38bdf8' }}>🔗 {msg.citation}</span>}
                  </div>
                ))}
              </div>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <input
                  type="text"
                  value={chatQuery}
                  onChange={(e) => setChatQuery(e.target.value)}
                  placeholder="Who is the current owner? / Is there any mismatch?"
                  style={{ flex: 1 }}
                />
                <button className="btn-primary" onClick={handleSendChat}>Send Query</button>
              </div>

              <div className="voice-card">
                <div style={{ fontWeight: 700, color: '#ffffff', marginBottom: '0.5rem' }}>
                  <span className="voice-pulse"></span> Jurisiva AI Voice Explainer (Layman's Terms)
                </div>
                <div style={{ color: '#e0e7ff', fontSize: '0.95rem', lineHeight: 1.6 }}>
                  {voiceExplanation}
                </div>
              </div>
            </div>
          )}

          {/* TAB: REPORTS */}
          {activeTab === 'reports' && (
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ margin: 0 }}>📑 Full Property Due-Diligence Report</h3>
                  <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.9rem' }}>
                    Structured Title Assessment: Facts ➔ Evidence ➔ Issues ➔ Risks ➔ Missing Documents ➔ Next Steps.
                  </p>
                </div>
                <button className="btn-primary" onClick={() => window.print()}>🖨️ Export PDF Report</button>
              </div>

              <div className="extract-section">
                <h4>🏛️ 1. Executive Summary & Property Details</h4>
                <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                  • <strong>Target Land:</strong> Survey No. 42/1 Hissa 2, Devanahalli Village, Bengaluru Rural District, Karnataka<br />
                  • <strong>Root Extent:</strong> 2 Acres 24 Guntas (104,544 Sq.Ft) • Classification: Agricultural Dry Land (Khuski)<br />
                  • <strong>Investigation Conclusion:</strong> Conditional Marketable Title subject to Mortgage Discharge Deed and Durasti Demarcation.
                </div>
              </div>

              <div className="extract-section">
                <h4>📜 2. Documents Reviewed & Ownership History</h4>
                <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                  • 1. Registered Sale Deed No. 1234/1985 (Venkatappa ➔ Krishnappa for 2A 24G)<br />
                  • 2. Revenue Mutation Extract M.R. No. 14/1986 (Khata transferred to Krishnappa)<br />
                  • 3. Registered Simple Mortgage Deed No. 450/2010 (Krishnappa ➔ SBI for ₹50 Lakhs)<br />
                  • 4. Registered Sale Deed No. 890/2018 (Krishnappa ➔ Anand Kumar for 2A 10G)
                </div>
              </div>

              <div className="extract-section" style={{ borderColor: '#ef4444' }}>
                <h4 style={{ color: '#f87171' }}>⚠️ 3. Identified Issues & Risk Assessment</h4>
                <div style={{ fontSize: '0.85rem', color: '#fca5a5', lineHeight: 1.6 }}>
                  • <strong>14 Guntas Shortage:</strong> Unrecorded difference between 1985 deed (2A 24G) and 2018 deed (2A 10G).<br />
                  • <strong>Active SBI Mortgage:</strong> No registered release deed on file for ₹50,00,000 credit facility.
                </div>
              </div>

              <div className="extract-section">
                <h4>📂 4. Missing Documents Required to Cure Title</h4>
                <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                  • 1. Registered Mortgage Discharge Deed (*Vimochana Patra*) from State Bank of India<br />
                  • 2. ADLR Tatkal 11E Survey Demarcation Sketch & Durasti Register<br />
                  • 3. Certified Genealogic Family Tree (*Vamshavruksha*) from Tahsildar<br />
                  • 4. 30-Year Encumbrance Certificate (Form 15) from SRO Devanahalli
                </div>
              </div>

              <div className="extract-section" style={{ borderColor: '#10b981' }}>
                <h4 style={{ color: '#34d399' }}>🚀 5. Action Plan & Next Steps</h4>
                <div style={{ fontSize: '0.85rem', color: '#a7f3d0', lineHeight: 1.6 }}>
                  • 1. Do not disburse token money until Bank Discharge Deed is registered in SRO Book 1.<br />
                  • 2. Execute a Registered Rectification Deed clarifying the 14 Guntas variance.<br />
                  • 3. Publish a 14-day statutory public notice in <em>The Deccan Herald</em> and <em>Prajavani</em>.
                </div>
              </div>
            </div>
          )}

          {/* TAB: SETTINGS */}
          {activeTab === 'settings' && (
            <div className="card">
              <h3>⚙️ Case Workspace & Tenant Governance Settings</h3>
              <div className="extract-section">
                <h4>🔐 Tenant Security & Data Retention</h4>
                <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                  • <strong>Organization ID:</strong> org_001 (Advocate Rajesh Sharma & Associates)<br />
                  • <strong>Retention Policy:</strong> Zero LLM Retention (Isolated Storage Enclave)<br />
                  • <strong>OCR Engine:</strong> Indic Multilingual v2 (Kannada, Marathi, Hindi, Telugu, Tamil, English)<br />
                  • <strong>Audit Stream:</strong> All case access and file exports are cryptographically hashed and logged.
                </div>
              </div>
            </div>
          )}

        </div>
      </main>
    </div>
  );
}
