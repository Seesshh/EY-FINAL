#!/usr/bin/env python
"""
Script to set up MongoDB indexes for the Business Resilience Tool.
This will create the necessary text indexes for document search.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Import app modules
from app.db.mongodb import documents_collection
from app.core.config import settings
from pymongo import MongoClient, IndexModel, ASCENDING, TEXT

def setup_mongodb_indexes():
    """Set up MongoDB indexes for document search"""
    print("Setting up MongoDB indexes...")
    
    try:
        # Create text index on content field
        documents_collection.create_index([("content", TEXT)], name="content_text_index")
        print("Created text index on 'content' field")
        
        # Create index on document_id for faster lookups
        documents_collection.create_index([("document_id", ASCENDING)], unique=True, name="document_id_index")
        print("Created index on 'document_id' field")
        
        # Create index on org_id for filtering
        documents_collection.create_index([("org_id", ASCENDING)], name="org_id_index")
        print("Created index on 'org_id' field")
        
        # Create index on document_type for filtering
        documents_collection.create_index([("document_type", ASCENDING)], name="document_type_index")
        print("Created index on 'document_type' field")
        
        # List all indexes to verify
        indexes = list(documents_collection.list_indexes())
        print(f"\nVerified indexes ({len(indexes)}):")
        for index in indexes:
            print(f"  - {index['name']}: {index['key']}")
        
        print("\nMongoDB indexes setup completed successfully!")
    
    except Exception as e:
        print(f"Error setting up MongoDB indexes: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_mongodb_indexes()
