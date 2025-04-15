## python src/main.py

"""
Main
""" 

# Import necessary libraries
import os
from tkinter import *
from pdf_manager import PDFManager
from note_manager import NoteManager
#from cli import CLI  # Corrected import from server to cli
from windows import *
from database_manager import DatabaseManager, User

# Main application structure
class ActiveReadingAssistant:
    def __init__(self):
        self.database_manager = DatabaseManager()  # Initialize DatabaseManager
        self.pdf_manager = PDFManager()
        # Needed to disable note_manager for now. Needs further implementation
        ##self.note_manager = NoteManager(self.database_manager)  # Pass DatabaseManager to NoteManager
        # self.cli = CLI()  # Updated to use CLI instead of Server

        self.user = User() # Initialize the user for local settings and offline mode
        self.userJSON = self.user.LoadUserJSON()

    def start(self):
        # self.cli.run()  # Updated tob call the CLI run method
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()


# Main entry point
if __name__ == "__main__":
    ara = ActiveReadingAssistant()
    ara.start()