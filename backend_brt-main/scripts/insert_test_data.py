#!/usr/bin/env python
"""
Script to insert test data into both PostgreSQL and MongoDB.
This script uses SQLAlchemy ORM instead of raw SQL to ensure compatibility.
"""

import sys
import os
import json
import uuid
from pathlib import Path
from datetime import datetime

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Import app modules
from app.db.mongodb import documents_collection
from app.db.postgres import SessionLocal, Base, engine
from app.models.document import DocumentMetadata, DocumentType
from app.models.organization import Organization
from app.models.user import User
from app.core.security import get_password_hash

# Sample data
ORGANIZATION = {
    "id": str(uuid.uuid4()),
    "name": "Test Organization",
    "industry": "Technology",
    "size": 500,
    "address": "123 Test St, Test City, TS 12345",
    "contact_email": "contact@testorg.com",
    "contact_phone": "555-123-4567",
    "website": "https://testorg.com",
    "description": "A test organization for API testing"
}

USER = {
    "id": str(uuid.uuid4()),
    "email": "admin@testorg.com",
    "password": "password123",
    "first_name": "Admin",
    "last_name": "User",
    "is_active": True,
    "is_superuser": True,
    "role": "admin"
}

DOCUMENTS = [
    {
        "id": str(uuid.uuid4()),
        "title": "Business Continuity Plan",
        "document_type": DocumentType.DR_BCP_PLAN.value,
        "description": "Plan for maintaining business operations during disruptions",
        "file_format": "docx",
        "tags": ["continuity", "disaster recovery", "planning"],
        "content": """
# Business Continuity Plan

## Purpose
This Business Continuity Plan (BCP) outlines the procedures to maintain or quickly resume critical business functions in the event of a major disruption.

## Scope
This plan covers all critical business operations and systems.

## Recovery Strategies
1. IT Systems Recovery
   - Backup and restore procedures
   - Alternative processing sites
   - Cloud-based recovery solutions

2. Workforce Recovery
   - Remote work capabilities
   - Alternative work locations
   - Cross-training of personnel

3. Critical Business Functions
   - Order processing
   - Customer service
   - Financial operations
   - Supply chain management

## Testing and Maintenance
This plan should be tested annually and updated as needed.
"""
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Information Security Policy",
        "document_type": DocumentType.POLICY.value,
        "description": "Company-wide information security policy",
        "file_format": "pdf",
        "tags": ["security", "policy", "compliance"],
        "content": """
# Information Security Policy

## Overview
This Information Security Policy establishes guidelines for protecting company information assets.

## Scope
This policy applies to all employees, contractors, and third parties with access to company information.

## Policy Statements
1. Access Control
   - Least privilege principle
   - Regular access reviews
   - Strong authentication requirements

2. Data Protection
   - Classification of information
   - Encryption requirements
   - Secure disposal procedures

3. Incident Response
   - Reporting procedures
   - Investigation process
   - Recovery and lessons learned

## Compliance
Violations of this policy may result in disciplinary action.
"""
    }
]

def create_test_data():
    """Create test data in PostgreSQL and MongoDB"""
    print("Creating test data...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Insert organization
        org = Organization(
            id=ORGANIZATION["id"],
            name=ORGANIZATION["name"],
            industry=ORGANIZATION["industry"],
            size=ORGANIZATION["size"],
            address=ORGANIZATION["address"],
            contact_email=ORGANIZATION["contact_email"],
            contact_phone=ORGANIZATION["contact_phone"],
            website=ORGANIZATION["website"],
            description=ORGANIZATION["description"]
        )
        
        # Check if organization already exists
        existing_org = db.query(Organization).filter(Organization.id == ORGANIZATION["id"]).first()
        if not existing_org:
            db.add(org)
            db.flush()  # Flush to get the ID
            print(f"Created organization: {org.name}")
        else:
            print(f"Organization already exists: {existing_org.name}")
            org = existing_org
        
        # Insert user
        user = User(
            id=USER["id"],
            email=USER["email"],
            hashed_password=get_password_hash(USER["password"]),
            first_name=USER["first_name"],
            last_name=USER["last_name"],
            is_active=USER["is_active"],
            is_superuser=USER["is_superuser"],
            org_id=org.id,
            role=USER["role"]
        )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == USER["email"]).first()
        if not existing_user:
            db.add(user)
            db.flush()  # Flush to get the ID
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {existing_user.email}")
            user = existing_user
        
        # Insert documents
        for doc_data in DOCUMENTS:
            # Create document metadata in PostgreSQL
            doc_metadata = DocumentMetadata(
                id=doc_data["id"],
                title=doc_data["title"],
                document_type=doc_data["document_type"],
                description=doc_data["description"],
                org_id=org.id,
                owner_email=user.email,
                file_format=doc_data["file_format"],
                tags=doc_data["tags"]
            )
            
            # Check if document already exists
            existing_doc = db.query(DocumentMetadata).filter(DocumentMetadata.id == doc_data["id"]).first()
            if not existing_doc:
                db.add(doc_metadata)
                db.flush()  # Flush to get the ID
                
                # Insert document content into MongoDB
                mongo_doc = {
                    "document_id": doc_data["id"],
                    "org_id": org.id,
                    "document_type": doc_data["document_type"],
                    "content": doc_data["content"],
                    "metadata": {
                        "title": doc_data["title"],
                        "description": doc_data["description"],
                        "owner_email": user.email,
                        "tags": doc_data["tags"],
                        "file_format": doc_data["file_format"]
                    },
                    "version_history": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                # Check if document already exists in MongoDB
                existing_mongo_doc = documents_collection.find_one({"document_id": doc_data["id"]})
                if not existing_mongo_doc:
                    documents_collection.insert_one(mongo_doc)
                    print(f"Created document: {doc_data['title']}")
                else:
                    print(f"Document already exists in MongoDB: {doc_data['title']}")
            else:
                print(f"Document already exists in PostgreSQL: {existing_doc.title}")
        
        # Commit changes to PostgreSQL
        db.commit()
        print("Test data creation completed successfully!")
    
    except Exception as e:
        db.rollback()
        print(f"Error creating test data: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
