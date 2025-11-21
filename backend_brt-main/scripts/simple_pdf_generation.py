#!/usr/bin/env python
"""
Simple PDF generation script to demonstrate combining multiple documents into one PDF.
"""

import io
import os
import json
from pathlib import Path
from datetime import datetime
import sys

# PDF generation imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def generate_pdf_from_files(file_paths, metadata, output_path=None):
    """
    Generate a PDF file from the provided files and metadata
    """
    print(f"Generating PDF from {len(file_paths)} files...")
    
    # Create a PDF buffer
    buffer = io.BytesIO()
    
    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter,
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
    
    # Process each file
    for i, file_path in enumerate(file_paths, 1):
        path = Path(file_path)
        elements.append(PageBreak())
        
        # Add file header
        elements.append(Paragraph(f"Document {i}: {path.name}", heading_style))
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
        
        # For this simple example, we'll just include text content or image representation
        # In a real implementation, you might want to use more advanced PDF manipulation libraries
        # to include the actual document contents
        
        # If it's an image file, try to include it
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
                        
                    elements.append(Paragraph("<b>File Content Preview:</b>", normal_style))
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
    
    # Build the PDF
    doc.build(elements)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # If output path is provided, save the PDF
    if output_path:
        output_file = Path(output_path)
        with open(output_file, 'wb') as f:
            f.write(pdf_data)
        print(f"PDF saved to: {output_file}")
    
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
