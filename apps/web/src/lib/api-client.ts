// Typed REST API Client Adapter — Matching Chapter 4 Contracts

import { User, Organization, Matter, DocumentEntity, ExtractedFinding, TimelineEvent, Contradiction, AuditEvent } from "../types";

export interface ApiResponse<T> {
  data?: T;
  error?: {
    code: string;
    message: string;
    requestId: string;
    retryable: boolean;
  };
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = "/api/v1") {
    this.baseUrl = baseUrl;
  }

  // Auth Methods
  async login(email: string, password: string): Promise<ApiResponse<{ user: User; token: string }>> {
    if (email === "advocate@legal.in" && password === "Password123!") {
      return {
        data: {
          token: "jwt_mock_token_12345",
          user: {
            id: "usr_001",
            email: "advocate@legal.in",
            fullName: "Advocate Rajesh Sharma",
            barCouncilId: "KAR/2012/9842",
            organizationId: "org_001",
            role: "LEAD_ADVOCATE",
          },
        },
      };
    }
    return {
      error: {
        code: "INVALID_CREDENTIALS",
        message: "Invalid email address or password.",
        requestId: "req_auth_001",
        retryable: true,
      },
    };
  }

  // Matter Methods
  async getMatters(organizationId: string): Promise<ApiResponse<Matter[]>> {
    return {
      data: [
        {
          id: "mat_001",
          organizationId: "org_001",
          title: "Title Diligence — Sy No 42/1 Devanahalli",
          clientName: "State Bank of India (Housing Finance)",
          surveyNumber: "42/1",
          district: "Bengaluru Rural",
          state: "Karnataka",
          documentCount: 12,
          status: "ACTIVE",
          createdBy: "usr_001",
          createdAt: "2026-08-10T10:00:00Z",
        },
        {
          id: "mat_002",
          organizationId: "org_001",
          title: "Land Acquisition Title Search — Khasra 104 Gurgaon",
          clientName: "DLF Cyber City Developers",
          surveyNumber: "104",
          district: "Gurugram",
          state: "Haryana",
          documentCount: 8,
          status: "ACTIVE",
          createdBy: "usr_001",
          createdAt: "2026-08-12T14:30:00Z",
        },
      ],
    };
  }

  async createMatter(matterData: Partial<Matter>): Promise<ApiResponse<Matter>> {
    const newMatter: Matter = {
      id: `mat_${Date.now()}`,
      organizationId: matterData.organizationId || "org_001",
      title: matterData.title || "Untitled Property Diligence",
      clientName: matterData.clientName || "General Client",
      surveyNumber: matterData.surveyNumber || "",
      district: matterData.district || "",
      state: matterData.state || "Karnataka",
      documentCount: 0,
      status: "ACTIVE",
      createdBy: "usr_001",
      createdAt: new Date().toISOString(),
    };
    return { data: newMatter };
  }

  // Document Methods
  async uploadDocuments(matterId: string, files: File[]): Promise<ApiResponse<{ jobId: string; documents: DocumentEntity[] }>> {
    const uploadedDocs: DocumentEntity[] = files.map((file, idx) => ({
      id: `doc_${Date.now()}_${idx}`,
      organizationId: "org_001",
      matterId,
      filename: file.name,
      fileHash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      fileSizeBytes: file.size,
      mimeType: file.type || "application/pdf",
      ocrStatus: "PROCESSED",
      pageCount: 12,
      uploadedBy: "usr_001",
      createdAt: new Date().toISOString(),
    }));
    return { data: { jobId: `job_${Date.now()}`, documents: uploadedDocs } };
  }

  // Property Intelligence Methods
  async getPropertyIntelligence(matterId: string): Promise<ApiResponse<{
    findings: ExtractedFinding[];
    timeline: TimelineEvent[];
    contradictions: Contradiction[];
  }>> {
    return {
      data: {
        findings: [
          {
            id: "fnd_001",
            matterId,
            documentId: "doc_001",
            entityType: "SURVEY_NO",
            extractedValue: "Survey No. 42/1 Hissa 2",
            verificationStatus: "HUMAN_VERIFIED",
            sourcePage: 2,
            citationIds: ["cit_001"],
            verifiedBy: "usr_001",
          },
          {
            id: "fnd_002",
            matterId,
            documentId: "doc_001",
            entityType: "EXTENT",
            extractedValue: "2 Acres 24 Guntas (104,544 Sq.Ft)",
            verifiedValue: "2 Acres 24 Guntas (104,544 Sq.Ft)",
            verificationStatus: "HUMAN_VERIFIED",
            sourcePage: 3,
            citationIds: ["cit_002"],
            verifiedBy: "usr_001",
          },
          {
            id: "fnd_003",
            matterId,
            documentId: "doc_002",
            entityType: "MORTGAGE",
            extractedValue: "Un-discharged Mortgage to Canara Bank (2011)",
            verificationStatus: "AI_EXTRACTION",
            sourcePage: 5,
            citationIds: ["cit_003"],
          },
        ],
        timeline: [
          {
            id: "tl_001",
            matterId,
            eventDate: "1985-08-14",
            documentId: "doc_001",
            documentName: "Absolute Sale Deed 1985.pdf",
            deedType: "Sale Deed",
            executant: "Venkatappa S/o Ramaiah",
            claimant: "Krishnappa S/o Govindappa",
            extentDescription: "2 Acres 24 Guntas in Sy No 42/1",
            considerationAmount: 150000,
            isLinkGapWarning: false,
            citationId: "cit_001",
          },
          {
            id: "tl_002",
            matterId,
            eventDate: "2004-03-22",
            documentId: "doc_002",
            documentName: "Partition Deed 2004.pdf",
            deedType: "Partition Deed",
            executant: "Krishnappa Family Members",
            claimant: "Ramesh Krishnappa (Son)",
            extentDescription: "2 Acres 20 Guntas in Sy No 42/1",
            considerationAmount: 0,
            isLinkGapWarning: true, // Link gap alert
            citationId: "cit_002",
          },
        ],
        contradictions: [
          {
            id: "cnt_001",
            matterId,
            title: "Land Extent Discrepancy Across Deeds",
            description: "1985 Sale Deed specifies extent as 2 Acres 24 Guntas (104,544 sq.ft), whereas 2004 Partition Deed specifies 2 Acres 20 Guntas (100,188 sq.ft).",
            severity: "CRITICAL",
            sourceA: { documentName: "Sale Deed 1985.pdf", page: 3, text: "Extent measuring 2 Acres 24 Guntas" },
            sourceB: { documentName: "Partition Deed 2004.pdf", page: 2, text: "Extent allotted measuring 2 Acres 20 Guntas" },
            status: "OPEN",
          },
        ],
      },
    };
  }

  // Audit Methods
  async getAuditLogs(matterId: string): Promise<ApiResponse<AuditEvent[]>> {
    return {
      data: [
        {
          id: "aud_001",
          organizationId: "org_001",
          matterId,
          userId: "usr_001",
          userName: "Advocate Rajesh Sharma",
          action: "DOCUMENT_UPLOADED",
          resourceType: "Document",
          resourceId: "doc_001",
          ipAddress: "49.207.210.42",
          timestamp: "2026-08-14T10:15:00Z",
        },
        {
          id: "aud_002",
          organizationId: "org_001",
          matterId,
          userId: "usr_001",
          userName: "Advocate Rajesh Sharma",
          action: "ENTITY_VERIFIED",
          resourceType: "ExtractedFinding",
          resourceId: "fnd_002",
          ipAddress: "49.207.210.42",
          timestamp: "2026-08-14T11:20:00Z",
        },
      ],
    };
  }
}

export const apiClient = new ApiClient();
