// Professional Legal Workspace Components — Split Viewer, Citation Popover, Property Timeline, & HITL Review

import React, { useState } from "react";
import { tokens } from "../../tokens";
import { Badge, Button, Card } from "../ui/primitives";
import { ExtractedFinding, TimelineEvent, Contradiction, Citation } from "../../types";

// 1. App Shell Component
export interface AppShellProps {
  currentMatterTitle?: string;
  activeTab: string;
  onTabChange: (tab: string) => void;
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ currentMatterTitle, activeTab, onTabChange, children }) => {
  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "documents", label: "Documents" },
    { id: "property", label: "Property Intelligence" },
    { id: "copilot", label: "Copilot & Q&A" },
    { id: "research", label: "Research" },
    { id: "reports", label: "Reports" },
    { id: "audit", label: "Audit Log" },
  ];

  return (
    <div style={{ minHeight: "100vh", backgroundColor: tokens.colors.surfaces.default, display: "flex", flexDirection: "column" }}>
      {/* Top Header */}
      <header
        style={{
          height: "56px",
          backgroundColor: tokens.colors.surfaces.dark,
          color: tokens.colors.text.inverse,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 24px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <span style={{ fontWeight: tokens.typography.weights.bold, fontSize: "16px", letterSpacing: "0.02em" }}>
            ⚖️ JURISIVA AI — India Legal Platform
          </span>
          <span style={{ color: "#64748B" }}>|</span>
          <span style={{ fontSize: "14px", color: "#CBD5E1", backgroundColor: "#1E293B", padding: "4px 10px", borderRadius: "4px" }}>
            📁 {currentMatterTitle || "Select Matter"}
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <button style={{ backgroundColor: "#1E293B", color: "#CBD5E1", border: "1px solid #334155", padding: "6px 12px", borderRadius: "4px", fontSize: "12px" }}>
            🔍 Cmd+K Global Search
          </button>
          <span style={{ fontSize: "13px", color: "#94A3B8" }}>Adv. Rajesh Sharma (Lead Advocate)</span>
        </div>
      </header>

      {/* Sub-Header Navigation Tabs */}
      <div style={{ backgroundColor: tokens.colors.surfaces.raised, borderBottom: `1px solid ${tokens.colors.border.default}`, padding: "0 24px" }}>
        <nav style={{ display: "flex", gap: "24px" }}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              style={{
                padding: "12px 0",
                background: "none",
                border: "none",
                borderBottom: activeTab === tab.id ? `2px solid ${tokens.colors.brand.accent}` : "2px solid transparent",
                color: activeTab === tab.id ? tokens.colors.brand.accent : tokens.colors.text.secondary,
                fontWeight: activeTab === tab.id ? tokens.typography.weights.semibold : tokens.typography.weights.medium,
                fontSize: "14px",
                cursor: "pointer",
              }}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: "24px", maxWidth: "1600px", margin: "0 auto", width: "100%", boxSizing: "border-box" }}>{children}</main>
    </div>
  );
};

// 2. Split-Screen Document Viewer Shell
export interface SplitDocumentViewerProps {
  documentName: string;
  currentPage: number;
  highlightText?: string;
  onPageChange: (p: number) => void;
}

export const SplitDocumentViewer: React.FC<SplitDocumentViewerProps> = ({ documentName, currentPage, highlightText, onPageChange }) => {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", height: "650px" }}>
      {/* Left PDF Canvas */}
      <Card style={{ display: "flex", flexDirection: "column", padding: "16px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "12px", borderBottom: `1px solid ${tokens.colors.border.default}`, paddingBottom: "8px" }}>
          <span style={{ fontWeight: tokens.typography.weights.semibold, fontSize: "14px" }}>📄 Scanned PDF: {documentName}</span>
          <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
            <Button variant="outline" size="sm" onClick={() => onPageChange(Math.max(1, currentPage - 1))}>◀ Prev Page</Button>
            <span style={{ fontSize: "13px" }}>Page {currentPage} of 12</span>
            <Button variant="outline" size="sm" onClick={() => onPageChange(currentPage + 1)}>Next Page ▶</Button>
          </div>
        </div>
        
        {/* PDF Simulated Page Canvas with Yellow Bounding Box Highlight */}
        <div style={{ flex: 1, backgroundColor: "#E2E8F0", borderRadius: "4px", padding: "24px", position: "relative", overflowY: "auto" }}>
          <div style={{ backgroundColor: "#FFFFFF", padding: "32px", minHeight: "500px", boxShadow: tokens.shadows.md, fontFamily: tokens.typography.fontSans }}>
            <p style={{ fontSize: "12px", color: "#64748B", textAlign: "right" }}>REGISTERED NO: 1234/1985</p>
            <h4 style={{ textAlign: "center", textTransform: "uppercase", marginBottom: "20px" }}>ABSOLUTE SALE DEED</h4>
            <p style={{ fontSize: "13px", lineHeight: 1.6 }}>
              THIS DEED OF SALE executed on 14th day of August 1985 between <strong>SRI. VENKATAPPA S/O RAMAIAH</strong> (hereinafter called SELLER) and <strong>SRI. KRISHNAPPA S/O GOVINDAPPA</strong> (hereinafter called BUYER).
            </p>
            
            {/* Live Bounding Box Highlight Target */}
            <div
              style={{
                backgroundColor: tokens.colors.highlights.citationFill,
                border: `2px solid ${tokens.colors.highlights.citationBorder}`,
                padding: "8px",
                borderRadius: "4px",
                margin: "16px 0",
              }}
            >
              <p style={{ fontSize: "13px", fontWeight: tokens.typography.weights.medium, margin: 0 }}>
                SCHEDULE PROPERTY: All that piece and parcel of Agricultural Land in <strong>Survey No. 42/1 Hissa 2</strong>, measuring an Extent of <strong>2 Acres 24 Guntas</strong> (104,544 Sq.Ft) situated at Devanahalli Village.
              </p>
            </div>
            
            <p style={{ fontSize: "13px", lineHeight: 1.6 }}>
              BOUNDARIES: North by Govt Road, South by Property of Ramappa, East by Survey No 42/2, West by Drainage Canal.
            </p>
          </div>
        </div>
      </Card>

      {/* Right OCR & Citation Extracted Layer */}
      <Card style={{ display: "flex", flexDirection: "column", padding: "16px" }}>
        <div style={{ marginBottom: "12px", borderBottom: `1px solid ${tokens.colors.border.default}`, paddingBottom: "8px" }}>
          <span style={{ fontWeight: tokens.typography.weights.semibold, fontSize: "14px" }}>🔍 Extracted OCR Text Layer & Metadata</span>
        </div>
        <div style={{ flex: 1, backgroundColor: "#F8FAFC", padding: "16px", borderRadius: "4px", fontFamily: tokens.typography.fontMono, fontSize: "12px", lineHeight: 1.5, overflowY: "auto" }}>
          <p style={{ color: "#2563EB", margin: "0 0 8px 0" }}>[OCR CONFIDENCE: 96.4% | ENGINE: Tesseract Indic (eng+kan)]</p>
          <p>SCHEDULE PROPERTY: All that piece and parcel of Agricultural Land in Survey No. 42/1 Hissa 2, measuring an Extent of 2 Acres 24 Guntas (104,544 Sq.Ft)...</p>
          <hr style={{ borderTop: `1px solid ${tokens.colors.border.default}`, margin: "16px 0" }} />
          <p style={{ color: "#475569" }}>SHA-256 HASH: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</p>
          <p style={{ color: "#475569" }}>STORAGE KEY: tenants/org_001/matters/mat_001/doc_001/originals/SaleDeed1985.pdf</p>
        </div>
      </Card>
    </div>
  );
};

// 3. Property Title Timeline Component
export const PropertyTimelineView: React.FC<{ events: TimelineEvent[] }> = ({ events }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
    <h3 style={{ fontSize: "16px", fontWeight: tokens.typography.weights.semibold, margin: 0 }}>
      📅 Chronological Ownership Chain (30-Year Flow)
    </h3>
    {events.map((evt) => (
      <Card key={evt.id} style={{ borderLeft: evt.isLinkGapWarning ? "4px solid #DC2626" : "4px solid #16A34A" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <span style={{ fontSize: "12px", color: tokens.colors.text.muted, fontWeight: tokens.typography.weights.medium }}>{evt.eventDate}</span>
            <h4 style={{ margin: "4px 0", fontSize: "15px" }}>{evt.deedType} — {evt.documentName}</h4>
            <p style={{ fontSize: "13px", color: tokens.colors.text.secondary, margin: "4px 0" }}>
              Executant: <strong>{evt.executant}</strong> ➔ Claimant: <strong>{evt.claimant}</strong>
            </p>
            <p style={{ fontSize: "12px", color: tokens.colors.text.muted, margin: 0 }}>Extent: {evt.extentDescription}</p>
          </div>
          <div>
            {evt.isLinkGapWarning ? (
              <Badge variant="CRITICAL">⚠️ LINK GAP WARNING</Badge>
            ) : (
              <Badge variant="HUMAN_VERIFIED">✓ UNBROKEN LINK</Badge>
            )}
          </div>
        </div>
      </Card>
    ))}
  </div>
);
