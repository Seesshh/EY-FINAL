import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.postgres import Base
from app.core.config import settings

class DocumentType(enum.Enum):
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

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    description = Column(String, nullable=True)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    owner_email = Column(String, ForeignKey("users.email"))
    file_path = Column(String, nullable=True)
    file_format = Column(String, nullable=True)
    tags = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", backref="documents")
    owner = relationship("User", backref="documents", foreign_keys=[owner_email])
    
    # Vector embeddings relationship
    embeddings = relationship("DocumentEmbedding", back_populates="document", cascade="all, delete-orphan")

class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("document_metadata.id"), nullable=False)
    chunk_id = Column(String, nullable=False)
    chunk_text = Column(String, nullable=False)
    embedding = Column(String, nullable=True)  # Will be replaced with pgvector type
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    document = relationship("DocumentMetadata", back_populates="embeddings")
