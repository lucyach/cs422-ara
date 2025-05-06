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

        self.pdf_manager = PDFManager() # Initialize PDFManager

    def start(self): # Start the application

        print("Starting ARA client..")
        Window = ARA() # Initialize the main window
        Window.mainloop() # Start the main loop

# Main entry point
if __name__ == "__main__":
    ara = ActiveReadingAssistant()
    ara.start()