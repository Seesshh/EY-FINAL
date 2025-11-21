from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    SOP = "SOP"
    RISK_REGISTER = "RISK_REGISTER"
    ROLE_CHART = "ROLE_CHART"
    PROCESS_MANUAL = "PROCESS_MANUAL"
    ARCHITECTURE_DIAGRAM = "ARCHITECTURE_DIAGRAM"
    INCIDENT_LOG = "INCIDENT_LOG"
    VENDOR_CONTRACT = "VENDOR_CONTRACT"
    POLICY = "POLICY"
    DR_BCP_PLAN = "DR_BCP_PLAN"
    CHAT_HISTORY = "CHAT_HISTORY"
    EXTERNAL_DOCUMENT = "EXTERNAL_DOCUMENT"

# Shared properties
class DocumentBase(BaseModel):
    title: str
    document_type: DocumentType
    description: Optional[str] = None
    org_id: UUID
    owner_email: EmailStr
    tags: Optional[List[str]] = None

# Properties to receive on document creation
class DocumentCreate(DocumentBase):
    content: str
    file_format: Optional[str] = None

# Properties to receive on document update
class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

# Properties shared by models stored in DB
class DocumentInDBBase(DocumentBase):
    id: UUID
    file_path: Optional[str] = None
    file_format: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties to return to client
class Document(DocumentInDBBase):
    pass

# Properties stored in MongoDB
class DocumentContent(BaseModel):
    document_id: UUID
    content: str
    metadata: Dict[str, Any] = {}
    version_history: List[Dict[str, Any]] = []

# Document embedding
class DocumentEmbeddingBase(BaseModel):
    document_id: UUID
    chunk_id: str
    chunk_text: str

class DocumentEmbeddingCreate(DocumentEmbeddingBase):
    embedding: Optional[List[float]] = None

class DocumentEmbedding(DocumentEmbeddingBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

# Document search
class DocumentSearchQuery(BaseModel):
    query: str
    document_type: Optional[DocumentType] = None
    org_id: Optional[UUID] = None
    limit: int = 10

class DocumentSearchResult(BaseModel):
    document_id: UUID
    title: str
    document_type: DocumentType
    chunk_text: str
    score: float
    metadata: Dict[str, Any] = {}
