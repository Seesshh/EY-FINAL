# Testing the Business Resilience Tool API

This guide explains how to generate test data and use Postman to test your Business Resilience Tool API.

## Step 1: Generate Test Data

The `generate_test_data.py` script creates sample organizations, users, and documents in both PostgreSQL and MongoDB.

Run the script:

```bash
cd c:\Users\ayush\OneDrive\Documents\ey_cat
python scripts/generate_test_data.py
```

This will create:
- 3 organizations (Acme Corporation, TechNova Solutions, FinSecure Bank)
- 4 users (one admin for each organization, plus a manager)
- 5 documents of different types (policies, plans, diagrams, etc.)

## Step 2: Start the FastAPI Server

Start your FastAPI application:

```bash
cd c:\Users\ayush\OneDrive\Documents\ey_cat
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Step 3: Import Postman Collection

1. Open Postman
2. Click "Import" button
3. Select the file: `c:\Users\ayush\OneDrive\Documents\ey_cat\scripts\Business_Resilience_Tool_API.postman_collection.json`
4. Click "Import"

## Step 4: Set Up Environment Variables

Create a new environment in Postman:

1. Click the gear icon (⚙️) in the top right
2. Click "Add" to create a new environment
3. Name it "Business Resilience Tool"
4. Add these variables:
   - `base_url`: `http://localhost:8000/api/v1`
   - `access_token`: (leave empty, will be auto-filled)
   - `organization_id`: (leave empty for now)
   - `document_id`: (leave empty for now)
5. Click "Save"
6. Select your new environment from the dropdown in the top right

## Step 5: Test the API

Follow this testing sequence:

### 1. Authentication

1. Execute the "Login" request to get an access token
   - Use credentials: `admin@acme.com` / `password123`
   - The token will be automatically saved to the `access_token` variable

### 2. Organizations

1. Execute "Get Organizations" to see the list of organizations
2. Copy an organization ID and set it as the `organization_id` variable in your environment

### 3. Users

1. Execute "Get Users" to see the list of users
2. Execute "Get Current User" to see your own user information

### 4. Documents

1. Execute "Get Documents" to see the list of documents
2. Copy a document ID and set it as the `document_id` variable in your environment
3. Execute "Get Document by ID" to see document metadata
4. Execute "Get Document Content" to see the document content from MongoDB
5. Try "Search Documents" to search for documents

## Test User Credentials

You can use these test users to login:

| Email | Password | Role |
|-------|----------|------|
| admin@acme.com | password123 | Admin |
| manager@acme.com | password123 | Manager |
| admin@technova.com | password123 | Admin |
| admin@finsecure.com | password123 | Admin |

## API Documentation

You can also access the Swagger UI documentation at:

http://localhost:8000/docs

This provides an interactive interface to test all API endpoints directly in your browser.

## Creating New Data

You can use the Postman collection to create new:
- Organizations
- Users
- Documents

Just use the corresponding POST requests and modify the JSON body as needed.
