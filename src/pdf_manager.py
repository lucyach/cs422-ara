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
        self.pdf_content = ""

    def load_pdf(self, file_path):
        """Load and parse a PDF file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Open the PDF file using PyMuPDF
        with fitz.open(file_path) as pdf:
            self.pdf_content = ""
            for page in pdf:
                self.pdf_content += page.get_text() + "\n"
        return self.pdf_content

    def get_page_text(self, file_path, page_number):
        """Extract text from a specific page of the PDF."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with fitz.open(file_path) as pdf:
            if page_number < 0 or page_number >= len(pdf):
                raise ValueError(f"Page number {page_number} is out of range.")
            return pdf[page_number].get_text()

    def render_page_as_image(self, file_path, page_number, dpi=100):
        """Render a specific page of the PDF as an image."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with fitz.open(file_path) as pdf:
            if page_number < 0 or page_number >= len(pdf):
                raise ValueError(f"Page number {page_number} is out of range.")

            # Render the page as a pixmap
            page = pdf[page_number]
            pix = page.get_pixmap(dpi=dpi)

            # Convert the pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return img