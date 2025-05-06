## python src/main.py

"""
Main
""" 

# Import necessary libraries
import os
from pdf_manager import PDFManager
from note_manager import NoteManager
from database_manager import DatabaseManager
from windows import *

# Main application structure
class ActiveReadingAssistant:
    def __init__(self):
        #self.database_manager = DatabaseManager()  # Initialize DatabaseManager
        self.pdf_manager = PDFManager()
        #self.note_manager = NoteManager(self.database_manager)  # Pass DatabaseManager to NoteManager

    def start(self):
        print("Starting ARA client..")
        Window = ARA()
        Window.mainloop()

# Main entry point
if __name__ == "__main__":
    ara = ActiveReadingAssistant()
    ara.start()