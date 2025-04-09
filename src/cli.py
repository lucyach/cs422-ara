'''
CLI: command-line interface
'''
import tkinter as tk
from tkinter import ttk # For themed widgets

import sys
from pdf_manager import PDFManager
from note_manager import NoteManager
from database_manager import DatabaseManager


class CLI:
    def __init__(self):  # Initialization of the CLI class
        self.database_manager = DatabaseManager()
        self.pdf_manager = PDFManager()
        self.note_manager = NoteManager(self.database_manager)

    def display_menu(self):  # Display the main menu
        print("Welcome to the Active Reading Assistant")
        print("1. Load PDF")
        print("2. Highlight Sections")
        print("3. Create Note Hierarchy")
        print("4. Save Notes")
        print("5. Load Notes")
        print("6. Exit")

    def load_pdf(self):  # Load a PDF file
        file_path = input("Enter the path to the PDF file: ")
        self.pdf_manager.load_pdf(file_path)
        print("PDF loaded successfully.")

    def highlight_sections(self):  # Highlight important sections in the PDF
        keywords = input("Enter keywords to highlight (comma-separated): ").split(",")
        highlighted_content = self.pdf_manager.highlight_sections(keywords)
        print("Highlighted sections:")
        for section in highlighted_content:
            print(section)

    def create_note_hierarchy(self):  # Create a hierarchical structure for notes
        chapter_title = input("Enter chapter title: ")
        section_heading = input("Enter section heading: ")
        self.note_manager.create_note_hierarchy(chapter_title, section_heading)

    def save_notes(self):  # Save notes
        notes = input("Enter notes to save: ")
        self.note_manager.save_notes(notes)

    def load_notes(self):  # Load notes
        notes = self.note_manager.load_notes()
        print("Loaded notes:")
        for note in notes:
            print(f"{note.id}: {note.content}")

    def run(self):  # Main loop for the CLI
        while True:
            self.display_menu()
            choice = input("Choose an option: ")
            if choice == '1':
                self.load_pdf()
            elif choice == '2':
                self.highlight_sections()
            elif choice == '3':
                self.create_note_hierarchy()
            elif choice == '4':
                self.save_notes()
            elif choice == '5':
                self.load_notes()
            elif choice == '6':
                print("Exiting the application.")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")