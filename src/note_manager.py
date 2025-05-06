"""
Note Manager Module
This module manages the creation, saving, and loading of notes.
"""

class NoteManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager # DatabaseManager instance
        self.active_pdf = "" # Active PDF file name
        #self._initialize_note_hierarchy_table()

    def create_note_hierarchy(self, chapter_title, section_heading, notes):
        """Create or update a hierarchical structure for notes."""
        collection = self.database_manager.db[str(self.active_pdf)] # Get the active PDF collection

        # Check if a note for this chapter and section already exists
        existing_entry = collection.find_one({
            "chapter_title": chapter_title,
            "section_heading": section_heading
        })

        if existing_entry: # Entry exists, update it
            current_notes = existing_entry.get("notes", "") # Get current notes
            updated_notes = current_notes + "\n" + notes  # or any delimiter

            result = collection.update_one( # Update the existing entry
                {"chapter_title": chapter_title, "section_heading": section_heading},
                {"$set": {"notes": updated_notes}}
            )

            print("Note updated with appended content.")
        else: # Entry does not exist, create a new one
            new_note = { # Create a new note entry
                "chapter_title": chapter_title,
                "section_heading": section_heading,
                "notes": notes
            }
            result = collection.insert_one(new_note) # Insert new note
            self.database_manager.save_data(self.active_pdf, new_note) # Save the new note to the database
            print("New note inserted.")


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

    def delete_all_notes(self):
        """Delete all notes and hierarchies from the database."""
        self.database_manager.save_data() # Clear the database collection

    def get_note_labels(self):
        """Return list of formatted note labels: Chapter - Section"""
        notes = self.load_notes() # Load notes from the database
        return [f"{n['chapter_title']} - {n['section_heading']}" for n in notes] # Format labels as 'Chapter - Section'

    def get_note_by_label(self, label):
        """Return note that matches a given label like 'Chapter - Section'"""
        notes = self.load_notes() # Load notes from the database
        for n in notes: # Iterate through notes
            if f"{n['chapter_title']} - {n['section_heading']}" == label: # Check if label matches
                return n
        return None
    
    def delete_note(self, chapter_title, section_heading):
        """Delete a single note based on chapter and section."""
        query = """
        DELETE FROM note_hierarchy
        WHERE chapter_title = :chapter_title AND section_heading = :section_heading
        """
        self.database_manager.save_data(query, { # Delete note from the database
            "chapter_title": chapter_title,
            "section_heading": section_heading
        })
        print(f"Deleted note: Chapter '{chapter_title}', Section '{section_heading}'")


