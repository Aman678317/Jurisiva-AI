import React, { useEffect, useRef, useState } from 'react';

interface Hero3DSceneProps {
  onStartCase: () => void;
}

export default function Hero3DScene({ onStartCase }: Hero3DSceneProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [activeDocTab, setActiveDocTab] = useState<'deed' | 'map' | 'ai'>('deed');

  // High-performance canvas animation loop for 3D AI particles and legal courtroom ambiance
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || 800);
    let height = (canvas.height = 440);

    const handleResize = () => {
      if (canvas && canvas.parentElement) {
        width = canvas.width = canvas.parentElement.clientWidth;
        height = canvas.height = 440;
      }
    };
    window.addEventListener('resize', handleResize);

    // AI Analysis Particle Swarm
    const particleCount = 45;
    const particles: Array<{
      x: number;
      y: number;
      z: number;
      vx: number;
      vy: number;
      radius: number;
      color: string;
      alpha: number;
    }> = [];

    const colors = ['#38bdf8', '#fbbf24', '#34d399', '#60a5fa', '#e2e8f0'];

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        z: Math.random() * 200 + 50,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        radius: Math.random() * 2.5 + 1,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: Math.random() * 0.7 + 0.3,
      });
    }

    let time = 0;

    const render = () => {
      time += 0.015;
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Courtroom Ambient Perspective Grid (Floor Depth)
      ctx.save();
      const horizonY = height * 0.65;
      const fov = 350;

      // Subtle volumetric light cone from top-right
      const lightGrad = ctx.createRadialGradient(width * 0.7, 0, 10, width * 0.7, height, 400);
      lightGrad.addColorStop(0, 'rgba(56, 189, 248, 0.08)');
      lightGrad.addColorStop(0.5, 'rgba(217, 119, 6, 0.03)');
      lightGrad.addColorStop(1, 'rgba(11, 17, 32, 0)');
      ctx.fillStyle = lightGrad;
      ctx.fillRect(0, 0, width, height);

      // Floor grid lines with depth
      ctx.strokeStyle = 'rgba(51, 65, 85, 0.25)';
      ctx.lineWidth = 1;
      const gridCount = 12;
      const targetX = width * 0.5 + mousePos.x * 30;

      for (let i = -gridCount; i <= gridCount; i++) {
        const startX = targetX + i * 45;
        ctx.beginPath();
        ctx.moveTo(targetX, horizonY);
        ctx.lineTo(startX + (startX - targetX) * 2.5, height);
        ctx.stroke();
      }

      // Horizontal depth lines
      for (let y = horizonY + 10; y < height; y += (y - horizonY) * 0.4 + 5) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }
      ctx.restore();

      // 2. Draw Floating AI Knowledge Particles with 3D Depth
      particles.forEach((p) => {
        p.x += p.vx + Math.sin(time + p.z) * 0.2;
        p.y += p.vy + Math.cos(time + p.z) * 0.2;

        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        // Perspective scale
        const scale = fov / (fov + p.z);
        const drawX = (p.x - width / 2) * scale + width / 2 + mousePos.x * (200 - p.z) * 0.05;
        const drawY = (p.y - height / 2) * scale + height / 2 + mousePos.y * (200 - p.z) * 0.05;
        const radius = p.radius * scale;

        ctx.save();
        ctx.beginPath();
        ctx.arc(drawX, drawY, Math.max(0.5, radius), 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha * Math.min(1, scale * 1.5);
        ctx.shadowBlur = 8;
        ctx.shadowColor = p.color;
        ctx.fill();
        ctx.restore();

        // Connect nearest particles with subtle knowledge strands
        particles.slice(0, 15).forEach((p2) => {
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 75) {
            ctx.beginPath();
            ctx.moveTo(drawX, drawY);
            const scale2 = fov / (fov + p2.z);
            const drawX2 = (p2.x - width / 2) * scale2 + width / 2 + mousePos.x * (200 - p2.z) * 0.05;
            const drawY2 = (p2.y - height / 2) * scale2 + height / 2 + mousePos.y * (200 - p2.z) * 0.05;
            ctx.lineTo(drawX2, drawY2);
            ctx.strokeStyle = p.color;
            ctx.globalAlpha = (1 - dist / 75) * 0.15;
            ctx.stroke();
          }
        });
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
    };
  }, [mousePos]);

  // Mouse move handler for 3D parallax
  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    setMousePos({ x, y });
  };

  const handleMouseLeave = () => {
    setMousePos({ x: 0, y: 0 });
  };

  // Parallax transform styles
  const lawyerParallax = {
    transform: `perspective(1000px) rotateY(${mousePos.x * 8}deg) rotateX(${-mousePos.y * 6}deg) translateZ(40px)`,
    transition: 'transform 0.1s ease-out',
  };

  const documentParallax = {
    transform: `perspective(1000px) rotateY(${mousePos.x * 12 - 6}deg) rotateX(${-mousePos.y * 8 + 4}deg) translateZ(60px)`,
    transition: 'transform 0.1s ease-out',
  };

  return (
    <div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        position: 'relative',
        width: '100%',
        height: '440px',
        background: 'linear-gradient(180deg, #0b1120 0%, #0f172a 50%, #0b1120 100%)',
        borderRadius: '16px',
        border: '1px solid #1e293b',
        boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.7)',
        overflow: 'hidden',
        userSelect: 'none',
      }}
    >
      {/* Background Interactive WebGL/Canvas Layer */}
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: 1,
          pointerEvents: 'none',
        }}
      />

      {/* Top 3D Control Strip */}
      <div
        style={{
          position: 'absolute',
          top: '1rem',
          left: '1.5rem',
          right: '1.5rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          zIndex: 10,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#38bdf8', boxShadow: '0 0 10px #38bdf8' }}></div>
          <span style={{ fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.08em', color: '#94a3b8', textTransform: 'uppercase' }}>
            Interactive 3D Spatial Courtroom Scene
          </span>
        </div>

        <div style={{ display: 'flex', gap: '0.4rem', background: '#0b1120', padding: '0.2rem', borderRadius: '6px', border: '1px solid #1e293b' }}>
          <button
            onClick={() => setActiveDocTab('deed')}
            style={{
              background: activeDocTab === 'deed' ? '#2563eb' : 'transparent',
              color: activeDocTab === 'deed' ? '#ffffff' : '#94a3b8',
              border: 'none',
              borderRadius: '4px',
              padding: '0.25rem 0.6rem',
              fontSize: '0.75rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            📄 3D Deed
          </button>
          <button
            onClick={() => setActiveDocTab('map')}
            style={{
              background: activeDocTab === 'map' ? '#2563eb' : 'transparent',
              color: activeDocTab === 'map' ? '#ffffff' : '#94a3b8',
              border: 'none',
              borderRadius: '4px',
              padding: '0.25rem 0.6rem',
              fontSize: '0.75rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            🗺️ 3D Parcel
          </button>
          <button
            onClick={() => setActiveDocTab('ai')}
            style={{
              background: activeDocTab === 'ai' ? '#2563eb' : 'transparent',
              color: activeDocTab === 'ai' ? '#ffffff' : '#94a3b8',
              border: 'none',
              borderRadius: '4px',
              padding: '0.25rem 0.6rem',
              fontSize: '0.75rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            ✨ AI Assistant
          </button>
        </div>
      </div>

      {/* Center 3D Workspace Scene */}
      <div
        style={{
          position: 'absolute',
          top: '3.5rem',
          left: '1.5rem',
          right: '1.5rem',
          bottom: '1rem',
          display: 'grid',
          gridTemplateColumns: '1.1fr 1.2fr',
          gap: '1.5rem',
          zIndex: 5,
          alignItems: 'center',
        }}
      >
          {/* Left 3D Entity: Stylized Original Lawyer Avatar & Courtroom Dais */}
          <div
            style={{
              ...lawyerParallax,
              background: 'radial-gradient(circle at 50% 40%, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%)',
              border: '1px solid #334155',
              borderRadius: '12px',
              padding: '1.5rem',
              height: '330px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              backdropFilter: 'blur(8px)',
              boxShadow: '0 20px 35px -10px rgba(0, 0, 0, 0.5)',
              position: 'relative',
            }}
          >
            {/* 3D Lawyer Silhouette / Avatar Graphic */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div
                style={{
                  width: '64px',
                  height: '64px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
                  border: '2px solid #38bdf8',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 0 20px rgba(56, 189, 248, 0.3)',
                  position: 'relative',
                }}
              >
                <span style={{ fontSize: '2rem' }}>⚖️</span>
                <div
                  style={{
                    position: 'absolute',
                    bottom: '-2px',
                    right: '-2px',
                    width: '14px',
                    height: '14px',
                    borderRadius: '50%',
                    background: '#10b981',
                    border: '2px solid #0f172a',
                  }}
                ></div>
              </div>

              <div>
                <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  AI Legal Counsel OS
                </div>
                <h3 style={{ margin: '0.15rem 0 0 0', fontSize: '1.15rem', color: '#ffffff', fontWeight: 800 }}>
                  Advocate Rajesh Sharma
                </h3>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>High Court of Karnataka • Lead Diligence Officer</div>
              </div>
            </div>

            {/* Real-time Dynamic AI Commentary */}
            <div style={{ background: '#0b1120', border: '1px solid #1e3a8a', borderRadius: '8px', padding: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.3rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#fbbf24', fontWeight: 700 }}>⚡ ACTIVE CASE HYPOTHESIS:</span>
              </div>
              <div style={{ fontSize: '0.8rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                "Survey No. 42/1 Hissa 2 has a 14 Guntas deficit between the 1985 and 2018 conveyances. SARFAESI simple mortgage of ₹50 Lakhs remains unreleased on SRO Book 1."
              </div>
            </div>

            {/* Quick Action */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Matter ID: mat_001 • org_001</span>
              <button
                onClick={onStartCase}
                style={{
                  background: '#2563eb',
                  color: '#ffffff',
                  border: 'none',
                  padding: '0.45rem 0.9rem',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  boxShadow: '0 4px 12px rgba(37, 99, 235, 0.4)',
                }}
              >
                Open Workspace →
              </button>
            </div>
          </div>

          {/* Right 3D Entity: Floating Document, 3D Map, or AI Extraction Box */}
          <div style={{ height: '330px', position: 'relative' }}>
            {/* TAB 1: 3D DEED VISUALIZATION */}
            {activeDocTab === 'deed' && (
              <div
                style={{
                  ...documentParallax,
                  background: '#fffbeb',
                  color: '#1e293b',
                  border: '2px solid #b45309',
                  borderRadius: '10px',
                  padding: '1.25rem',
                  fontFamily: 'Georgia, serif',
                  height: '100%',
                  boxSizing: 'border-box',
                  boxShadow: '0 25px 40px -15px rgba(0, 0, 0, 0.6), 0 0 25px rgba(217, 119, 6, 0.15)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                }}
              >
                <div>
                  <div style={{ textAlign: 'center', fontWeight: 800, borderBottom: '2px solid #b45309', paddingBottom: '0.4rem', color: '#78350f', fontSize: '0.85rem', letterSpacing: '0.05em' }}>
                    GOVERNMENT OF KARNATAKA • DEED OF ABSOLUTE SALE (ಕ್ರಯ ಪತ್ರ)
                  </div>
                  <div style={{ fontSize: '0.75rem', lineHeight: 1.6, marginTop: '0.6rem' }}>
                    <p style={{ margin: '0.2rem 0' }}>
                      <strong>REG NO:</strong> <span style={{ background: 'rgba(254, 240, 138, 0.8)', padding: '0.1rem 0.3rem', border: '1px dashed #ca8a04', borderRadius: '3px' }}>1234/1985-86</span> | <strong>BOOK 1, VOL:</strong> 120
                    </p>
                    <p style={{ margin: '0.2rem 0' }}>
                      <strong>SCHEDULE PROPERTY:</strong> Dry land in <span style={{ background: 'rgba(254, 240, 138, 0.8)', padding: '0.1rem 0.3rem', border: '1px dashed #ca8a04', borderRadius: '3px' }}>Survey No. 42/1 Hissa 2</span>, Devanahalli Taluk.
                    </p>
                    <p style={{ margin: '0.2rem 0' }}>
                      <strong>TOTAL EXTENT:</strong> <span style={{ background: 'rgba(254, 240, 138, 0.8)', padding: '0.1rem 0.3rem', border: '1px dashed #ca8a04', borderRadius: '3px' }}>2 Acres 24 Guntas</span> (104,544 Sq.Ft)
                    </p>
                    <p style={{ margin: '0.2rem 0' }}>
                      <strong>PARTIES:</strong> Venkatappa (Vendor) ➔ Krishnappa (Purchaser)
                    </p>
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #e2e8f0', paddingTop: '0.5rem' }}>
                  <div style={{ border: '2px double #b91c1c', borderRadius: '50%', padding: '0.35rem 0.6rem', fontSize: '0.65rem', fontWeight: 'bold', color: '#b91c1c', textTransform: 'uppercase' }}>
                    SEAL • SRO DEVANAHALLI
                  </div>
                  <span style={{ fontSize: '0.7rem', color: '#059669', fontWeight: 'bold' }}>✓ 300 DPI Indic OCR Verified</span>
                </div>
              </div>
            )}

            {/* TAB 2: 3D PARCEL MAP VISUALIZATION */}
            {activeDocTab === 'map' && (
              <div
                style={{
                  ...documentParallax,
                  background: '#0f172a',
                  border: '1px solid #3b82f6',
                  borderRadius: '10px',
                  padding: '1.25rem',
                  height: '100%',
                  boxSizing: 'border-box',
                  boxShadow: '0 25px 40px -15px rgba(0, 0, 0, 0.6)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '0.8rem', color: '#38bdf8', fontWeight: 700 }}>🗺️ 3D SPATIAL CADASTRE (ILLUSTRATIVE)</span>
                    <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Kasaba Hobli, Sy 42/1</span>
                  </div>

                  <div style={{ position: 'relative', height: '170px', background: '#0b1120', borderRadius: '8px', border: '1px solid #1e293b', overflow: 'hidden', padding: '0.5rem' }}>
                    <div style={{ position: 'absolute', top: '8px', right: '12px', fontSize: '0.75rem', color: '#38bdf8', fontWeight: 800 }}>▲ N</div>
                    <div
                      style={{
                        position: 'absolute',
                        top: '25px',
                        left: '35px',
                        width: '160px',
                        height: '100px',
                        background: 'rgba(37, 99, 235, 0.25)',
                        border: '2px solid #38bdf8',
                        borderRadius: '4px',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.75rem',
                        color: '#ffffff',
                        fontWeight: 700,
                      }}
                    >
                      <span>Sy No. 42/1 Hissa 2</span>
                      <span style={{ color: '#34d399', fontSize: '0.7rem' }}>2 Acres 24 Guntas</span>
                    </div>

                    <div
                      style={{
                        position: 'absolute',
                        top: '25px',
                        left: '145px',
                        width: '50px',
                        height: '100px',
                        background: 'rgba(239, 68, 68, 0.3)',
                        border: '2px dashed #ef4444',
                        borderRadius: '0 4px 4px 0',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.65rem',
                        color: '#fca5a5',
                        fontWeight: 700,
                        textAlign: 'center',
                      }}
                    >
                      -14G<br />Deficit
                    </div>
                  </div>
                </div>

                <div style={{ fontSize: '0.7rem', color: '#94a3b8', fontStyle: 'italic' }}>
                  *Illustrative 3D Spatial Model reconstructed from deed schedule boundaries. Not an official survey.
                </div>
              </div>
            )}

            {/* TAB 3: AI ASSISTANT EVIDENCE PANEL */}
            {activeDocTab === 'ai' && (
              <div
                style={{
                  ...documentParallax,
                  background: '#0f172a',
                  border: '1px solid #10b981',
                  borderRadius: '10px',
                  padding: '1.25rem',
                  height: '100%',
                  boxSizing: 'border-box',
                  boxShadow: '0 25px 40px -15px rgba(0, 0, 0, 0.6)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                }}
              >
                <div>
                  <div style={{ fontSize: '0.8rem', color: '#34d399', fontWeight: 700, marginBottom: '0.5rem' }}>✨ 3D EVIDENCE-FIRST EXTRACTION</div>
                  <div style={{ background: '#0b1120', padding: '0.85rem', borderRadius: '6px', fontSize: '0.8rem', color: '#cbd5e1', lineHeight: 1.6 }}>
                    • <strong>Root Title:</strong> 1985 Venkatappa ➔ Krishnappa (2A 24G)<br />
                    • <strong>Mutation:</strong> M.R. No. 14/1986 sanctioned under Sec 128 KLR Act<br />
                    • <strong>Mortgage Charge:</strong> SBI ₹50,00,000 in 2010 (Unreleased)<br />
                    • <strong>Current Status:</strong> Sub-division mismatch requires ADLR 11E survey
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #1e293b', paddingTop: '0.5rem' }}>
                  <span style={{ fontSize: '0.75rem', color: '#38bdf8' }}>Confidence: 96.8%</span>
                  <button
                    onClick={onStartCase}
                    style={{
                      background: '#10b981',
                      color: '#0f172a',
                      border: 'none',
                      padding: '0.35rem 0.75rem',
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                    }}
                  >
                    Inspect in Workspace →
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
    </div>
  );
}
