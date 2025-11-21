#!/usr/bin/env python
"""
Script to test the LLM interface functionality.
This script will:
1. Retrieve documents from MongoDB
2. Prepare them for LLM consumption
3. Print the formatted output
"""

import sys
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Import app modules
from app.services.llm_interface import LLMInterface
from app.db.mongodb import documents_collection
from app.db.postgres import SessionLocal
from app.models.document import DocumentMetadata

def get_document_ids():
    """Get all document IDs from MongoDB"""
    try:
        # Get all documents from MongoDB
        docs = documents_collection.find({}, {"document_id": 1})
        return [doc["document_id"] for doc in docs]
    except Exception as e:
        print(f"Error retrieving document IDs: {str(e)}")
        return []

async def test_document_preparation():
    """Test the document preparation for LLM"""
    print("Testing document preparation for LLM...")
    
    # Get all document IDs
    document_ids = get_document_ids()
    
    if not document_ids:
        print("No documents found in MongoDB. Please run the generate_test_data.py script first.")
        return
    
    print(f"Found {len(document_ids)} documents in MongoDB.")
    
    try:
        # Prepare documents for LLM
        prepared_docs = await LLMInterface.prepare_documents_for_llm(document_ids)
        
        # Print the result
        print("\nPrepared documents for LLM:")
        print(json.dumps(prepared_docs, indent=2))
        
        # Save to file for inspection
        output_file = Path(__file__).parent / "prepared_documents.json"
        with open(output_file, "w") as f:
            json.dump(prepared_docs, f, indent=2)
        
        print(f"\nPrepared documents saved to: {output_file}")
        
        # Print document statistics
        doc_count = len(prepared_docs.get("documents", []))
        print(f"\nDocument Statistics:")
        print(f"Total documents: {doc_count}")
        
        # Print document types
        doc_types = {}
        for doc in prepared_docs.get("documents", []):
            doc_type = doc.get("type")
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        print("\nDocument Types:")
        for doc_type, count in doc_types.items():
            print(f"  - {doc_type}: {count}")
        
    except Exception as e:
        print(f"Error preparing documents for LLM: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_document_search():
    """Test the document search functionality"""
    print("\nTesting document search functionality...")
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Import here to avoid circular imports
        from app.schemas.document import DocumentSearchQuery
        
        # Create a search query
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
        
    except Exception as e:
        print(f"Error searching documents: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

async def main():
    """Main function"""
    print("Starting LLM Interface Test")
    print("==========================\n")
    
    # Test document preparation
    await test_document_preparation()
    
    # Test document search
    await test_document_search()
    
    print("\nLLM Interface Test Completed")
    print("==========================")

if __name__ == "__main__":
    asyncio.run(main())
