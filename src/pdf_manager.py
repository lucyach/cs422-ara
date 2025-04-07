
'''
PDF Manager Module
manages the loading and parsing of PDF files
It includes methods for loading PDFs, highlighting important sections, and extracting text.
'''

import os
import PyPDF2

class PDFManager: # PDFManager class for managing PDF files
    def __init__(self):
        self.pdf_content = ""

    def load_pdf(self, file_path): # Load a PDF file
        """Load and parse a PDF file."""
        if not os.path.exists(file_path): # Check if the file exists
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, 'rb') as file: # Open the PDF file in binary mode
            reader = PyPDF2.PdfReader(file)
            self.pdf_content = ""
            for page in reader.pages: # Iterate through each page
                self.pdf_content += page.extract_text() + "\n" # Extract text from the page
        return self.pdf_content

    def highlight_sections(self, keywords): # Highlight important sections in the PDF
        """Highlight important sections for the survey phase."""
        highlighted_sections = []
        for line in self.pdf_content.splitlines(): # Split the content into lines
            if any(keyword.lower() in line.lower() for keyword in keywords): # Check if any keyword is in the line
                highlighted_sections.append(line)
        return highlighted_sections