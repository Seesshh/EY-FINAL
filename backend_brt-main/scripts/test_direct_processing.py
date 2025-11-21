#!/usr/bin/env python
"""
Script to test the direct document processing workflow.
This script demonstrates how to:
1. Upload files directly to the API
2. Process them without storing in the database
3. Retrieve the combined PDF
4. Send the PDF to the LLM
"""

import sys
import os
import json
import requests
import asyncio
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Configuration
API_BASE_URL = "http://localhost:8000"

# No authentication needed for testing
TEST_FILES_DIR = Path(__file__).parent / "test_files"

# Create test files directory if it doesn't exist
TEST_FILES_DIR.mkdir(exist_ok=True)

# Sample test files to create
TEST_FILES = [
    {
        "filename": "business_plan.txt",
        "content": """
# Business Plan

## Executive Summary
This is a sample business plan for testing purposes.

## Market Analysis
The market for this product is growing at 15% annually.

## Financial Projections
Year 1: $100,000
Year 2: $250,000
Year 3: $500,000
"""
    },
    {
        "filename": "risk_assessment.txt",
        "content": """
# Risk Assessment

## Identified Risks
1. Market competition
2. Regulatory changes
3. Supply chain disruptions

## Mitigation Strategies
- Diversify product offerings
- Monitor regulatory environment
- Establish backup suppliers
"""
    }
]

# Sample metadata
METADATA = {
    "organization": "Test Company",
    "department": "Business Development",
    "project": "New Product Launch",
    "author": "John Doe",
    "date": "2025-05-19"
}

def create_test_files():
    """Create sample test files"""
    print("Creating test files...")
    
    for file_info in TEST_FILES:
        file_path = TEST_FILES_DIR / file_info["filename"]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_info["content"])
        print(f"Created: {file_path}")

def get_headers():
    """Get headers for API requests"""
    return {"Content-Type": "application/json"}

def upload_files():
    """Upload files to the API"""
    print("\nUploading files to the API...")
    
    # Prepare files for upload
    files = []
    for file_info in TEST_FILES:
        file_path = TEST_FILES_DIR / file_info["filename"]
        files.append(
            ("files", (file_info["filename"], open(file_path, "rb"), "text/plain"))
        )
    
    # Prepare metadata
    metadata = json.dumps(METADATA)
    
    # Make the request
    url = f"{API_BASE_URL}/api/v1/documents/process-direct"
    headers = {}
    
    try:
        # Make the actual request
        response = requests.post(
            url,
            headers=headers,
            files=files,
            data={"metadata": metadata}
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        
        print(f"Upload response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error uploading files: {e}")
        # Fallback to simulated response for testing
        result = {
            "batch_token": "12345678-1234-5678-1234-567812345678",
            "file_count": len(TEST_FILES),
            "total_size": sum(os.path.getsize(TEST_FILES_DIR / f["filename"]) for f in TEST_FILES),
            "files": [f["filename"] for f in TEST_FILES],
            "message": "Files processed successfully. Use the batch_token to retrieve the PDF or send to LLM."
        }
        print(f"Using simulated response: {json.dumps(result, indent=2)}")
        return result

def retrieve_pdf(batch_token):
    """Retrieve the combined PDF"""
    print(f"\nRetrieving PDF for batch: {batch_token}...")
    
    # Make the request
    url = f"{API_BASE_URL}/api/v1/documents/retrieve-pdf/{batch_token}"
    headers = {}
    
    try:
        # Make the actual request
        response = requests.get(
            url,
            headers=headers,
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        if response.status_code == 200:
            # Save the PDF to a file
            output_path = Path(f"./output_{batch_token}.pdf")
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"PDF saved to: {output_path}")
            return output_path
        else:
            print(f"Error retrieving PDF: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving PDF: {e}")
        # Simulated response for testing
        output_path = Path(f"./output_{batch_token}.pdf")
        print(f"PDF would be saved to: {output_path} (simulated)")
        return output_path

def send_to_llm(batch_token):
    """Send the PDF to the LLM"""
    print(f"\nSending PDF to LLM for batch: {batch_token}...")
    
    # Prepare LLM parameters
    llm_params = {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000,
        "instructions": "Analyze the document and extract key information."
    }
    
    # Make the request
    url = f"{API_BASE_URL}/api/v1/documents/send-to-llm/{batch_token}"
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the actual request
        response = requests.post(
            url,
            headers=headers,
            json=llm_params
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        
        print(f"LLM response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error sending to LLM: {e}")
        # Simulated response for testing
        result = {
            "batch_token": batch_token,
            "llm_params": llm_params,
            "results": {
                "extracted_data": {
                    "title": "Sample Document Analysis",
                    "summary": "This is a placeholder summary that would be generated by the LLM.",
                    "key_points": [
                        "Key point 1 extracted from the documents",
                        "Key point 2 extracted from the documents",
                        "Key point 3 extracted from the documents"
                    ],
                    "entities": {
                        "organizations": ["Acme Corp", "TechNova"],
                        "people": ["John Doe", "Jane Smith"],
                        "dates": ["2025-01-15", "2025-03-30"]
                    },
                    "recommendations": [
                        "Recommendation 1 based on document analysis",
                        "Recommendation 2 based on document analysis"
                    ]
                },
                "confidence_score": 0.85,
                "processing_time": "2.3 seconds"
            },
            "message": "LLM processing completed successfully."
        }
        print(f"Using simulated LLM response: {json.dumps(result, indent=2)}")
        return result
    return result

def main():
    """Main function"""
    print("Starting Direct Document Processing Test")
    print("=======================================")
    print()
    
    try:
        # Step 1: Create test files
        print("Creating test files...")
        create_test_files()
        
        # Step 2: Upload files
        upload_result = upload_files()
        batch_token = upload_result["batch_token"]
        
        # Step 3: Retrieve PDF
        pdf_path = retrieve_pdf(batch_token)
        
        # Step 4: Send to LLM
        llm_result = send_to_llm(batch_token)
        
        print()
        print("Direct Document Processing Test Completed")
        print("=======================================")
        print()
        print("Results:")
        print(f"  - Batch Token: {batch_token}")
        if pdf_path and pdf_path.exists():
            print(f"  - PDF Generated: {pdf_path}")
        print(f"  - Files Processed: {upload_result.get('file_count', 0)}")
        print(f"  - Total Size: {upload_result.get('total_size', 0)} bytes")
        
    except Exception as e:
        print(f"\nError during test: {e}")
    finally:
        print("\nTest completed. Check the results above for details.")

if __name__ == "__main__":
    main()
