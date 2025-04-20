
'''
PDF Manager Module
manages the loading and parsing of PDF files
It includes methods for loading PDFs, highlighting important sections, and extracting text.
'''

import os
import PyPDF2

class PDFManager:
    def __init__(self):
        self.pdf_content = ""

    def load_pdf(self, file_path):
        """Load and parse a PDF file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            self.pdf_content = ""
            for page in reader.pages:
                self.pdf_content += page.extract_text() + "\n"
        return self.pdf_content

    def get_page_text(self, file_path, page_number):
        """Extract text from a specific page of the PDF."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if page_number < 0 or page_number >= len(reader.pages):
                raise ValueError(f"Page number {page_number} is out of range.")
            return reader.pages[page_number].extract_text()
        