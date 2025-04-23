import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from pdf_manager import PDFManager
from note_manager import NoteManager
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import fitz  # PyMuPDF library for handling PDFs

## from database_manager import DatabaseManager

class ARA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ARA - Active Reading Assistant")
        self.geometry("1100x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.setup_custom_theme()

        self.frames = {}

        for F in (MainMenu, NotesScreen, ServerSetupScreen, AboutScreen):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def setup_custom_theme(self):
        style = ttk.Style()

        # Use a base theme with support for custom styling
        style.theme_use("clam")

        # Define primary colors
        bg_dark = "#1e1e1e"
        bg_medium = "#2c2c2c"
        bg_light = "#3a3a3a"
        fg_light = "#f0f0f0"
        accent_mint = "#98ff98"  # soft mint green
        border_color = "#3a3a3a"

        # General window background
        self.configure(bg=bg_dark)

        # Set default styles for all ttk widgets
        style.configure(".", 
                        background=bg_medium,
                        foreground=fg_light,
                        font=("Segoe UI", 10),
                        relief="flat")

        style.configure("TLabel",
                        background=bg_dark,
                        foreground=fg_light)

        style.configure("TButton",
                        background=bg_medium,
                        foreground=fg_light,
                        padding=6,
                        borderwidth=0)
        style.map("TButton",
                background=[("active", accent_mint), ("pressed", "#80ffaa")],
                foreground=[("active", "#000000")])

        style.configure("TEntry",
            fieldbackground=bg_light,    
            background=bg_light,
            foreground=fg_light,      
            padding=4,
            bordercolor=border_color, 
            relief="flat",
            borderwidth=1
        )

        style.configure("TFrame",
                        background=bg_dark)

        style.configure("TNotebook",
                        background=bg_dark,
                        borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=bg_medium,
                        foreground=fg_light,
                        padding=[10, 4],
                        borderwidth=0,
                        focuscolor=accent_mint)
        style.map("TNotebook.Tab",
                background=[("selected", accent_mint)],
                foreground=[("selected", "#000000")])

        style.configure("Treeview",
                        background=bg_medium,
                        foreground=fg_light,
                        fieldbackground=bg_medium,
                        bordercolor=border_color)
        style.map("Treeview",
                background=[("selected", accent_mint)],
                foreground=[("selected", "#000000")])

        # Custom rounded button
        style.configure("Rounded.TButton",
                        background=accent_mint,
                        foreground="#000000",
                        padding=8,
                        relief="flat",
                        borderwidth=0,
                        font=("Segoe UI", 10, "bold"))
        style.map("Rounded.TButton",
                background=[("active", "#baffba")])

        # Scrollbar (optional)
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=bg_medium,
                        troughcolor=bg_dark,
                        bordercolor=border_color,
                        arrowcolor=fg_light)

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(2, weight=1)

        content = ttk.Frame(container)
        content.grid(row=1, column=1)

        label = ttk.Label(content, text="Welcome to ARA\nYour Active Reading Assistant", style="Header.TLabel", justify="center")
        label.pack(pady=20)

        ttk.Button(content, text="Notes", width=20, command=lambda: controller.show_frame(NotesScreen)).pack(pady=5)
        ttk.Button(content, text="Server Setup", width=20, command=lambda: controller.show_frame(ServerSetupScreen)).pack(pady=5)
        ttk.Button(content, text="About", width=20, command=lambda: controller.show_frame(AboutScreen)).pack(pady=5)

class NotesScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.pdf_manager = PDFManager()

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Explicitly set the width of the note-taking box
        self.note_frame = ttk.Frame(self, width=250)  # Set the desired width
        self.note_frame.grid(row=1, column=0, sticky="nsew")
        self.note_frame.grid_propagate(False)  # Prevent resizing based on content

        self.pdf_frame = ttk.Frame(self)
        self.pdf_frame.grid(row=1, column=1, sticky="nsew")

        # Adjust column weights to allocate more space to the PDF viewer
        self.grid_rowconfigure(1, weight=1) # Row for PDF viewer and note-taking box
        self.grid_columnconfigure(0, weight=1)  # Note-taking box column
        self.grid_columnconfigure(1, weight=4)  # PDF viewer column

        # Buttons
        ttk.Button(self.button_frame, text="1. Load PDF", command=self.load_pdf, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="2. Create Note Hierarchy", command=self.create_note_hierarchy, width=20).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="3. Save Notes", command=self.save_notes, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="4. Load Notes", command=self.load_notes, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="5. Delete All Notes", command=self.delete_all_notes, width=20).pack(side="left", padx=5, pady=5)

        self.sq3r_enabled = tk.BooleanVar(value=True)
        self.prompt_toggle = ttk.Checkbutton(self.button_frame, text="SQ3R Prompts", variable=self.sq3r_enabled, command=self.toggle_prompts)
        self.prompt_toggle.pack(side="left", padx=5, pady=5)

        ttk.Label(self.note_frame, text="Notes", style="Header.TLabel").pack(pady=5)

        chapter_frame = ttk.Frame(self.note_frame)
        chapter_frame.pack(pady=5, padx=10, fill="x")
        ttk.Label(chapter_frame, text="Chapter:").pack(side="left", padx=5)
        self.chapter_entry = tk.Entry(chapter_frame, width=30, bg="#3a3a3a", fg="#f0f0f0",
                              bd=0, relief="flat", highlightthickness=1,
                              highlightbackground="#3a3a3a", highlightcolor="#98ff98")
        self.chapter_entry.pack(side="left", padx=5, pady=1)


        section_frame = ttk.Frame(self.note_frame)
        section_frame.pack(pady=5, padx=10, fill="x")
        ttk.Label(section_frame, text="Section:").pack(side="left", padx=5)
        self.section_entry = tk.Entry(section_frame, width=30, bg="#3a3a3a", fg="#f0f0f0",
                              bd=0, relief="flat", highlightthickness=1,
                              highlightbackground="#3a3a3a", highlightcolor="#98ff98")
        self.section_entry.pack(side="left", padx=5, pady=1)

        # Button to load notes for the selected section
        self.load_notes_button = ttk.Button(self.note_frame, text="Begin Notetaking", command=self.load_notes_for_section, width=20)
        self.load_notes_button.pack(pady=5)

        self.note_text = tk.Text(self.note_frame, wrap="word", bg="#3a3a3a", fg="#f0f0f0", bd=0, relief="flat", highlightthickness=1, highlightbackground="#3a3a3a", highlightcolor="#98ff98", height=20)
        self.note_text.pack(expand=True, fill="both", padx=10, pady=10)

        # PDF viewer
        ttk.Label(self.pdf_frame, text="PDF Viewer").pack(pady=10)

        # Add a canvas for displaying PDF content
        self.canvas = tk.Canvas(self.pdf_frame, height=500, bg="#3a3a3a", bd=0, relief="flat",
                        highlightthickness=1, highlightbackground="#3a3a3a", highlightcolor="#98ff98")
        self.canvas.pack(side="top", fill="x", expand=False)  # Adjust to fit horizontally but not vertically

        # Add these attributes to track the current page and total pages
        self.current_page = 0  # Track the current page
        self.total_pages = 0  # Track the total number of pages
        self.file_path = None  # Store the file path of the loaded PDF

        # Add navigation buttons for the PDF viewer
        nav_frame = ttk.Frame(self.pdf_frame)  # Create a frame for navigation buttons
        nav_frame.pack(side="bottom", fill="x")  # Place it at the bottom of the PDF viewer

        self.prev_button = ttk.Button(nav_frame, text="Previous", command=self.show_previous_page, state="disabled")
        self.prev_button.pack(side="left", padx=10, pady=5)  # Align to the left

        self.next_button = ttk.Button(nav_frame, text="Next", command=self.show_next_page, state="disabled")
        self.next_button.pack(side="right", padx=10, pady=5)  # Align to the right

        # SQ3R prompts
        self.prompt_labels = [
            ttk.Label(self.note_frame, text="SURVEY: Glance over the headings to get the big ideas."),
            ttk.Label(self.note_frame, text="QUESTION: What questions do you want to answer?"),
            ttk.Label(self.note_frame, text="READ: Read to find answers and main points."),
            ttk.Label(self.note_frame, text="RECITE: Write down what you remember."),
            ttk.Label(self.note_frame, text="REVIEW: Summarize key ideas and test yourself."),
        ]

        for label in self.prompt_labels:
            label.pack(anchor="w", padx=10)

        back_btn = ttk.Button(self, text="Back to Main Menu", width=20, command=lambda: controller.show_frame(MainMenu))
        back_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def load_pdf(self):
        """Load a PDF file and display its first page in the PDF viewer."""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            try:
                # Open the PDF and get the total number of pages
                with fitz.open(file_path) as pdf:
                    self.total_pages = len(pdf)

                # Reset to the first page
                self.current_page = 0
                self.file_path = file_path

                # Display the first page
                self.display_page(self.current_page)

                # Enable navigation buttons if there are multiple pages
                if self.total_pages > 1:
                    self.next_button.config(state="normal")
                else:
                    self.next_button.config(state="disabled")
                self.prev_button.config(state="disabled")
            except Exception as e:
                ttk.messagebox.showerror("Error", f"Failed to load PDF: {e}")
        
    def display_page(self, page_number):
        """Display a specific page of the PDF in the canvas."""
        try:
            # Render the page as an image
            img = self.pdf_manager.render_page_as_image(self.file_path, page_number, dpi=100)

            # Resize the image to fit the canvas dimensions
            self.update_idletasks()  # Ensure the canvas dimensions are updated
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img = img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)

            # Convert the PIL image to a format compatible with Tkinter
            self.tk_image = ImageTk.PhotoImage(img)

            # Display the image on the canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        except Exception as e:
            ttk.messagebox.showerror("Error", f"Failed to display page: {e}")
    
    def show_next_page(self):
        """Display the next page of the PDF."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_page(self.current_page)

            # Update navigation buttons
            self.prev_button.config(state="normal")
            if self.current_page == self.total_pages - 1:
                self.next_button.config(state="disabled")

    def show_previous_page(self):
        """Display the previous page of the PDF."""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)

            # Update navigation buttons
            self.next_button.config(state="normal")
            if self.current_page == 0:
                self.prev_button.config(state="disabled")

    def create_note_hierarchy(self):
        self.note_text.delete("1.0", "end")
        messagebox.showinfo("Create Note Hierarchy", "Please enter the chapter title, section heading, and notes in the note-taking area.")

    def save_notes(self):
        chapter = self.chapter_entry.get().strip()
        section = self.section_entry.get().strip()
        notes = self.note_text.get("1.0", "end").strip()
        if not chapter or not section or not notes:
            messagebox.showwarning("Warning", "All fields must be filled out to save notes.")
            return
        self.note_manager.create_note_hierarchy(chapter, section, notes)
        messagebox.showinfo("Success", "Notes saved successfully.")

    def load_notes(self):
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
        if messagebox.askyesno("Delete All Notes", "Are you sure you want to delete all notes?"):
            self.note_manager.delete_all_notes()
            self.note_text.delete("1.0", "end")
            messagebox.showinfo("Success", "All notes deleted.")

    def load_notes_for_section(self):
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
    def toggle_prompts(self):
        if self.sq3r_enabled.get():
            for label in self.prompt_labels:
                label.pack(anchor="w", padx=10)
        else:
            for label in self.prompt_labels:
                label.pack_forget()

class ServerSetupScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Server Setup Screen").pack(padx=10, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

class AboutScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="About This App").pack(padx=10, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

if __name__ == "__main__":
    app = ARA()
    app.mainloop()
