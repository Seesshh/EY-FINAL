#!/usr/bin/env python
"""
Comprehensive test script for document processing pipeline.
This script tests the entire flow from database to LLM preparation.
"""

import sys
import os
import json
import asyncio
import uuid
from pathlib import Path
from datetime import datetime

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Import app modules
from app.services.llm_interface import LLMInterface
from app.db.mongodb import documents_collection
from app.db.postgres import SessionLocal, Base, engine
from app.models.document import DocumentMetadata, DocumentType
from app.core.config import settings
from pymongo import MongoClient, ASCENDING, TEXT

# Create a sample document for testing
SAMPLE_DOCUMENT = {
    "id": str(uuid.uuid4()),
    "title": "Test Document for LLM Processing",
    "document_type": DocumentType.POLICY.value,
    "description": "A test document to verify LLM processing pipeline",
    "org_id": str(uuid.uuid4()),  # Random org ID for testing
    "owner_email": "test@example.com",
    "file_format": "txt",
    "tags": ["test", "llm", "processing"],
    "content": """
# Test Document

This is a test document to verify the LLM processing pipeline. It contains various sections
that can be used to test different aspects of document processing.

## Section 1: Policies

This section contains sample policy information:

1. All employees must complete security training annually
2. Passwords must be changed every 90 days
3. Two-factor authentication is required for all system access

## Section 2: Procedures

This section contains sample procedures:

1. In case of a security incident, contact the security team immediately
2. Regular backups must be performed daily
3. All code changes must go through peer review

## Section 3: Technical Information

This section contains technical details:

- Database: PostgreSQL and MongoDB
- Authentication: JWT-based
- API: RESTful with FastAPI
- Deployment: Docker containers

This document should be processed by the LLM to extract key information and provide insights.
"""
}

async def setup_mongodb_indexes():
    """Set up MongoDB indexes for document search"""
    print("Setting up MongoDB indexes...")
    
    try:
        # Create text index on content field
        documents_collection.create_index([("content", TEXT)], name="content_text_index")
        print("Created text index on 'content' field")
        
        # Create index on document_id for faster lookups
        documents_collection.create_index([("document_id", ASCENDING)], unique=True, name="document_id_index")
        print("Created index on 'document_id' field")
        
        # List all indexes to verify
        indexes = list(documents_collection.list_indexes())
        print(f"Verified indexes ({len(indexes)})")
        
        return True
    except Exception as e:
        print(f"Error setting up MongoDB indexes: {str(e)}")
        return False

def insert_test_document():
    """Insert a test document into PostgreSQL and MongoDB"""
    print("Inserting test document...")
    
    db = SessionLocal()
    try:
        # Check if tables exist, create if not
        Base.metadata.create_all(bind=engine)
        
        # Create document metadata in PostgreSQL
        doc_id = SAMPLE_DOCUMENT["id"]
        
        # Check if document already exists
        existing_doc = db.query(DocumentMetadata).filter(DocumentMetadata.id == doc_id).first()
        if existing_doc:
            print(f"Test document already exists with ID: {doc_id}")
            return doc_id
        
        # Create new document metadata
        doc_metadata = DocumentMetadata(
            id=doc_id,
            title=SAMPLE_DOCUMENT["title"],
            document_type=SAMPLE_DOCUMENT["document_type"],
            description=SAMPLE_DOCUMENT["description"],
            org_id=SAMPLE_DOCUMENT["org_id"],
            owner_email=SAMPLE_DOCUMENT["owner_email"],
            file_format=SAMPLE_DOCUMENT["file_format"],
            tags=SAMPLE_DOCUMENT["tags"]
        )
        
        db.add(doc_metadata)
        db.commit()
        
        # Insert document content into MongoDB
        mongo_doc = {
            "document_id": doc_id,
            "org_id": SAMPLE_DOCUMENT["org_id"],
            "document_type": SAMPLE_DOCUMENT["document_type"],
            "content": SAMPLE_DOCUMENT["content"],
            "metadata": {
                "title": SAMPLE_DOCUMENT["title"],
                "description": SAMPLE_DOCUMENT["description"],
                "owner_email": SAMPLE_DOCUMENT["owner_email"],
                "tags": SAMPLE_DOCUMENT["tags"],
                "file_format": SAMPLE_DOCUMENT["file_format"]
            },
            "version_history": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        documents_collection.insert_one(mongo_doc)
        print(f"Inserted test document with ID: {doc_id}")
        
        return doc_id
    
    except Exception as e:
        db.rollback()
        print(f"Error inserting test document: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()

async def test_document_preparation(document_id):
    """Test the document preparation for LLM"""
    print("\nTesting document preparation for LLM...")
    
    try:
        # Prepare document for LLM
        prepared_docs = await LLMInterface.prepare_documents_for_llm([document_id])
        
        # Print the result
        print("\nPrepared document for LLM:")
        print(json.dumps(prepared_docs, indent=2))
        
        # Save to file for inspection
        output_file = Path(__file__).parent / "prepared_document.json"
        with open(output_file, "w") as f:
            json.dump(prepared_docs, f, indent=2)
        
        print(f"\nPrepared document saved to: {output_file}")
        
        # Verify document structure
        if "documents" in prepared_docs and len(prepared_docs["documents"]) > 0:
            doc = prepared_docs["documents"][0]
            print("\nDocument structure verification:")
            print(f"  - ID: {doc.get('id') == document_id}")
            print(f"  - Type: {doc.get('type') == SAMPLE_DOCUMENT['document_type']}")
            print(f"  - Title: {doc.get('title') == SAMPLE_DOCUMENT['title']}")
            print(f"  - Content present: {len(doc.get('content', '')) > 0}")
            print(f"  - Metadata present: {doc.get('metadata') is not None}")
            
            return True
        else:
            print("Error: No documents found in prepared data")
            return False
    
    except Exception as e:
        print(f"Error preparing document for LLM: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_document_search():
    """Test the document search functionality"""
    print("\nTesting document search functionality...")
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Import here to avoid circular imports
        from app.schemas.document import DocumentSearchQuery
        
        # Create a search query for policies
        query = DocumentSearchQuery(
            query="policy",  # Search for documents containing "policy"
            limit=5
        )
        
        # Search for documents
        search_results = await LLMInterface.search_documents(query, db)
        
        # Print the results
        print(f"\nFound {len(search_results)} documents matching the query 'policy':")
        for i, result in enumerate(search_results, 1):
            print(f"\n{i}. {result.title} (Score: {result.score:.2f})")
            print(f"   Document Type: {result.document_type}")
            print(f"   Preview: {result.chunk_text[:100]}...")
        
        # Create a search query for technical information
        query = DocumentSearchQuery(
            query="technical",  # Search for documents containing "technical"
            limit=5
        )
        
        # Search for documents
        search_results = await LLMInterface.search_documents(query, db)
        
        # Print the results
        print(f"\nFound {len(search_results)} documents matching the query 'technical':")
        for i, result in enumerate(search_results, 1):
            print(f"\n{i}. {result.title} (Score: {result.score:.2f})")
            print(f"   Document Type: {result.document_type}")
            print(f"   Preview: {result.chunk_text[:100]}...")
        
        return True
    
    except Exception as e:
        print(f"Error searching documents: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

async def main():
    """Main function"""
    print("Starting Document Processing Test")
    print("================================\n")
    
    # Step 1: Set up MongoDB indexes
    indexes_setup = await setup_mongodb_indexes()
    if not indexes_setup:
        print("Failed to set up MongoDB indexes. Exiting.")
        return
    
    # Step 2: Insert test document
    document_id = insert_test_document()
    if not document_id:
        print("Failed to insert test document. Exiting.")
        return
    
    # Step 3: Test document preparation for LLM
    preparation_success = await test_document_preparation(document_id)
    if not preparation_success:
        print("Document preparation test failed. Continuing with search test...")
    
    # Step 4: Test document search
    search_success = await test_document_search()
    if not search_success:
        print("Document search test failed.")
    
    print("\nDocument Processing Test Completed")
    print("================================")
    
    # Summary
    print("\nTest Summary:")
    print(f"  - MongoDB Indexes Setup: {'Success' if indexes_setup else 'Failed'}")
    print(f"  - Test Document Insertion: {'Success' if document_id else 'Failed'}")
    print(f"  - Document Preparation for LLM: {'Success' if preparation_success else 'Failed'}")
    print(f"  - Document Search: {'Success' if search_success else 'Failed'}")
    
    # Next steps
    print("\nNext Steps:")
    if preparation_success:
        print("  1. Review the prepared_document.json file to verify the document structure for LLM")
        print("  2. Implement the LLM integration using the prepared document format")
        print("  3. Test the end-to-end flow with the actual LLM")
    else:
        print("  1. Fix the document preparation issues before proceeding")
        print("  2. Run this test script again to verify the fixes")

if __name__ == "__main__":
    asyncio.run(main())
