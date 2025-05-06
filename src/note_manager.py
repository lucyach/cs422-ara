"""
Note Manager Module
This module manages the creation, saving, and loading of notes.
"""


class NoteManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.active_pdf = "Notes"

    def create_note_hierarchy(self, chapter_title, section_heading, notes):
        """Create or update a hierarchical structure for notes."""
        collection = self.database_manager.db[str(self.active_pdf)]

        # Check if a note for this chapter and section already exists
        existing_entry = collection.find_one({
            "chapter_title": chapter_title,
            "section_heading": section_heading
        })

        if existing_entry:
            current_notes = existing_entry.get("notes", "")
            updated_notes = current_notes + "\n" + notes  # or any delimiter

            result = collection.update_one(
                {"chapter_title": chapter_title, "section_heading": section_heading},
                {"$set": {"notes": updated_notes}}
            )

            print("Note updated with appended content.")
        else:
            new_note = {
                "chapter_title": chapter_title,
                "section_heading": section_heading,
                "notes": notes
            }
            result = collection.insert_one(new_note)
            self.database_manager.save_data(self.active_pdf, new_note)
            print("New note inserted.")


    def save_notes(self, chapter_title, section_heading, notes):
        """Save notes to the database."""
        self.create_note_hierarchy(chapter_title, section_heading, notes)
        print("Notes saved successfully.")

    def load_notes(self):
        """Load notes from the database."""
        result = self.database_manager.load_data(self.active_pdf)  # Use database_manager to load data
        return result

    def delete_all_notes(self):
        """Delete all notes and hierarchies from the database."""
        
        self.database_manager.save_data()

