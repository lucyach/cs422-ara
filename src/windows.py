import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from pdf_manager import PDFManager
from note_manager import NoteManager
from PIL import Image, ImageTk
import fitz  # PyMuPDF library for handling PDFs
from database_manager import DatabaseManager

# Global colors
bg_dark = "#1e1e1e"
bg_medium = "#2c2c2c"
bg_light = "#3a3a3a"
fg_light = "#f0f0f0"
fg_dark = "#000000"
accent_color = "#98ff98"

# Global fonts
title_font = "Segoe UI", 25, "bold"
header_font = "Segoe UI", 14, "bold"
text_font = "Segoe UI", 10


class ARA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ARA - Active Reading Assistant")
        self.geometry("1100x800")

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

        # General window background
        self.configure(bg=bg_dark)

        # Set default styles for all ttk widgets
        style.configure(".", 
                        background=bg_medium,
                        foreground=fg_light,
                        font=(text_font),
                        relief="flat")

        style.configure("TLabel",
                        background=bg_dark,
                        foreground=fg_light)
        
        style.configure("Header.TLabel",
                        background=bg_dark,
                        foreground=accent_color,
                        font=(header_font),
                        padding=10)
        
        style.configure("Title.TLabel",
                background=bg_dark,
                foreground=accent_color,
                font=(title_font),
                padding=10,
                justify="center")


        style.configure("TButton",
                        background=bg_medium,
                        foreground=fg_light,
                        padding=6,
                        borderwidth=0)
        style.map("TButton",
                  background=[("active", accent_color)],
                  foreground=[("active", fg_dark)])

        style.configure("TFrame",
                        background=bg_dark)

        # Scrollbar (optional)
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=bg_medium,
                        troughcolor=bg_dark,
                        bordercolor=bg_light,
                        arrowcolor=fg_light)
        
        style.configure("TCheckbutton",
                        background=bg_dark,
                        foreground=fg_light,
                        font=(text_font),
                        focuscolor=accent_color,
                        indicatorcolor=bg_light)

        style.map("TCheckbutton",
                  background=[("active", accent_color)],
                  foreground=[("active", fg_dark)])

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Make the MainMenu frame expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a container frame that will hold the content
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        # Center container content using another grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(2, weight=1)

        content = ttk.Frame(container)
        content.grid(row=1, column=1)

        label = ttk.Label(content, text="Welcome to ARA\nYour Active Reading Assistant", style="Title.TLabel")
        label.pack(pady=20)

        ttk.Button(content, text="Notes", width=20, command=lambda: controller.show_frame(NotesScreen)).pack(pady=5)
        ttk.Button(content, text="Server Setup", width=20, command=lambda: controller.show_frame(ServerSetupScreen)).pack(pady=5)
        ttk.Button(content, text="About", width=20, command=lambda: controller.show_frame(AboutScreen)).pack(pady=5)

class NotesScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.database_manager = DatabaseManager()  # Initialize the database manager
        self.note_manager = NoteManager(self.database_manager)  # Pass the database manager to NoteManager
        self.pdf_manager = PDFManager()

        # Layout frames for buttons, notes, and PDF viewer
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
        ttk.Button(self.button_frame, text="2. Highlight Sections", command=self.highlight_sections, width=20).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="3. Create Note Hierarchy", command=self.create_note_hierarchy, width=25).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="4. Save Notes", command=self.save_notes, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="5. Load Notes", command=self.load_notes, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="6. Delete All Notes", command=self.delete_all_notes, width=20).pack(side="left", padx=5, pady=5)

        # SQ3R checkbox prompts
        self.sq3r_enabled = tk.BooleanVar(value=True)
        self.prompt_toggle = ttk.Checkbutton(self.button_frame, text="SQ3R Prompts", variable=self.sq3r_enabled, command=self.toggle_prompts)
        self.prompt_toggle.pack(side="left", padx=5, pady=5)

        # Notes section
        ttk.Label(self.note_frame, text="Notes", style="Header.TLabel").pack(pady=5)

        # tk.Entry is used to create a text entry field
        chapter_frame = ttk.Frame(self.note_frame)
        chapter_frame.pack(pady=5, padx=10, fill="x")
        ttk.Label(chapter_frame, text="Chapter:").pack(side="left", padx=5)
        self.chapter_entry = tk.Entry(chapter_frame, 
                                      width=30, bg=bg_light, 
                                      fg=fg_light,
                                      bd=0, relief="flat", 
                                      highlightthickness=1,
                                      highlightbackground=bg_light, 
                                      highlightcolor=accent_color)
        self.chapter_entry.pack(side="left", padx=5, pady=1)


        section_frame = ttk.Frame(self.note_frame)
        section_frame.pack(pady=5, padx=10, fill="x")
        ttk.Label(section_frame, text="Section:").pack(side="left", padx=5)
        self.section_entry = tk.Entry(section_frame, 
                                      width=30, bg=bg_light, 
                                      fg=fg_light,
                                      bd=0, relief="flat", highlightthickness=1,
                                      highlightbackground=bg_light, highlightcolor=accent_color)
        self.section_entry.pack(side="left", padx=5, pady=1)

        # Button to load notes for the selected section
        self.load_notes_button = ttk.Button(self.note_frame, text="Begin Notetaking", command=self.load_notes_for_section, width=20)
        self.load_notes_button.pack(pady=5)

        self.note_text = tk.Text(self.note_frame, 
                                 wrap="word", 
                                 bg=bg_light, 
                                 fg=fg_light, bd=0, 
                                 relief="flat", highlightthickness=1, 
                                 highlightbackground=bg_light,
                                 highlightcolor=accent_color, 
                                 height=20)
        
        self.note_text.pack(expand=True, fill="both", padx=10, pady=10)

        # PDF viewer
        ttk.Label(self.pdf_frame, text="PDF Viewer", style="Header.TLabel").pack(pady=10)

        # Add a canvas for displaying PDF content
        self.canvas = tk.Canvas(self.pdf_frame, 
                                height=500, 
                                bg=bg_light, 
                                bd=0, 
                                relief="flat",
                                highlightthickness=1, 
                                highlightbackground=bg_light, 
                                highlightcolor=accent_color)
        self.canvas.pack(side="top", fill="both", expand=True)

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

        # SQ3R checkbox prompts instead of just labels 
        self.sq3r_check_vars = []
        self.sq3r_checkboxes = []

        sq3r_texts = [
            "SURVEY: Glance over the headings to get the big ideas.",
            "QUESTION: What questions do you want to answer?",
            "READ: Read to find answers and main points.",
            "RECITE: Write down what you remember.",
            "REVIEW: Summarize key ideas and test yourself."
        ]

        for text in sq3r_texts:
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.note_frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=10)
            self.sq3r_check_vars.append(var)
            self.sq3r_checkboxes.append(checkbox)

        # Back to the main menu button
        back_btn = ttk.Button(self, text="Back to Main Menu", width=20, command=lambda: controller.show_frame(MainMenu))
        back_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Methods from MainWindow class
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
                messagebox.showerror("Error", f"Failed to load PDF: {e}")
            
    def display_page(self, page_number):
        """Display a specific page of the PDF and make it responsive to window resizing."""
        try:
            self.current_page = page_number

            # Render the raw image for the current page
            raw_image = self.pdf_manager.render_page_as_image(self.file_path, page_number, dpi=100)

            # Bind to canvas resizing — trigger redisplay on window resize
            if not hasattr(self, "resize_bound"):
                self.canvas.bind("<Configure>", lambda event: self.display_page(self.current_page))
                self.resize_bound = True

            # Get current canvas size
            self.update_idletasks()  # Ensure dimensions are up-to-date
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Calculate scaled size with aspect ratio preserved
            img_ratio = raw_image.width / raw_image.height
            canvas_ratio = canvas_width / canvas_height

            if img_ratio > canvas_ratio:
                new_width = canvas_width
                new_height = int(canvas_width / img_ratio)
            else:
                new_height = canvas_height
                new_width = int(canvas_height * img_ratio)

            resized_image = raw_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert and display
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.delete("all")
            x = (self.canvas.winfo_width() - new_width) // 2
            y = (self.canvas.winfo_height() - new_height) // 2
            self.canvas.create_image(x, y, anchor="nw", image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display page: {e}")

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
        self.note_text.delete("1.0", "end")
        messagebox.showinfo("No Notes", "No notes found for this chapter and section.")

    def toggle_prompts(self):
        if self.sq3r_enabled.get():
            for checkbox in self.sq3r_checkboxes:
                checkbox.pack(anchor="w", padx=10)
        else:
            for checkbox in self.sq3r_checkboxes:
                checkbox.pack_forget()

    def highlight_sections(self):
        from tkinter import simpledialog, messagebox
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