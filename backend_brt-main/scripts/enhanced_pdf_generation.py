#!/usr/bin/env python
"""
Enhanced PDF generation script that properly handles PDF files by embedding them
rather than just displaying metadata.
"""

import io
import os
import json
from pathlib import Path
from datetime import datetime
import sys
import tempfile

# PDF generation imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# For PDF merging
try:
    from PyPDF2 import PdfReader, PdfWriter, PdfMerger
    PYPDF2_AVAILABLE = True
except ImportError:
    print("PyPDF2 not installed. PDF embedding will not be available.")
    print("To install: pip install PyPDF2")
    PYPDF2_AVAILABLE = False

def generate_pdf_from_files(file_paths, metadata, output_path=None):
    """
    Generate a PDF file from the provided files and metadata
    This version properly embeds PDF files
    """
    print(f"Generating PDF from {len(file_paths)} files...")
    
    # Separate PDF and non-PDF files
    pdf_files = [f for f in file_paths if Path(f).suffix.lower() == '.pdf']
    other_files = [f for f in file_paths if Path(f).suffix.lower() != '.pdf']
    
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
    if metadata:
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
    
    for i, file_path in enumerate(all_files, 1):
        path = Path(file_path)
        doc_index.append([
            Paragraph(str(i), normal_style),
            Paragraph(path.name, normal_style),
            Paragraph(path.suffix.upper()[1:], normal_style),
            Paragraph(f"{path.stat().st_size:,} bytes", normal_style)
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
    for i, file_path in enumerate(other_files, 1):
        path = Path(file_path)
        elements.append(PageBreak())
        
        # Add file header
        elements.append(Paragraph(f"Document {i + len(pdf_files)}: {path.name}", heading_style))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Add file metadata
        file_info = [
            [Paragraph("<b>Filename</b>", normal_style), Paragraph(path.name, normal_style)],
            [Paragraph("<b>Size</b>", normal_style), Paragraph(f"{path.stat().st_size:,} bytes", normal_style)],
            [Paragraph("<b>Modified</b>", normal_style), Paragraph(datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"), normal_style)]
        ]
        
        file_table = Table(file_info, colWidths=[1.5*inch, 4*inch])
        file_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(file_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # For image files, try to include them
        if path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            try:
                img = Image(str(path))
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
        else:
            # For text files, try to include the content
            if path.suffix.lower() in ['.txt', '.md', '.csv']:
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
            else:
                # For other file types, just show a placeholder
                elements.append(Paragraph(f"This is a {path.suffix} file. Content is not displayed in this preview.", normal_style))
    
    # Build the PDF with non-PDF content
    doc.build(elements)
    
    # Now merge with PDF files if there are any and PyPDF2 is available
    if pdf_files and PYPDF2_AVAILABLE:
        # Create a PDF merger
        merger = PdfMerger()
        
        # Add the temp PDF with metadata and non-PDF content
        merger.append(temp_pdf_path)
        
        # Process each PDF file
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"Embedding PDF: {pdf_path}")
            try:
                # Create a simple cover page for this PDF
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as cover_file:
                    cover_path = cover_file.name
                
                cover_doc = SimpleDocTemplate(cover_path, pagesize=letter,
                                            rightMargin=72, leftMargin=72,
                                            topMargin=72, bottomMargin=72)
                
                cover_elements = []
                path = Path(pdf_path)
                
                # Add file header
                cover_elements.append(Paragraph(f"Document {i}: {path.name}", heading_style))
                cover_elements.append(Spacer(1, 0.1 * inch))
                
                # Add file metadata
                file_info = [
                    [Paragraph("<b>Filename</b>", normal_style), Paragraph(path.name, normal_style)],
                    [Paragraph("<b>Size</b>", normal_style), Paragraph(f"{path.stat().st_size:,} bytes", normal_style)],
                    [Paragraph("<b>Modified</b>", normal_style), Paragraph(datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"), normal_style)]
                ]
                
                file_table = Table(file_info, colWidths=[1.5*inch, 4*inch])
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
        
        # Write the merged PDF
        if output_path:
            with open(output_path, 'wb') as f:
                merger.write(f)
            print(f"PDF saved to: {output_path}")
        else:
            # Create a buffer and write to it
            buffer = io.BytesIO()
            merger.write(buffer)
            pdf_data = buffer.getvalue()
            buffer.close()
        
        # Close the merger
        merger.close()
        
        # Clean up temp file
        os.unlink(temp_pdf_path)
        
        if output_path:
            # Return the file path if output_path is provided
            return output_path
        else:
            # Return the PDF data
            return pdf_data
    else:
        # If no PDFs or PyPDF2 not available, just return the temp PDF
        if output_path:
            # Copy temp file to output path
            with open(temp_pdf_path, 'rb') as src, open(output_path, 'wb') as dst:
                dst.write(src.read())
            # Clean up temp file
            os.unlink(temp_pdf_path)
            print(f"PDF saved to: {output_path}")
            return output_path
        else:
            # Read the temp file into memory
            with open(temp_pdf_path, 'rb') as f:
                pdf_data = f.read()
            # Clean up temp file
            os.unlink(temp_pdf_path)
            return pdf_data

def main():
    # Create output directory if it doesn't exist
    output_dir = Path("pdf_output")
    output_dir.mkdir(exist_ok=True)
    
    # Get input directory from command line or use default
    if len(sys.argv) > 1:
        input_dir = Path(sys.argv[1])
    else:
        input_dir = Path("scripts/test_files")
        print(f"No input directory specified. Using: {input_dir}")
    
    # Check if input directory exists
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: Input directory {input_dir} does not exist or is not a directory")
        return
    
    # Find files
    file_paths = list(input_dir.glob('*.*'))
    if not file_paths:
        print(f"No files found in {input_dir}")
        return
    
    print(f"Found {len(file_paths)} files:")
    for i, path in enumerate(file_paths, 1):
        print(f"{i}. {path.name} ({path.stat().st_size:,} bytes)")
    
    # Sample metadata
    metadata = {
        "organization": "EY Sample",
        "project": "Code Analysis",
        "description": "Collection of process documents",
        "additionalInfo": {
            "priority": "High",
            "department": "Technology",
            "category": "Process Documentation"
        }
    }
    
    # Generate PDF
    output_file = output_dir / f"combined_docs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generate_pdf_from_files(file_paths, metadata, output_file)

if __name__ == "__main__":
    main()
