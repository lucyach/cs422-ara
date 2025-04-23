import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from pdf_manager import PDFManager
from note_manager import NoteManager
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk

## from database_manager import DatabaseManager

class ARA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ARA - Active Reading Assistant")
        self.geometry("1000x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (MainMenu, NotesScreen, ServerSetupScreen, AboutScreen):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Make the MainMenu frame expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a container frame that will hold the content
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        # Center container content using another grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(2, weight=1)

        content = tk.Frame(container)
        content.grid(row=1, column=1)

        # Your label and buttons inside content
        label = tk.Label(content, text="Welcome to ARA\nYour Active Reading Assistant", font=("Arial", 20), justify="center")
        label.pack(pady=20)

        tk.Button(content, text="Notes", width=20, command=lambda: controller.show_frame(NotesScreen)).pack(pady=5)
        tk.Button(content, text="Server Setup", width=20, command=lambda: controller.show_frame(ServerSetupScreen)).pack(pady=5)
        tk.Button(content, text="About", width=20, command=lambda: controller.show_frame(AboutScreen)).pack(pady=5)

class NotesScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Initialize managers
        # self.database_manager = DatabaseManager()
        self.pdf_manager = PDFManager()
        # self.note_manager = NoteManager(self.database_manager)

        # Layout frames
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.note_frame = tk.Frame(self, bg="lightgray")
        self.note_frame.grid(row=1, column=0, sticky="nsew")

        self.pdf_frame = tk.Frame(self, bg="white")
        self.pdf_frame.grid(row=1, column=1, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Buttons
        tk.Button(self.button_frame, text="1. Load PDF", command=self.load_pdf, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="2. Create Note Hierarchy", command=self.create_note_hierarchy, width=20).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="3. Save Notes", command=self.save_notes, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="4. Load Notes", command=self.load_notes, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="5. Delete All Notes", command=self.delete_all_notes, width=20).pack(side="left", padx=5, pady=5)

        # SQ3R checkbox
        self.sq3r_enabled = tk.BooleanVar(value=True)
        self.prompt_toggle = tk.Checkbutton(self.button_frame, text="SQ3R Prompts", variable=self.sq3r_enabled, command=self.toggle_prompts)
        self.prompt_toggle.pack(side="left", padx=5, pady=5)

        # Notes section
        tk.Label(self.note_frame, text="Notes", font=("Arial", 14), bg="lightgray").pack(pady=5)
    
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

        self.load_notes_button = tk.Button(self.note_frame, text="Begin Notetaking", command=self.load_notes_for_section, width=15)
        self.load_notes_button.pack(pady=5)

        self.note_text = tk.Text(self.note_frame, wrap="word", height=20)
        self.note_text.pack(expand=True, fill="both", padx=10, pady=10)

        # PDF viewer
        tk.Label(self.pdf_frame, text="PDF Viewer", font=("Arial", 14), bg="white").pack(pady=10)

        # Add a canvas for displaying PDF content
        self.canvas = tk.Canvas(self.pdf_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar for the canvas
        scroll_y = tk.Scrollbar(self.pdf_frame, orient="vertical", command=self.canvas.yview)
        scroll_y.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=scroll_y.set)

        

        # SQ3R prompts
        self.prompt_labels = [
            tk.Label(self.note_frame, text="SURVEY: Glance over the headings to get the big ideas.", anchor="w", bg="lightgray"),
            tk.Label(self.note_frame, text="QUESTION: What questions do you want to answer?", anchor="w", bg="lightgray"),
            tk.Label(self.note_frame, text="READ: Read to find answers and main points.", anchor="w", bg="lightgray"),
            tk.Label(self.note_frame, text="RECITE: Write down what you remember.", anchor="w", bg="lightgray"),
            tk.Label(self.note_frame, text="REVIEW: Summarize key ideas and test yourself.", anchor="w", bg="lightgray"),
        ]

        for label in self.prompt_labels:
            label.pack(anchor="w", padx=10)

        # Back button
        back_btn = tk.Button(self, text="Back to Main Menu", width=20, command=lambda: controller.show_frame(MainMenu))
        back_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Methods from MainWindow class
    def load_pdf(self):
        """Load a PDF file and display its content in the PDF viewer."""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            try:
                # Render the first page of the PDF as an image
                img = self.pdf_manager.render_page_as_image(file_path, page_number=0, dpi=100)

                # Convert the PIL image to a format compatible with Tkinter
                self.tk_image = ImageTk.PhotoImage(img)

                # Display the image on the canvas
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
                self.canvas.config(scrollregion=self.canvas.bbox("all"))
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to load PDF: {e}")



    def create_note_hierarchy(self):
        from tkinter import messagebox
        self.note_text.delete("1.0", "end")
        messagebox.showinfo("Create Note Hierarchy", "Please enter the chapter title, section heading, and notes in the note-taking area.")

    def save_notes(self):
        from tkinter import messagebox
        chapter = self.chapter_entry.get().strip()
        section = self.section_entry.get().strip()
        notes = self.note_text.get("1.0", "end").strip()

        if not chapter or not section or not notes:
            messagebox.showwarning("Warning", "All fields must be filled out to save notes.")
            return

        self.note_manager.create_note_hierarchy(chapter, section, notes)
        messagebox.showinfo("Success", "Notes saved successfully.")

    def load_notes(self):
        from tkinter import messagebox
        notes = self.note_manager.load_notes()
        if notes:
            display = "\n\n".join(
                f"Chapter: {n['chapter_title']}\nSection: {n['section_heading']}\nNotes: {n['notes']}" for n in notes
            )
            self.note_text.delete("1.0", "end")
            self.note_text.insert("1.0", display)
        else:
            self.note_text.delete("1.0", "end")
            messagebox.showinfo("Loaded Notes", "No notes found.")

    def delete_all_notes(self):
        from tkinter import messagebox
        if messagebox.askyesno("Delete All Notes", "Are you sure you want to delete all notes?"):
            self.note_manager.delete_all_notes()
            self.note_text.delete("1.0", "end")
            messagebox.showinfo("Success", "All notes deleted.")

    def load_notes_for_section(self):
        from tkinter import messagebox
        chapter = self.chapter_entry.get().strip()
        section = self.section_entry.get().strip()
        if not chapter or not section:
            messagebox.showwarning("Warning", "Chapter and section must be filled.")
            return
        notes = self.note_manager.load_notes()
        for row in notes:
            if row["chapter_title"] == chapter and row["section_heading"] == section:
                self.note_text.delete("1.0", "end")
                self.note_text.insert("1.0", row["notes"])
                return
        self.note_text.delete("1.0", "end")
        messagebox.showinfo("No Notes", "No notes found for this chapter and section.")

    def toggle_prompts(self):
        if self.sq3r_enabled.get():
            for label in self.prompt_labels:
                label.pack(anchor="w", padx=10)
        else:
            for label in self.prompt_labels:
                label.pack_forget()


class ServerSetupScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Server Setup Page", font=("Arial", 16))
        label.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)

        # Placeholder server setup info
        instructions = tk.Label(self, text="Instructions or fields for setting up the server will go here.")
        instructions.pack(pady=10)


class AboutScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="About ARA", font=("Arial", 16))
        label.pack(pady=20)

        description = tk.Label(
            self,
            text="ARA helps students actively read using the SQ3R method.\nSurvey, Question, Read, Recite, Review.\n How it works",
            justify="center"
        )
        description.pack(pady=10)

        back_btn = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)


# Run the application
if __name__ == "__main__":
    app = ARA()
    app.mainloop()
