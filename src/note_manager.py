"""
Note Manager Module
This module manages the creation, saving, and loading of notes.
"""

import os

class NoteManager:
    def __init__(self, database_manager):

        self.database_manager = database_manager
        self.active_pdf = "Notes"
        self.offline_mode = False

    def initialize_note_folder(self):

        parent_dir = os.path.join(os.getcwd(), '..')
        folder_path = os.path.join(parent_dir, 'notes')
        folder_path = os.path.abspath(folder_path)

        os.makedirs(folder_path, exist_ok=True)



    def create_note_hierarchy(self, chapter_title, section_heading, notes):
        """Create or update a hierarchical structure for notes."""
        collection = self.database_manager.db[str(self.active_pdf)] # Get the active PDF collection

        # Check if a note for this chapter and section already exists
        existing_entry = collection.find_one({
            "chapter_title": chapter_title,
            "section_heading": section_heading
        })


        if existing_entry:
            current_notes = existing_entry.get("notes", "")
            updated_notes = notes  

            filter_query = {"chapter_title": chapter_title, "section_heading": section_heading}
            update_fields = {"notes": updated_notes}


            if self.offline_mode:
                print("offlinesaving")
            else:
                self.database_manager.update_data(self.active_pdf, filter_query, update_fields)

        else:
            new_note = {

                "chapter_title": chapter_title,
                "section_heading": section_heading,
                "notes": notes
            }

            self.database_manager.save_data(self.active_pdf, new_note)
            print("New note inserted")



    def save_note_with_pdf_path(self, chapter_title, section_heading, notes, pdf_path): # pdf_path is optional
        # Always use a string (default to 'N/A' if None)
        pdf_path = pdf_path or "N/A" # Ensure pdf_path is a string

        notes_lines = notes.strip().splitlines() # Split notes into lines
        if notes_lines and pdf_path in notes_lines[0]: # Check if pdf_path is already in the first line of notes
            formatted = notes.strip() # Keep the notes as is
        else:
            formatted = f"{pdf_path}\n{notes.strip()}" # Prepend pdf_path to notes

        self.create_note_hierarchy(chapter_title, section_heading, formatted) # Create or update the note hierarchy


    def load_notes(self):
        """Load notes from the database."""
        result = self.database_manager.load_data(self.active_pdf)  # Use database_manager to load data
        return result


    def delete_note(self, chapter_title, section_heading):
        """Delete a specific note from the current PDF's MongoDB collection."""
        collection = self.database_manager.db[str(self.active_pdf)]
        result = collection.delete_one({
            "chapter_title": chapter_title,
            "section_heading": section_heading
        })
        print(f"Deleted {result.deleted_count} note(s).")

