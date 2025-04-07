## python C:\Users\aches\OneDrive\Desktop\ara\ara\src\main.py

"""
Main
""" 

# Import necessary libraries
import os
from pdf_manager import PDFManager
from note_manager import NoteManager
from cli import CLI  # Corrected import from server to cli
from database_manager import DatabaseManager

# Main application structure
class ActiveReadingAssistant:
    def __init__(self):
        self.database_manager = DatabaseManager()  # Initialize DatabaseManager
        self.pdf_manager = PDFManager()
        self.note_manager = NoteManager(self.database_manager)  # Pass DatabaseManager to NoteManager
        self.cli = CLI()  # Updated to use CLI instead of Server

    def start(self):
        self.cli.run()  # Updated to call the CLI run method

# Main entry point
if __name__ == "__main__":
    ara = ActiveReadingAssistant()
    ara.start()