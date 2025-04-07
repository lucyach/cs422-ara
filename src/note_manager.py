"""
Note Manager Module
This module manages the creation, saving, and loading of notes.
"""

class NoteManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def create_note_hierarchy(self, chapter_title, section_heading):  # Create a hierarchical structure for notes
        """Create a hierarchical structure for notes."""
        print(f"Note hierarchy created: Chapter '{chapter_title}', Section '{section_heading}'")

    def save_notes(self, notes):
        """Save notes to the database."""
        query = "INSERT INTO notes (content) VALUES (:content)"
        print(f"Saving note: {notes}")  # Debug print
        self.database_manager.save_data(query, {"content": notes})
        print("Notes saved successfully.")

    def load_notes(self):
        """Load notes from the database."""
        query = "SELECT id, content FROM notes"
        result = self.database_manager.load_data(query)
        print(f"Loaded notes: {result}")  # Debug print
        return result