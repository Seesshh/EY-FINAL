# Business Resilience Tool

A FastAPI backend project with polyglot persistence (MongoDB + PostgreSQL) for managing business resilience data.

## Overview

This tool manages various types of business resilience data including:

- Standard Operating Procedures (SOPs)
- Risk Registers
- Role Charts (RACI)
- Process Manuals
- Architecture Diagrams
- Incident Logs
- Vendor Contracts
- Policies
- DR/BCP Plans
- Chat History Logs
- External Documents (CSV/Excel/Docx)

The system uses PostgreSQL for structured data and MongoDB for unstructured data, with a linking mechanism between the two databases. Document vectorization is implemented using pgvector to enable semantic search capabilities for LLM integration.

## Architecture

- **Database Layer**:
  - PostgreSQL for structured data (organizations, users, relationships)
  - MongoDB for unstructured documents
  - PostgreSQL with pgvector for vector embeddings

- **API Layer**:
  - FastAPI endpoints for CRUD operations
  - Document processing pipeline
  - Authentication and authorization

- **Integration Layer**:
  - Document vectorization service
  - LLM integration interface

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.11+

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd business-resilience-tool
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the Docker containers:

```bash
docker-compose up -d
```

4. Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the Swagger UI documentation at:

http://localhost:8000/docs

## Data Model

### PostgreSQL (Structured Data)

1. **Organizations Table**:
   - Primary key: org_id (UUID)
   - Fields: name, industry, size, contact_info, etc.

2. **Users Table**:
   - Primary key: email
   - Fields: name, role, org_id (foreign key to Organizations)

3. **Document Metadata Table**:
   - Primary key: document_id (UUID)
   - Fields: title, type, created_at, updated_at, owner_email, org_id

4. **Vector Embeddings Table**:
   - Primary key: embedding_id
   - Fields: document_id, embedding, chunk_id, chunk_text

### MongoDB (Unstructured Data)

1. **Documents Collection**:
   - _id: document_id (same as in PostgreSQL Document Metadata)
   - content: The actual document content
   - metadata: Additional metadata specific to document type
   - version_history: Array of previous versions

## Features

- **Authentication and Authorization**: JWT-based authentication with role-based access control
- **Document Management**: Upload, retrieve, update, and delete various document types
- **Document Processing**: Process different file formats (Excel, Word, CSV)
- **Semantic Search**: Search documents using natural language queries
- **Versioning**: Track document changes with version history
- **Organization Management**: Multi-tenant support with organization-level isolation

## LLM Integration

The system is designed to integrate with Language Models by:

1. Storing document content in a format suitable for LLM consumption
2. Providing vector embeddings for semantic search
3. Exposing APIs for document retrieval and search
4. Supporting document chunking for context window management

## License

[MIT License](LICENSE)
