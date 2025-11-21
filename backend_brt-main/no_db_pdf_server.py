"""
Simple PDF generation server with no database dependencies.
This server will:
1. Accept file uploads and metadata
2. Convert them to a single PDF
3. Return the PDF directly or provide a way to retrieve it
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import tempfile
import os
from pathlib import Path
import json
from datetime import datetime
import io
import uuid
import uvicorn

# PDF generation imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

# For PDF embedding
try:
    from PyPDF2 import PdfReader, PdfWriter, PdfMerger
    PYPDF2_AVAILABLE = True
except ImportError:
    print("PyPDF2 not installed. PDF embedding will not be available.")
    print("Install with: pip install PyPDF2")
    PYPDF2_AVAILABLE = False

app = FastAPI(
    title="No-DB PDF Server",
    description="Process uploaded files into a PDF without any database storage"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for PDFs (instead of DB)
# This will be lost when the server restarts
PDF_STORAGE = {}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "No-DB PDF Server", "status": "online"}

@app.post("/process-pdf")
async def process_pdf(
    files: list[UploadFile] = File(...),
    metadata: str = Form(...),
):
    """
    Process uploaded files into a single PDF without any database storage.
    Returns the PDF directly in the response or provides a token to retrieve it.
    """
    try:
        # Parse metadata
        metadata_dict = json.loads(metadata)
        
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Process each uploaded file
            processed_files = []
            for file in files:
                # Save the file to the temporary directory
                file_path = temp_dir_path / file.filename
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                
                # Extract file information
                file_info = {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "path": str(file_path),
                    "size": os.path.getsize(file_path)
                }
                
                # Add file info to processed files list
                processed_files.append(file_info)
            
            # Generate PDF from the uploaded files
            pdf_data = await generate_pdf_from_uploads(processed_files, metadata_dict)
            
            # Generate a unique token for this batch
            batch_token = str(uuid.uuid4())
            
            # Store the PDF in memory
            PDF_STORAGE[batch_token] = {
                "pdf_data": pdf_data,
                "metadata": metadata_dict,
                "files": [{"filename": f["filename"], "size": f["size"]} for f in processed_files],
                "created_at": datetime.now().isoformat()
            }
            
            # Return information about the PDF
            return {
                "batch_token": batch_token,
                "file_count": len(processed_files),
                "total_size": sum(file["size"] for file in processed_files),
                "files": [f["filename"] for f in processed_files],
                "message": "Files processed successfully. Use the retrieve-pdf endpoint to get the PDF."
            }
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid metadata format. Expected valid JSON.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

@app.get("/retrieve-pdf/{batch_token}")
async def retrieve_pdf(batch_token: str):
    """
    Retrieve a PDF that was previously processed.
    """
    if batch_token not in PDF_STORAGE:
        raise HTTPException(status_code=404, detail="PDF not found. It may have expired or been removed.")
    
    pdf_data = PDF_STORAGE[batch_token]["pdf_data"]
    
    return StreamingResponse(
        io.BytesIO(pdf_data),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=combined_document_{batch_token}.pdf"
        }
    )

@app.post("/send-to-llm/{batch_token}")
async def send_to_llm(batch_token: str):
    """
    Simulate sending the PDF to an LLM endpoint.
    In a real implementation, this would call your actual LLM service.
    """
    if batch_token not in PDF_STORAGE:
        raise HTTPException(status_code=404, detail="PDF not found. It may have expired or been removed.")
    
    pdf_data = PDF_STORAGE[batch_token]["pdf_data"]
    metadata = PDF_STORAGE[batch_token]["metadata"]
    
    # This is a placeholder for the actual LLM call
    llm_response = {
        "batch_token": batch_token,
        "analysis": {
            "summary": "This is a placeholder summary that would be generated by the LLM.",
            "key_points": [
                "Key point 1 from the combined document",
                "Key point 2 from the combined document"
            ],
            "recommendations": [
                "Recommendation 1 based on document analysis",
                "Recommendation 2 based on document analysis"
            ]
        },
        "metadata": metadata,
        "pdf_size": len(pdf_data),
        "message": "PDF successfully processed by LLM."
    }
    
    return JSONResponse(content=llm_response)

async def generate_pdf_from_uploads(files, metadata):
    """
    Generate a PDF from the uploaded files and metadata.
    Uses PyPDF2 to properly embed PDF files.
    """
    # Separate PDF and non-PDF files
    pdf_files = [f for f in files if f["content_type"] == "application/pdf" or f["filename"].endswith(".pdf")]
    other_files = [f for f in files if f["content_type"] != "application/pdf" and not f["filename"].endswith(".pdf")]
    
    # Create a temporary file for the non-PDF content
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        temp_pdf_path = tmp_file.name
    
    # Create a PDF document for non-PDF content
    doc = SimpleDocTemplate(temp_pdf_path, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Create PDF elements
    elements = []
    
    # Add title
    elements.append(Paragraph("Combined Documents", title_style))
    elements.append(Spacer(1, 0.25 * inch))
    
    # Add metadata section
    elements.append(Paragraph("Metadata", heading_style))
    elements.append(Spacer(1, 0.1 * inch))
    
    # Format metadata
    metadata_items = []
    for key, value in metadata.items():
        if isinstance(value, dict):
            # Handle nested dictionaries
            value_str = "<br/>".join([f"<b>{k}:</b> {v}" for k, v in value.items()])
            metadata_items.append([Paragraph(f"<b>{key}</b>", normal_style), 
                                  Paragraph(value_str, normal_style)])
        else:
            metadata_items.append([Paragraph(f"<b>{key}</b>", normal_style), 
                                  Paragraph(str(value), normal_style)])
    
    # Create a table for the metadata
    if metadata_items:
        metadata_table = Table(metadata_items, colWidths=[1.5*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(metadata_table)
    
    elements.append(Spacer(1, 0.25 * inch))
    
    # List of all documents
    elements.append(Paragraph("Document Index", heading_style))
    elements.append(Spacer(1, 0.1 * inch))
    
    # Create a table for all documents
    all_files = pdf_files + other_files
    doc_index = []
    doc_index.append([
        Paragraph("<b>No.</b>", normal_style),
        Paragraph("<b>Filename</b>", normal_style),
        Paragraph("<b>Type</b>", normal_style),
        Paragraph("<b>Size</b>", normal_style)
    ])
    
    for i, file_info in enumerate(all_files, 1):
        doc_index.append([
            Paragraph(str(i), normal_style),
            Paragraph(file_info["filename"], normal_style),
            Paragraph(file_info["content_type"], normal_style),
            Paragraph(f"{file_info['size']:,} bytes", normal_style)
        ])
    
    index_table = Table(doc_index, colWidths=[0.5*inch, 3*inch, 1*inch, 1.5*inch])
    index_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(index_table)
    
    # Process non-PDF files
    for i, file_info in enumerate(other_files, 1):
        path = file_info["path"]
        filename = file_info["filename"]
        content_type = file_info["content_type"]
        size = file_info["size"]
        
        elements.append(PageBreak())
        
        # Add file header
        elements.append(Paragraph(f"Document {i + len(pdf_files)}: {filename}", heading_style))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Add file metadata
        file_metadata = [
            [Paragraph("<b>Filename</b>", normal_style), Paragraph(filename, normal_style)],
            [Paragraph("<b>Content Type</b>", normal_style), Paragraph(content_type, normal_style)],
            [Paragraph("<b>Size</b>", normal_style), Paragraph(f"{size:,} bytes", normal_style)]
        ]
        
        file_table = Table(file_metadata, colWidths=[1.5*inch, 4*inch])
        file_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(file_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # For text files, try to include the content
        if content_type.startswith("text/") or filename.endswith(".txt") or filename.endswith(".md"):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read(10000)  # Limit to first 10,000 chars
                
                elements.append(Paragraph("<b>File Content:</b>", normal_style))
                elements.append(Spacer(1, 0.1 * inch))
                
                # Split content into paragraphs and add each
                for paragraph in content.split('\n\n'):
                    if paragraph.strip():
                        elements.append(Paragraph(paragraph.replace('\n', '<br/>'), normal_style))
                        elements.append(Spacer(1, 0.05 * inch))
            except Exception as e:
                elements.append(Paragraph(f"Error reading file: {str(e)}", normal_style))
        
        # For image files, try to include them
        elif content_type.startswith("image/"):
            try:
                img = Image(path)
                
                # Scale the image to fit on the page
                img_width, img_height = img.imageWidth, img.imageHeight
                aspect = img_height / float(img_width)
                
                # Set maximum width to 6 inches (accounting for margins)
                max_width = 6 * inch
                # Calculate height based on aspect ratio
                img_width = min(img_width, max_width)
                img_height = img_width * aspect
                
                img.drawWidth = img_width
                img.drawHeight = img_height
                
                elements.append(img)
            except Exception as e:
                elements.append(Paragraph(f"Error including image: {str(e)}", normal_style))
        
        # For other file types, just show a placeholder
        else:
            elements.append(Paragraph(f"This is a {content_type} file. Content is not displayed in this preview.", normal_style))
    
    # Build the PDF
    doc.build(elements)
    
    # Now merge with PDF files if there are any and PyPDF2 is available
    if pdf_files and PYPDF2_AVAILABLE:
        # Create a PDF merger
        merger = PdfMerger()
        
        # Add the temp PDF with metadata and non-PDF content
        merger.append(temp_pdf_path)
        
        # Process each PDF file
        for i, file_info in enumerate(pdf_files, 1):
            pdf_path = file_info["path"]
            filename = file_info["filename"]
            try:
                # Create a simple cover page for this PDF
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as cover_file:
                    cover_path = cover_file.name
                
                cover_doc = SimpleDocTemplate(cover_path, pagesize=letter,
                                            rightMargin=72, leftMargin=72,
                                            topMargin=72, bottomMargin=72)
                
                cover_elements = []
                
                # Add file header
                cover_elements.append(Paragraph(f"Document {i}: {filename}", heading_style))
                cover_elements.append(Spacer(1, 0.1 * inch))
                
                # Add file metadata
                file_metadata = [
                    [Paragraph("<b>Filename</b>", normal_style), Paragraph(filename, normal_style)],
                    [Paragraph("<b>Content Type</b>", normal_style), Paragraph(file_info["content_type"], normal_style)],
                    [Paragraph("<b>Size</b>", normal_style), Paragraph(f"{file_info['size']:,} bytes", normal_style)]
                ]
                
                file_table = Table(file_metadata, colWidths=[1.5*inch, 4*inch])
                file_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('PADDING', (0, 0), (-1, -1), 6),
                ]))
                cover_elements.append(file_table)
                cover_elements.append(Spacer(1, 0.1 * inch))
                
                cover_elements.append(Paragraph("<b>PDF Content follows on next page</b>", normal_style))
                
                cover_doc.build(cover_elements)
                
                # Add the cover page
                merger.append(cover_path)
                
                # Add the actual PDF
                merger.append(pdf_path)
                
                # Clean up temporary cover file
                os.unlink(cover_path)
                
            except Exception as e:
                print(f"Error processing PDF {pdf_path}: {str(e)}")
        
        # Create a buffer for the merged PDF
        buffer = io.BytesIO()
        merger.write(buffer)
        
        # Get the PDF data
        pdf_data = buffer.getvalue()
        
        # Close resources
        buffer.close()
        merger.close()
        
        # Clean up temp file
        os.unlink(temp_pdf_path)
        
        return pdf_data
    else:
        # If no PDFs or PyPDF2 not available, just return the temp PDF
        with open(temp_pdf_path, 'rb') as f:
            pdf_data = f.read()
        
        # Clean up temp file
        os.unlink(temp_pdf_path)
        
        return pdf_data

if __name__ == "__main__":
    # Create temporary directory for processing
    print("Starting No-DB PDF Server...")
    print(f"PyPDF2 available: {PYPDF2_AVAILABLE}")
    uvicorn.run(app, host="0.0.0.0", port=8080)
