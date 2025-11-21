#!/usr/bin/env python
"""
Script to generate test data for the Business Resilience Tool.
This will create organizations, users, and documents in both PostgreSQL and MongoDB.
"""

import sys
import os
import json
import uuid
import requests
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Import app modules
from app.core.security import get_password_hash
from app.models.document import DocumentType
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.postgres import Base
from app.core.config import settings
from pymongo import MongoClient

# Connect to PostgreSQL
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Connect to MongoDB
client = MongoClient(settings.MONGODB_URL)
mongodb = client[settings.MONGODB_DB]
documents_collection = mongodb["documents"]

# Sample data
organizations = [
    {
        "id": str(uuid.uuid4()),
        "name": "Acme Corporation",
        "industry": "Manufacturing",
        "size": 1500,
        "address": "123 Main St, New York, NY 10001",
        "contact_email": "contact@acme.com",
        "contact_phone": "212-555-1234",
        "website": "https://acme.com",
        "description": "A global manufacturing company specializing in innovative products."
    },
    {
        "id": str(uuid.uuid4()),
        "name": "TechNova Solutions",
        "industry": "Information Technology",
        "size": 500,
        "address": "456 Tech Blvd, San Francisco, CA 94107",
        "contact_email": "info@technova.com",
        "contact_phone": "415-555-6789",
        "website": "https://technova.com",
        "description": "Leading provider of enterprise software solutions."
    },
    {
        "id": str(uuid.uuid4()),
        "name": "FinSecure Bank",
        "industry": "Financial Services",
        "size": 2500,
        "address": "789 Finance Ave, Chicago, IL 60601",
        "contact_email": "support@finsecure.com",
        "contact_phone": "312-555-9012",
        "website": "https://finsecure.com",
        "description": "A trusted financial institution with over 50 years of experience."
    }
]

users = [
    {
        "id": str(uuid.uuid4()),
        "email": "admin@acme.com",
        "hashed_password": get_password_hash("password123"),
        "first_name": "John",
        "last_name": "Smith",
        "is_active": True,
        "is_superuser": True,
        "org_id": organizations[0]["id"],
        "role": "Admin"
    },
    {
        "id": str(uuid.uuid4()),
        "email": "manager@acme.com",
        "hashed_password": get_password_hash("password123"),
        "first_name": "Jane",
        "last_name": "Doe",
        "is_active": True,
        "is_superuser": False,
        "org_id": organizations[0]["id"],
        "role": "Manager"
    },
    {
        "id": str(uuid.uuid4()),
        "email": "admin@technova.com",
        "hashed_password": get_password_hash("password123"),
        "first_name": "Michael",
        "last_name": "Johnson",
        "is_active": True,
        "is_superuser": True,
        "org_id": organizations[1]["id"],
        "role": "Admin"
    },
    {
        "id": str(uuid.uuid4()),
        "email": "admin@finsecure.com",
        "hashed_password": get_password_hash("password123"),
        "first_name": "Sarah",
        "last_name": "Williams",
        "is_active": True,
        "is_superuser": True,
        "org_id": organizations[2]["id"],
        "role": "Admin"
    }
]

documents = [
    # Acme Corporation Documents
    {
        "id": str(uuid.uuid4()),
        "title": "Emergency Response Plan",
        "document_type": DocumentType.DR_BCP_PLAN.value,
        "description": "Comprehensive plan for responding to emergencies and disasters",
        "org_id": organizations[0]["id"],
        "owner_email": users[0]["email"],
        "file_format": "docx",
        "tags": ["emergency", "disaster", "response"],
        "content": """
# Emergency Response Plan for Acme Corporation

## Purpose
This plan outlines the procedures to be followed in case of an emergency or disaster affecting Acme Corporation operations.

## Emergency Response Team
- John Smith, Emergency Coordinator (ext. 1234)
- Jane Doe, Deputy Coordinator (ext. 5678)
- Michael Johnson, Communications Lead (ext. 9012)

## Emergency Procedures
1. Assess the situation and determine the type of emergency
2. Contact the appropriate emergency services if needed
3. Evacuate the building if necessary, following the evacuation routes
4. Account for all employees at the designated assembly points
5. Provide first aid as needed
6. Communicate with employees, customers, and stakeholders

## Recovery Procedures
1. Assess damage to facilities and equipment
2. Implement business continuity measures
3. Restore critical systems and operations
4. Communicate recovery status to stakeholders
5. Review and update the emergency response plan based on lessons learned

## Contact Information
- Emergency Services: 911
- Building Security: 212-555-7890
- IT Support: 212-555-4321
"""
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Risk Register",
        "document_type": DocumentType.RISK_REGISTER.value,
        "description": "Comprehensive risk assessment for Acme Corporation",
        "org_id": organizations[0]["id"],
        "owner_email": users[1]["email"],
        "file_format": "xlsx",
        "tags": ["risk", "assessment", "mitigation"],
        "content": json.dumps([
            {
                "risk_id": "R001",
                "risk_category": "Operational",
                "risk_description": "Production line failure",
                "likelihood": "Medium",
                "impact": "High",
                "mitigation_strategy": "Regular maintenance schedule and backup equipment",
                "owner": "Operations Manager",
                "status": "Active"
            },
            {
                "risk_id": "R002",
                "risk_category": "Financial",
                "risk_description": "Currency exchange rate fluctuations",
                "likelihood": "High",
                "impact": "Medium",
                "mitigation_strategy": "Hedging strategy and diversified markets",
                "owner": "Finance Director",
                "status": "Active"
            },
            {
                "risk_id": "R003",
                "risk_category": "Compliance",
                "risk_description": "Non-compliance with new regulations",
                "likelihood": "Medium",
                "impact": "High",
                "mitigation_strategy": "Regular compliance audits and legal reviews",
                "owner": "Compliance Officer",
                "status": "Monitoring"
            }
        ])
    },
    
    # TechNova Solutions Documents
    {
        "id": str(uuid.uuid4()),
        "title": "System Architecture Diagram",
        "document_type": DocumentType.ARCHITECTURE_DIAGRAM.value,
        "description": "High-level architecture diagram of TechNova's core systems",
        "org_id": organizations[1]["id"],
        "owner_email": users[2]["email"],
        "file_format": "docx",
        "tags": ["architecture", "systems", "infrastructure"],
        "content": """
# TechNova Solutions System Architecture

## Overview
This document provides a high-level overview of TechNova's core system architecture.

## Components

### Frontend Layer
- Web Application (React.js)
- Mobile Application (React Native)
- Admin Dashboard (Angular)

### API Layer
- REST API Gateway (Node.js/Express)
- GraphQL API (Apollo Server)
- Authentication Service (OAuth 2.0)

### Backend Services
- User Service (Java/Spring Boot)
- Product Service (Python/FastAPI)
- Analytics Service (Go)
- Notification Service (Node.js)

### Data Layer
- PostgreSQL (Transactional Data)
- MongoDB (Document Storage)
- Redis (Caching)
- Elasticsearch (Search)

### Infrastructure
- AWS Cloud Infrastructure
- Kubernetes Orchestration
- CI/CD Pipeline (Jenkins)
- Monitoring (Prometheus/Grafana)

## Data Flow
1. User requests come through the Frontend Layer
2. Requests are routed through the API Gateway
3. Backend Services process the requests
4. Data is stored and retrieved from the Data Layer
5. Responses are returned to the user

## Security Measures
- SSL/TLS Encryption
- JWT Authentication
- Role-Based Access Control
- Regular Security Audits
"""
    },
    
    # FinSecure Bank Documents
    {
        "id": str(uuid.uuid4()),
        "title": "Information Security Policy",
        "document_type": DocumentType.POLICY.value,
        "description": "Information security policy for FinSecure Bank",
        "org_id": organizations[2]["id"],
        "owner_email": users[3]["email"],
        "file_format": "docx",
        "tags": ["security", "policy", "compliance"],
        "content": """
# Information Security Policy

## Purpose
This policy establishes guidelines for protecting FinSecure Bank's information assets from unauthorized access, use, disclosure, disruption, modification, or destruction.

## Scope
This policy applies to all employees, contractors, consultants, temporary staff, and other workers at FinSecure Bank, including personnel affiliated with third parties.

## Policy Statements

### Data Classification
All data must be classified according to its sensitivity:
- Public
- Internal
- Confidential
- Restricted

### Access Control
- Access to information systems must be granted based on the principle of least privilege
- All access rights must be reviewed quarterly
- Strong authentication mechanisms must be implemented for all systems

### Password Requirements
- Minimum 12 characters
- Combination of uppercase, lowercase, numbers, and special characters
- Changed every 90 days
- No reuse of the last 10 passwords

### Incident Response
- All security incidents must be reported to the Information Security team immediately
- A formal incident response procedure must be followed
- Post-incident reviews must be conducted to identify improvements

### Compliance
- Annual security awareness training is mandatory for all staff
- Regular security assessments and audits must be conducted
- Non-compliance may result in disciplinary action

## Responsibilities
- Information Security Officer: Policy maintenance and enforcement
- Department Managers: Implementation within their departments
- All Employees: Compliance with the policy

## Review
This policy will be reviewed annually or when significant changes occur.
"""
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Vendor Contract - Core Banking System",
        "document_type": DocumentType.VENDOR_CONTRACT.value,
        "description": "Contract with FIS for core banking system",
        "org_id": organizations[2]["id"],
        "owner_email": users[3]["email"],
        "file_format": "docx",
        "tags": ["vendor", "contract", "banking"],
        "content": """
# VENDOR CONTRACT

## PARTIES
This Service Agreement ("Agreement") is entered into as of January 15, 2023, by and between:

FinSecure Bank ("Client")
789 Finance Ave, Chicago, IL 60601

AND

Financial Information Systems, Inc. ("Vendor")
456 Tech Park, Boston, MA 02110

## SERVICES
Vendor agrees to provide the following services ("Services") to Client:

1. Implementation and maintenance of the CoreBanking Pro system
2. Data migration from legacy systems
3. Staff training on system usage
4. 24/7 technical support
5. Regular system updates and security patches

## TERM
The initial term of this Agreement shall be for a period of five (5) years commencing on February 1, 2023, and ending on January 31, 2028.

## FEES AND PAYMENT
Client agrees to pay Vendor the following fees:
- Implementation Fee: $1,500,000 (payable in three installments)
- Annual License Fee: $750,000 (payable quarterly)
- Support Fee: $250,000 per year (payable quarterly)

## SERVICE LEVEL AGREEMENT
Vendor guarantees the following service levels:
- System Uptime: 99.95% (excluding scheduled maintenance)
- Response Time for Critical Issues: 15 minutes
- Resolution Time for Critical Issues: 4 hours

## CONFIDENTIALITY
Both parties agree to maintain the confidentiality of all information shared during the course of this Agreement.

## TERMINATION
Either party may terminate this Agreement with 180 days written notice. Early termination fees may apply.

## SIGNATURES

________________________
For FinSecure Bank

________________________
For Financial Information Systems, Inc.
"""
    }
]

def create_test_data():
    """Create test data in PostgreSQL and MongoDB"""
    
    print("Creating test data...")
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Insert organizations
        for org_data in organizations:
            # Check if organization already exists
            org_id = org_data["id"]
            existing_org = db.execute(text(f"SELECT id FROM organizations WHERE id = '{org_id}'")).fetchone()
            
            if not existing_org:
                db.execute(text(
                    f"""
                    INSERT INTO organizations (id, name, industry, size, address, contact_email, 
                    contact_phone, website, description, created_at, updated_at)
                    VALUES (
                        '{org_data["id"]}', 
                        '{org_data["name"]}', 
                        '{org_data["industry"]}', 
                        {org_data["size"]}, 
                        '{org_data["address"]}', 
                        '{org_data["contact_email"]}', 
                        '{org_data["contact_phone"]}', 
                        '{org_data["website"]}', 
                        '{org_data["description"]}',
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                    """)
                )
                print(f"Created organization: {org_data['name']}")
            else:
                print(f"Organization already exists: {org_data['name']}")
        
        # Insert users
        for user_data in users:
            # Check if user already exists
            user_id = user_data["id"]
            existing_user = db.execute(text(f"SELECT id FROM users WHERE id = '{user_id}'")).fetchone()
            
            if not existing_user:
                db.execute(text(
                    f"""
                    INSERT INTO users (id, email, hashed_password, first_name, last_name, 
                    is_active, is_superuser, org_id, role, created_at, updated_at)
                    VALUES (
                        '{user_data["id"]}', 
                        '{user_data["email"]}', 
                        '{user_data["hashed_password"]}', 
                        '{user_data["first_name"]}', 
                        '{user_data["last_name"]}', 
                        {str(user_data["is_active"]).lower()}, 
                        {str(user_data["is_superuser"]).lower()}, 
                        '{user_data["org_id"]}', 
                        '{user_data["role"]}',
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                    """)
                )
                print(f"Created user: {user_data['email']}")
            else:
                print(f"User already exists: {user_data['email']}")
        
        # Insert documents
        for doc_data in documents:
            # Check if document already exists
            doc_id = doc_data["id"]
            existing_doc = db.execute(text(f"SELECT id FROM document_metadata WHERE id = '{doc_id}'")).fetchone()
            
            if not existing_doc:
                # Insert document metadata into PostgreSQL
                tags_json = json.dumps(doc_data["tags"])
                db.execute(text(
                    f"""
                    INSERT INTO document_metadata (id, title, document_type, description, org_id, 
                    owner_email, file_format, tags, created_at, updated_at)
                    VALUES (
                        '{doc_data["id"]}', 
                        '{doc_data["title"]}', 
                        '{doc_data["document_type"]}', 
                        '{doc_data["description"]}', 
                        '{doc_data["org_id"]}', 
                        '{doc_data["owner_email"]}', 
                        '{doc_data["file_format"]}', 
                        '{tags_json}',
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                    """)
                )
                
                # Insert document content into MongoDB
                mongo_doc = {
                    "document_id": doc_data["id"],
                    "org_id": doc_data["org_id"],
                    "document_type": doc_data["document_type"],
                    "content": doc_data["content"],
                    "metadata": {
                        "title": doc_data["title"],
                        "description": doc_data["description"],
                        "owner_email": doc_data["owner_email"],
                        "tags": doc_data["tags"],
                        "file_format": doc_data["file_format"]
                    },
                    "version_history": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                documents_collection.insert_one(mongo_doc)
                print(f"Created document: {doc_data['title']}")
            else:
                print(f"Document already exists: {doc_data['title']}")
        
        # Commit changes to PostgreSQL
        db.commit()
        print("Test data creation completed successfully!")
    
    except Exception as e:
        db.rollback()
        print(f"Error creating test data: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
