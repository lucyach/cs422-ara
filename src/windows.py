import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from pdf_manager import PDFManager
from note_manager import NoteManager
from database_manager import DatabaseManager


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Active Reading Assistant")
        self.root.geometry("800x600")

        # Initialize managers
        self.database_manager = DatabaseManager()
        self.pdf_manager = PDFManager()
        self.note_manager = NoteManager(self.database_manager)

        # Create frames for layout
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.note_frame = tk.Frame(self.root, bg="lightgray")
        self.note_frame.grid(row=1, column=0, sticky="nsew")

        self.pdf_frame = tk.Frame(self.root, bg="white")
        self.pdf_frame.grid(row=1, column=1, sticky="nsew")

        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Add buttons to the top frame
        tk.Button(self.button_frame, text="1. Load PDF", command=self.load_pdf, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="2. SQ3R", command=self.sq3r, width=20).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="3. Create Note Hierarchy", command=self.create_note_hierarchy, width=20).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="4. Save Notes", command=self.save_notes, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="5. Load Notes", command=self.load_notes, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="6. Delete All Notes", command=self.delete_all_notes, width=20).pack(side="left", padx=5, pady=5)

        # Add widgets to the note-taking frame
        tk.Label(self.note_frame, text="Notes", font=("Arial", 14), bg="lightgray").pack(pady=5)

        # Add input boxes for chapter and section
        chapter_frame = tk.Frame(self.note_frame, bg="lightgray")
        chapter_frame.pack(pady=5, padx=10, fill="x")
        tk.Label(chapter_frame, text="Chapter:", bg="lightgray").pack(side="left", padx=5)
        self.chapter_entry = tk.Entry(chapter_frame, width=30)
        self.chapter_entry.pack(side="left", padx=5)

        section_frame = tk.Frame(self.note_frame, bg="lightgray")
        section_frame.pack(pady=5, padx=10, fill="x")
        tk.Label(section_frame, text="Section:", bg="lightgray").pack(side="left", padx=5)
        self.section_entry = tk.Entry(section_frame, width=30)
        self.section_entry.pack(side="left", padx=5)

        # Add the note-taking text box
        self.note_text = tk.Text(self.note_frame, wrap="word", height=20)
        self.note_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Add widgets to the PDF display frame
        tk.Label(self.pdf_frame, text="PDF Viewer", font=("Arial", 14), bg="white").pack(pady=10)
        self.pdf_display = tk.Text(self.pdf_frame, wrap="word", height=20, state="disabled", bg="white")
        self.pdf_display.pack(expand=True, fill="both", padx=10, pady=10)


    def load_pdf(self):
        """Load a PDF file."""
        file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                pdf_content = self.pdf_manager.load_pdf(file_path)
                self.pdf_display.config(state="normal")
                self.pdf_display.delete("1.0", "end")
                self.pdf_display.insert("1.0", pdf_content)
                self.pdf_display.config(state="disabled")
                messagebox.showinfo("Success", "PDF loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def highlight_sections(self):
        """Highlight important sections in the PDF."""
        keywords = simpledialog.askstring("Highlight Sections", "Enter keywords (comma-separated):")
        if keywords:
            highlighted = self.pdf_manager.highlight_sections(keywords.split(","))
            if highlighted:
                self.pdf_display.config(state="normal")
                self.pdf_display.delete("1.0", "end")
                self.pdf_display.insert("1.0", "\n".join(highlighted))
                self.pdf_display.config(state="disabled")
                messagebox.showinfo("Highlighted Sections", "Highlighted sections displayed.")
            else:
                messagebox.showinfo("Highlighted Sections", "No matches found.")

    def create_note_hierarchy(self):
        """Prepare the note-taking area for entering chapter and section information."""
        # Clear the note-taking area
        self.note_text.delete("1.0", "end")

        messagebox.showinfo("Create Note Hierarchy", "Please enter the chapter title, section heading, and notes in the note-taking area.")
        


    def save_notes(self):
        """Save notes to the database."""
        # Get the chapter and section from the input boxes
        chapter_title = self.chapter_entry.get().strip()
        section_heading = self.section_entry.get().strip()
        notes = self.note_text.get("1.0", "end").strip()  # Get the content of the note-taking area

        if not chapter_title:
            messagebox.showwarning("Warning", "Chapter title cannot be empty.")
            return

        if not section_heading:
            messagebox.showwarning("Warning", "Section heading cannot be empty.")
            return

        if not notes:
            messagebox.showwarning("Warning", "The note-taking area is empty. Nothing to save.")
            return

        # Save the notes to the database
        self.note_manager.create_note_hierarchy(chapter_title, section_heading, notes)
        messagebox.showinfo("Success", "Notes saved successfully.")



    def load_notes(self):
        """Load notes from the database.
        Loads all notes taken."""
        notes = self.note_manager.load_notes()
        if notes:
            # Format and display all notes in the note-taking text box
            notes_display = "\n\n".join(
                f"Chapter: {row['chapter_title']}\nSection: {row['section_heading']}\nNotes: {row['notes']}"
                for row in notes
            )
            self.note_text.delete("1.0", "end")  # Clear the note-taking area
            self.note_text.insert("1.0", notes_display)  # Insert loaded notes
            messagebox.showinfo("Loaded Notes", "Notes loaded into the note-taking area.")
        else:
            self.note_text.delete("1.0", "end")  # Clear the note-taking area
            messagebox.showinfo("Loaded Notes", "No notes found.")
    
    def delete_all_notes(self):
        """Delete all notes and hierarchies."""
        if messagebox.askyesno("Delete All Notes", "Are you sure you want to delete all notes and hierarchies?"):
            self.note_manager.delete_all_notes()
            self.note_text.delete("1.0", "end")  # Clear the note-taking area
            messagebox.showinfo("Success", "All notes and hierarchies have been deleted.")

    def sq3r(self):
        """Perform the SQ3R method."""
        # Step 1: Survey
        

        # Step 2: Question
        

        # Step 3: Read
        

        # Step 4: Recite
        

        # Step 5: Review
        


# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()