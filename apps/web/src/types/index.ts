// Typed Domain Data Contracts & Entities

export type UserRole = "ADMIN" | "LEAD_ADVOCATE" | "ASSOCIATE" | "AUDITOR";

export interface User {
  id: string;
  email: string;
  fullName: string;
  barCouncilId?: string;
  organizationId: string;
  role: UserRole;
}

export interface Organization {
  id: string;
  name: string;
  jurisdiction: string;
  createdAt: string;
}

export interface Matter {
  id: string;
  organizationId: string;
  title: string;
  clientName: string;
  surveyNumber?: string;
  district?: string;
  state?: string;
  documentCount: number;
  status: "ACTIVE" | "ARCHIVED" | "COMPLETED";
  createdBy: string;
  createdAt: string;
}

export interface DocumentEntity {
  id: string;
  organizationId: string;
  matterId: string;
  filename: string;
  fileHash: string;
  fileSizeBytes: number;
  mimeType: string;
  ocrStatus: "QUEUED" | "PROCESSING" | "PROCESSED" | "FAILED";
  pageCount: number;
  uploadedBy: string;
  createdAt: string;
}

export interface Citation {
  id: string;
  documentId: string;
  documentName: string;
  pageNumber: number;
  excerpt: string;
  boundingBox?: { xmin: number; ymin: number; xmax: number; ymax: number };
}

export type VerificationStatus = "SOURCE_FACT" | "AI_EXTRACTION" | "AI_INFERENCE" | "HUMAN_VERIFIED" | "REJECTED";

export interface ExtractedFinding {
  id: string;
  matterId: string;
  documentId?: string;
  entityType: "SURVEY_NO" | "EXTENT" | "EXECUTANT" | "CLAIMANT" | "BOUNDARY" | "MORTGAGE";
  extractedValue: string;
  verifiedValue?: string;
  verificationStatus: VerificationStatus;
  sourcePage?: number;
  citationIds: string[];
  verifiedBy?: string;
}

export interface TimelineEvent {
  id: string;
  matterId: string;
  eventDate: string;
  documentId: string;
  documentName: string;
  deedType: string;
  executant: string;
  claimant: string;
  extentDescription: string;
  considerationAmount?: number;
  isLinkGapWarning: boolean;
  citationId: string;
}

export interface Contradiction {
  id: string;
  matterId: string;
  title: string;
  description: string;
  severity: "CRITICAL" | "WARNING" | "INFO";
  sourceA: { documentName: string; page: number; text: string };
  sourceB: { documentName: string; page: number; text: string };
  status: "OPEN" | "RESOLVED_DEFECT" | "RESOLVED_CLERICAL";
}

export interface AuditEvent {
  id: string;
  organizationId: string;
  matterId?: string;
  userId: string;
  userName: string;
  action: string;
  resourceType: string;
  resourceId?: string;
  ipAddress: string;
  timestamp: string;
}
