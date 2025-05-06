'''
PDF Manager Module
Manages the loading and parsing of PDF files.
It includes methods for loading PDFs, rendering pages as images, and extracting text.
'''

import os
import fitz  # PyMuPDF
from PIL import Image

class PDFManager:
    def __init__(self):
        self.pdf_content = "" # Placeholder for PDF content

    def load_pdf(self, file_path):
        """Load and parse a PDF file."""
        if not os.path.exists(file_path): # Check if the file exists
            raise FileNotFoundError(f"The file {file_path} does not exist.") # Raise error if not found

        # Open the PDF file using PyMuPDF
        with fitz.open(file_path) as pdf:
            self.pdf_content = "" # Initialize content variable
            for page in pdf: # Iterate through each page
                self.pdf_content += page.get_text() + "\n" # Extract text from the page
        return self.pdf_content

    def get_page_text(self, file_path, page_number):
        """Extract text from a specific page of the PDF."""
        if not os.path.exists(file_path): # Check if the file exists
            raise FileNotFoundError(f"The file {file_path} does not exist.") # Raise error if not found

        with fitz.open(file_path) as pdf: # Open the PDF file
            if page_number < 0 or page_number >= len(pdf): # Check if the page number is valid
                raise ValueError(f"Page number {page_number} is out of range.") # Raise error if out of range
            return pdf[page_number].get_text() # Extract text from the specified page

    def render_page_as_image(self, file_path, page_number, dpi=100):
        """Render a specific page of the PDF as an image."""
        if not os.path.exists(file_path): # Check if the file exists
            raise FileNotFoundError(f"The file {file_path} does not exist.") # Raise error if not found

        with fitz.open(file_path) as pdf: # Open the PDF file
            if page_number < 0 or page_number >= len(pdf): # Check if the page number is valid
                raise ValueError(f"Page number {page_number} is out of range.") # Raise error if out of range

            # Render the page as a pixmap
            page = pdf[page_number] # Get the specified page
            pix = page.get_pixmap(dpi=dpi) # Render the page as a pixmap with specified DPI

            # Convert the pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples) # Create a PIL Image from the pixmap
            return img