import tkinter as tk
from tkinter import messagebox
from pdf_manager import PDFManager
from note_manager import NoteManager
from database_manager import DatabaseManager


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Active Reading Assistant")
        self.root.geometry("400x400")

        # Initialize managers
        self.database_manager = DatabaseManager()
        self.pdf_manager = PDFManager()
        self.note_manager = NoteManager(self.database_manager)

        # Add buttons for each menu option
        tk.Label(self.root, text="Active Reading Assistant", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="1. Load PDF", command=self.load_pdf, width=30).pack(pady=5)
        tk.Button(self.root, text="2. Highlight Sections", command=self.highlight_sections, width=30).pack(pady=5)
        tk.Button(self.root, text="3. Create Note Hierarchy", command=self.create_note_hierarchy, width=30).pack(pady=5)
        tk.Button(self.root, text="4. Save Notes", command=self.save_notes, width=30).pack(pady=5)
        tk.Button(self.root, text="5. Load Notes", command=self.load_notes, width=30).pack(pady=5)
        tk.Button(self.root, text="6. Delete All Notes", command=self.delete_all_notes, width=30).pack(pady=5)

    def load_pdf(self):
        """Load a PDF file."""
        file_path = tk.filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                self.pdf_manager.load_pdf(file_path)
                messagebox.showinfo("Success", "PDF loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def highlight_sections(self):
        """Highlight important sections in the PDF."""
        keywords = tk.simpledialog.askstring("Highlight Sections", "Enter keywords (comma-separated):")
        if keywords:
            highlighted = self.pdf_manager.highlight_sections(keywords.split(","))
            messagebox.showinfo("Highlighted Sections", "\n".join(highlighted) if highlighted else "No matches found.")

    def create_note_hierarchy(self):
        """Create a hierarchical structure for notes."""
        chapter_title = tk.simpledialog.askstring("Create Note Hierarchy", "Enter chapter title:")
        section_heading = tk.simpledialog.askstring("Create Note Hierarchy", "Enter section heading:")
        if chapter_title and section_heading:
            self.note_manager.create_note_hierarchy(chapter_title, section_heading, "")
            messagebox.showinfo("Success", "Note hierarchy created.")

    def save_notes(self):
        """Save notes to the database."""
        chapter_title = tk.simpledialog.askstring("Save Notes", "Enter chapter title:")
        section_heading = tk.simpledialog.askstring("Save Notes", "Enter section heading:")
        notes = tk.simpledialog.askstring("Save Notes", "Enter notes:")
        if chapter_title and section_heading and notes:
            self.note_manager.create_note_hierarchy(chapter_title, section_heading, notes)
            messagebox.showinfo("Success", "Notes saved successfully.")

    def load_notes(self):
        """Load notes from the database."""
        notes = self.note_manager.load_notes()
        if notes:
            notes_display = "\n".join(
                f"Chapter: {row['chapter_title']}, Section: {row['section_heading']}, Notes: {row['notes']}"
                for row in notes
            )
            messagebox.showinfo("Loaded Notes", notes_display)
        else:
            messagebox.showinfo("Loaded Notes", "No notes found.")

    def delete_all_notes(self):
        """Delete all notes and hierarchies."""
        if messagebox.askyesno("Delete All Notes", "Are you sure you want to delete all notes and hierarchies?"):
            self.note_manager.delete_all_notes()
            messagebox.showinfo("Success", "All notes and hierarchies have been deleted.")


# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()