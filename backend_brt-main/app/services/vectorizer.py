import uuid
from typing import List, Dict, Any, Optional
import re
from sqlalchemy.orm import Session

from app.models.document import DocumentEmbedding, DocumentMetadata
from app.db.mongodb import documents_collection

class Vectorizer:
    """Service for vectorizing documents for semantic search"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        if not text:
            return []
        
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # If text is shorter than chunk size, return it as a single chunk
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Get chunk of text
            end = start + self.chunk_size
            if end > len(text):
                end = len(text)
            
            chunk = text[start:end]
            
            # Try to end at a sentence or paragraph boundary
            if end < len(text):
                # Look for paragraph break
                para_break = chunk.rfind('\n\n')
                if para_break != -1 and para_break > self.chunk_size // 2:
                    chunk = chunk[:para_break]
                    end = start + para_break
                else:
                    # Look for sentence break (period followed by space)
                    sentence_break = chunk.rfind('. ')
                    if sentence_break != -1 and sentence_break > self.chunk_size // 2:
                        chunk = chunk[:sentence_break+1]  # Include the period
                        end = start + sentence_break + 1
            
            chunks.append(chunk)
            start = end - self.chunk_overlap
        
        return chunks
    
    async def vectorize_document(self, document_id: str, db: Session) -> List[str]:
        """
        Retrieve document from MongoDB, chunk it, and store embeddings in PostgreSQL
        Returns list of chunk IDs
        """
        # Get document from MongoDB
        doc = documents_collection.find_one({"document_id": document_id})
        if not doc:
            return []
        
        # Get document content
        content = doc.get("content", "")
        
        # Chunk the content
        chunks = self.chunk_text(content)
        
        # Store chunks in PostgreSQL
        chunk_ids = []
        
        for i, chunk_text in enumerate(chunks):
            chunk_id = f"{document_id}-chunk-{i}"
            
            # Create embedding record
            embedding = DocumentEmbedding(
                document_id=document_id,
                chunk_id=chunk_id,
                chunk_text=chunk_text,
                # The actual embedding vector will be added by the embedding service
            )
            
            db.add(embedding)
            chunk_ids.append(chunk_id)
        
        db.commit()
        
        return chunk_ids
    
    @staticmethod
    async def get_document_chunks(document_id: str, db: Session) -> List[Dict[str, Any]]:
        """Get all chunks for a document"""
        chunks = db.query(DocumentEmbedding).filter(
            DocumentEmbedding.document_id == document_id
        ).all()
        
        return [
            {
                "chunk_id": chunk.chunk_id,
                "chunk_text": chunk.chunk_text,
                "embedding": chunk.embedding
            }
            for chunk in chunks
        ]
    
    @staticmethod
    async def update_embedding(chunk_id: str, embedding: List[float], db: Session) -> bool:
        """Update the embedding for a chunk"""
        chunk = db.query(DocumentEmbedding).filter(
            DocumentEmbedding.chunk_id == chunk_id
        ).first()
        
        if not chunk:
            return False
        
        # Convert embedding to string representation
        # This will be replaced with pgvector type in production
        chunk.embedding = str(embedding)
        db.commit()
        
        return True
