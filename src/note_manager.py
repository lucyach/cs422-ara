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

            result = (
                {"chapter_title": chapter_title, "section_heading": section_heading},
                {"$set": {"notes": updated_notes}}
            )

            self.database_manager.update_data(self.active_pdf, result)
        
            
        else:
            new_note = {
                "chapter_title": chapter_title,
                "section_heading": section_heading,
                "notes": notes
            }
            result = collection.insert_one(new_note)
            self.database_manager.save_data(self.active_pdf, new_note)
            print("New note inserted.")


    def save_note_with_pdf_path(self, chapter_title, section_heading, notes, pdf_path):
        # Always use a string (default to 'N/A' if None)
        pdf_path = pdf_path or "N/A"

        notes_lines = notes.strip().splitlines()
        if notes_lines and pdf_path in notes_lines[0]:
            formatted = notes.strip()
        else:
            formatted = f"{pdf_path}\n{notes.strip()}"

        self.create_note_hierarchy(chapter_title, section_heading, formatted)


    def load_notes(self):
        """Load notes from the database."""
        result = self.database_manager.load_data(self.active_pdf)  # Use database_manager to load data
        return result

    def delete_all_notes(self):
        """Delete all notes and hierarchies from the database."""
        
        self.database_manager.save_data()

    def get_note_labels(self):
        """Return list of formatted note labels: Chapter - Section"""
        notes = self.load_notes()
        return [f"{n['chapter_title']} - {n['section_heading']}" for n in notes]

    def get_note_by_label(self, label):
        """Return note that matches a given label like 'Chapter - Section'"""
        notes = self.load_notes()
        for n in notes:
            if f"{n['chapter_title']} - {n['section_heading']}" == label:
                return n
        return None
    
    def delete_note(self, chapter_title, section_heading):
        """Delete a specific note from the current PDF's MongoDB collection."""
        collection = self.database_manager.db[str(self.active_pdf)]
        result = collection.delete_one({
            "chapter_title": chapter_title,
            "section_heading": section_heading
        })
        print(f"Deleted {result.deleted_count} note(s).")

