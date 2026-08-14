# Database Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ MEMBERSHIPS : has
    ORGANIZATIONS ||--o{ MATTERS : owns
    USERS ||--o{ MEMBERSHIPS : belongs_to
    
    MATTERS ||--o{ DOCUMENTS : contains
    MATTERS ||--o{ EXTRACTED_ENTITIES : tracks
    MATTERS ||--o{ PROPERTY_TIMELINES : defines
    MATTERS ||--o{ AUDIT_LOGS : records
    
    DOCUMENTS ||--o{ DOCUMENT_PAGES : has
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : chunks
    DOCUMENT_PAGES ||--o{ EXTRACTED_ENTITIES : sources
    
    ORGANIZATIONS {
        uuid id PK
        string name
        string jurisdiction
        timestamp created_at
    }

    USERS {
        uuid id PK
        string email
        string hashed_password
        string full_name
        string bar_council_id
    }

    MEMBERSHIPS {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        string role
    }

    MATTERS {
        uuid id PK
        uuid organization_id FK
        string title
        string client_name
        string survey_number
    }

    DOCUMENTS {
        uuid id PK
        uuid organization_id FK
        uuid matter_id FK
        string filename
        string file_hash
        string ocr_status
    }

    DOCUMENT_CHUNKS {
        uuid id PK
        uuid document_id FK
        int page_number
        string content
        vector embedding
    }

    EXTRACTED_ENTITIES {
        uuid id PK
        uuid matter_id FK
        uuid document_id FK
        string entity_type
        string extracted_value
        string verification_status
    }

    AUDIT_LOGS {
        uuid id PK
        uuid organization_id FK
        uuid matter_id FK
        uuid user_id FK
        string action
        timestamp timestamp
    }
```
