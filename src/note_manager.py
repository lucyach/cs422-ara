"""
Note Manager Module
This module manages the creation, saving, and loading of notes.
"""

class NoteManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self._initialize_note_hierarchy_table()

    def _initialize_note_hierarchy_table(self):
        """Ensure the database has the required table for note hierarchy."""
        query = """
        CREATE TABLE IF NOT EXISTS note_hierarchy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_title TEXT NOT NULL,
            section_heading TEXT NOT NULL,
            notes TEXT NOT NULL
        )
        """
        self.database_manager.save_data(query, {})

    def create_note_hierarchy(self, chapter_title, section_heading, notes):
        """Create or update a hierarchical structure for notes."""
        # Check if the hierarchy already exists
        query_check = """
        SELECT id FROM note_hierarchy
        WHERE chapter_title = :chapter_title AND section_heading = :section_heading
        """
        existing_entry = self.database_manager.load_data(query_check, {
            "chapter_title": chapter_title,
            "section_heading": section_heading
        })

        if existing_entry:
            # Update the existing entry
            query_update = """
            UPDATE note_hierarchy
            SET notes = :notes
            WHERE chapter_title = :chapter_title AND section_heading = :section_heading
            """
            self.database_manager.save_data(query_update, {
                "chapter_title": chapter_title,
                "section_heading": section_heading,
                "notes": notes
            })
            print(f"Note hierarchy updated: Chapter '{chapter_title}', Section '{section_heading}'")
        else:
            # Insert a new entry
            query_insert = """
            INSERT INTO note_hierarchy (chapter_title, section_heading, notes)
            VALUES (:chapter_title, :section_heading, :notes)
            """
            self.database_manager.save_data(query_insert, {
                "chapter_title": chapter_title,
                "section_heading": section_heading,
                "notes": notes
            })
            print(f"Note hierarchy created: Chapter '{chapter_title}', Section '{section_heading}'")

    def save_notes(self, chapter_title, section_heading, notes):
        """Save notes to the database."""
        self.create_note_hierarchy(chapter_title, section_heading, notes)
        print("Notes saved successfully.")

    def load_notes(self):
        """Load notes from the database."""
        query = "SELECT chapter_title, section_heading, notes FROM note_hierarchy"
        result = self.database_manager.load_data(query)  # Use database_manager to load data
        print("Loaded notes:")
        for row in result:
            # Access rows as dictionaries
            print(f"Chapter: {row['chapter_title']}, Section: {row['section_heading']}, Notes: {row['notes']}")
        return result

    def save_notes(self):
        """Save notes to the database, prompting for hierarchy if necessary."""
        chapter_title = input("Enter the chapter title: ")
        section_heading = input("Enter the section heading: ")
        notes = input("Enter notes to save: ")
        self.note_manager.create_note_hierarchy(chapter_title, section_heading, notes)
        print("Notes saved successfully.")

    def delete_all_notes(self):
        """Delete all notes and hierarchies from the database."""
        query = "DELETE FROM note_hierarchy"
        self.database_manager.save_data(query, {})
        print("All notes and hierarchies have been deleted.")

