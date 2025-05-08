import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from pdf_manager import PDFManager
from note_manager import NoteManager
from PIL import Image, ImageTk
import fitz  # PyMuPDF library for handling PDFs
import json, os
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

database_manager = DatabaseManager()  # Initialize the database manager
pdf_manager = PDFManager()
note_manager = NoteManager(database_manager)  # Pass the database manager to NoteManager
note_manager.initialize_note_folder()

default_creds = {}


script_dir = os.path.dirname(__file__)  # Folder where script is located
file_path = os.path.join(script_dir, 'creds.json') # Path to the credentials file

try: # Attempt to load the credentials from a JSON file
    with open(file_path, 'r') as file: # Open the JSON file
            default_creds = json.load(file) # Load the credentials into a dictionary
except: #   If the file is not found, print an error message
    note_manager.offline_mode = True
    print("Error, no credential file found!")

class ARA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ARA - Active Reading Assistant") # Set the window title
        self.geometry("1200x800") # Set the window size

        # Set up the main window layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.setup_custom_theme()

        self.frames = {} # Dictionary to hold different frames

        # Create frames for different screens
        for F in (MainMenu, NotesScreen, ServerSetupScreen, AboutScreen): # Iterate through the frames
            frame = F(parent=self, controller=self) # Create an instance of the frame
            self.frames[F] = frame # Store the frame in the dictionary
            frame.grid(row=0, column=0, sticky="nsew") # Grid the frame in the main window

        self.show_frame(MainMenu) # Show the main menu frame by default

    def show_frame(self, frame_class): # Show a frame for the given class
        frame = self.frames[frame_class] # Get the frame from the dictionary
        frame.tkraise() # Raise the frame to the top of the stack

    def setup_custom_theme(self): # Set up a custom theme for the application
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

        # Set specific styles for labels, buttons, and frames
        style.configure("TLabel",
                        background=bg_dark,
                        foreground=fg_light)
        
        # Header and title styles
        style.configure("Header.TLabel",
                        background=bg_dark,
                        foreground=accent_color,
                        font=(header_font),
                        padding=10)
        
        # Title label style
        style.configure("Title.TLabel",
                background=bg_dark,
                foreground=accent_color,
                font=(title_font),
                padding=10,
                justify="center")

        # Button styles
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
        
        # Custom Combobox style
        style.configure("CustomCombobox.TCombobox",
            fieldbackground=bg_light,
            background=bg_medium,
            foreground=fg_light,
            arrowcolor=fg_light,
            relief="flat",
            borderwidth=1)

        style.map("CustomCombobox.TCombobox",
            fieldbackground=[("readonly", bg_light)],
            foreground=[("readonly", fg_light)],
            arrowcolor=[("active", fg_dark)],
            background=[("active", accent_color)],
            bordercolor=[("focus", accent_color)])

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Reference to the main application

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

        # Set the background color of the content frame
        label = ttk.Label(
            content,
            text="Welcome to ARA\nYour Active Reading Assistant",
            style="Title.TLabel",
            justify="center",
            anchor="center"
        )
        label.pack(pady=20)

        # Create buttons for different functionalities
        ttk.Button(content, text="Notes", width=20, command=lambda: controller.show_frame(NotesScreen)).pack(pady=5)
        ttk.Button(content, text="Server Setup", width=20, command=lambda: controller.show_frame(ServerSetupScreen)).pack(pady=5)
        ttk.Button(content, text="About", width=20, command=lambda: controller.show_frame(AboutScreen)).pack(pady=5)

class NotesScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Reference to the main application

        # Layout frames for buttons, notes, and PDF viewer
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Explicitly set the width of the note-taking box
        self.note_frame = ttk.Frame(self, width=250)  # Set the desired width
        self.note_frame.grid(row=1, column=0, sticky="nsew")
        self.note_frame.grid_propagate(False)  # Prevent resizing based on content

        self.pdf_frame = ttk.Frame(self) # Frame for PDF viewer
        self.pdf_frame.grid(row=1, column=1, sticky="nsew") # Grid the PDF frame

        # Adjust column weights to allocate more space to the PDF viewer
        self.grid_rowconfigure(1, weight=1) # Row for PDF viewer and note-taking box
        self.grid_columnconfigure(0, weight=1)  # Note-taking box column
        self.grid_columnconfigure(1, weight=4)  # PDF viewer column

        # Buttons
        ttk.Button(self.button_frame, text="Load PDF", command=self.load_pdf, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="Save Notes", command=self.save_notes, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="Load Notes", command=self.load_notes, width=15).pack(side="left", padx=5, pady=5)
        ttk.Button(self.button_frame, text="Delete Note", command=self.delete_current_note, width=15).pack(side="left", padx=5, pady=5)

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
                                      width=30, 
                                      bg=bg_light, 
                                      fg=fg_light,
                                      bd=0, 
                                      relief="flat", 
                                      highlightthickness=1,
                                      highlightbackground=bg_light, 
                                      highlightcolor=accent_color)
        self.chapter_entry.pack(side="left", padx=5, pady=1)


        # Section entry field
        section_frame = ttk.Frame(self.note_frame)
        section_frame.pack(pady=5, padx=10, fill="x")
        ttk.Label(section_frame, text="Section:").pack(side="left", padx=5)
        self.section_entry = tk.Entry(section_frame, 
                                      width=30, 
                                      bg=bg_light, 
                                      fg=fg_light,
                                      bd=0, 
                                      relief="flat", 
                                      highlightthickness=1,
                                      highlightbackground=bg_light, 
                                      highlightcolor=accent_color)
        self.section_entry.pack(side="left", padx=5, pady=1)

        # Note-taking area
        self.note_text = tk.Text(self.note_frame, 
                                 wrap="word", 
                                 bg=bg_light, 
                                 fg=fg_light, 
                                 bd=0, 
                                 relief="flat", 
                                 highlightthickness=1, 
                                 highlightbackground=bg_light,
                                 highlightcolor=accent_color, 
                                 height=20)
        
        self.note_text.pack(expand=True, fill="both", padx=10, pady=10) # Expand to fill the frame

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

        # Preloaded PDFs
        ttk.Label(self.button_frame, text="Preloaded PDFs:").pack(side="left", padx=(10, 0), pady=5)

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_dir = os.path.join(project_root, "pdfs")

        self.preloaded_pdfs = {
            "Sommerville - Chapter 1": os.path.join(pdf_dir, "SE_10e_Sommerville_Ch1.pdf"),
            "Sommerville - Chapter 2": os.path.join(pdf_dir, "SE_10e_Sommerville_Ch2.pdf"),
            "Sommerville - Chapter 22": os.path.join(pdf_dir, "SE_10e_Sommerville_Ch22.pdf"),
        }


        self.pdf_selector = ttk.Combobox(
            self.button_frame,
            values=list(self.preloaded_pdfs.keys()),
            state="readonly",
            width=30,
            style="CustomCombobox.TCombobox"
        )

        # Set the default text for the combobox
        self.pdf_selector.set("Select a PDF")
        self.pdf_selector.pack(side="left", padx=5, pady=5)

        self.pdf_selector.bind("<<ComboboxSelected>>", self.on_preloaded_pdf_selected)

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

        # Create checkboxes for each SQ3R prompt
        for text in sq3r_texts:
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.note_frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=10)
            self.sq3r_check_vars.append(var)
            self.sq3r_checkboxes.append(checkbox)

        # Back to the main menu button
        back_btn = ttk.Button(self, text="Back to Main Menu", width=20, command=lambda: controller.show_frame(MainMenu))
        back_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Bind the <<FocusOut>> event to the chapter and section entry fields
        self.chapter_entry.bind("<Return>", lambda event: self.load_notes_for_section())
        self.section_entry.bind("<Return>", lambda event: self.load_notes_for_section())



    # Methods from MainWindow class
    def load_pdf(self):
        file_path = filedialog.askopenfilename( # Open file dialog to select a PDF
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path: # Check if a file was selected
            try:
                with fitz.open(file_path) as pdf: # Open the PDF file using PyMuPDF
                    self.total_pages = len(pdf) # Get the total number of pages

                # Reset current page and file path
                self.current_page = 0 # Set current page to 0
                self.file_path = file_path # Store the file path
                note_manager.active_pdf = os.path.splitext(os.path.basename(file_path))[0] # Set the active PDF name
                self.display_page(self.current_page) # Display the first page of the PDF
                self.load_notes_for_section()  # Automatically load notes for the PDF
                if self.total_pages > 1: # Enable navigation buttons if there are multiple pages
                    self.next_button.config(state="normal")
                else: # Disable the next button if there's only one page
                    self.next_button.config(state="disabled")
                self.prev_button.config(state="disabled")
            except Exception as e: # Handle any errors that occur during PDF loading
                messagebox.showerror("Error", f"Failed to load PDF: {e}")
            
    def display_page(self, page_number):
        """Display a specific page of the PDF and make it responsive to window resizing."""
        try:
            self.current_page = page_number # Set the current page

            # Render the raw image for the current page
            raw_image = pdf_manager.render_page_as_image(self.file_path, page_number, dpi=100)

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

            # Determine new dimensions based on aspect ratio
            if img_ratio > canvas_ratio:
                new_width = canvas_width
                new_height = int(canvas_width / img_ratio)
            else:
                new_height = canvas_height
                new_width = int(canvas_height * img_ratio)

            # Resize the image to fit the canvas
            resized_image = raw_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert and display
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.delete("all")
            x = (self.canvas.winfo_width() - new_width) // 2
            y = (self.canvas.winfo_height() - new_height) // 2
            self.canvas.create_image(x, y, anchor="nw", image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        except Exception as e: # Handle any errors that occur during page display
            messagebox.showerror("Error", f"Failed to display page: {e}")

    def show_next_page(self):
        """Display the next page of the PDF."""
        if self.current_page < self.total_pages - 1: # Check if there are more pages
            self.current_page += 1 # Increment the current page
            self.display_page(self.current_page) #  Display the next page

            # Update navigation buttons
            self.prev_button.config(state="normal")
            if self.current_page == self.total_pages - 1: # If on the last page
                self.next_button.config(state="disabled") # Disable the next button

    def show_previous_page(self):
        """Display the previous page of the PDF."""
        if self.current_page > 0: # Check if there are previous pages
            self.current_page -= 1 # Decrement the current page
            self.display_page(self.current_page) #  Display the previous page

            # Update navigation buttons
            self.next_button.config(state="normal")
            if self.current_page == 0: # If on the first page
                self.prev_button.config(state="disabled") # Disable the previous button

    def create_note_hierarchy(self): # Create a new note hierarchy
        self.note_text.delete("1.0", "end") # Clear the note-taking area
        messagebox.showinfo("Create Note Hierarchy", "Please enter the chapter title, section heading, and notes in the note-taking area.")

    def save_notes(self): # Save notes to the database
        chapter = self.chapter_entry.get().strip() # Get the chapter title
        section = self.section_entry.get().strip() # Get the section heading
        notes = self.note_text.get("1.0", "end").strip() # Get the notes from the text box

        if not chapter or not section or not notes: # Check if all fields are filled out
            messagebox.showwarning("Warning", "All fields must be filled out to save notes.")
            return

        # Save only the raw values
        #formatted_notes = f"{self.file_path or 'N/A'}\n{notes}"

        # Save the notes under the respective chapter and section
        note_manager.create_note_hierarchy(chapter, section, notes)

        messagebox.showinfo("Success", "Notes saved successfully.") # Show success message

    def load_notes(self): # Load notes from the database

        notes = note_manager.load_notes()

        # Create a popup window to select a note
        popup = tk.Toplevel(self)
        popup.title("Select a Note")
        popup.geometry("500x300")
        popup.configure(bg=bg_dark)

        # Set up the popup window style
        ttk.Label(popup, text="Select a note to load:", style="Header.TLabel").pack(pady=10)

        # Format: "Chapter: X - Section: Y"
        options = [f"{n['chapter_title']} - {n['section_heading']}" for n in notes]
        selected_note = tk.StringVar() # Variable to hold the selected note
        note_dropdown = ttk.Combobox( # Create a dropdown for note selection
            popup,
            values=options,
            state="readonly",
            textvariable=selected_note,
            width=50,
            style="CustomCombobox.TCombobox"  # Match style here
        )
        note_dropdown.set("Choose a note...") # Set default text
        note_dropdown.pack(pady=5) # Pack the dropdown

        # Load the selected note into the text box
        def load_selected_note():
            choice = selected_note.get()
            for n in notes: # Iterate through the notes to find the selected one
                label = f"{n['chapter_title']} - {n['section_heading']}"
                if label == choice: # If the selected note matches the label
                    self.chapter_entry.delete(0, "end")
                    self.section_entry.delete(0, "end")
                    self.chapter_entry.insert(0, n["chapter_title"])
                    self.section_entry.insert(0, n["section_heading"])

                    popup.destroy()
                    return
            
            new_text = database_manager.load_notes_from_menu(choice, note_manager.active_pdf)

            self.note_text.delete("1.0", tk.END)
            self.note_text.insert("1.0", new_text)

            parts = choice.split(" - ")

            self.chapter_entry.delete(0, "end")
            self.chapter_entry.insert(0, parts[0])
            self.section_entry.delete(0, "end")
            self.section_entry.insert(0, parts[1])

            popup.destroy()

        # Create a button to load the selected note
        ttk.Button(popup, text="Load Note", command=load_selected_note).pack(pady=10)


    def delete_current_note(self):
        """Delete the currently loaded note based on the chapter and section inputs."""
        chapter = self.chapter_entry.get().strip()
        section = self.section_entry.get().strip()

        if not chapter or not section:
            messagebox.showwarning("Warning", "Please enter both chapter and section to delete a note.")
            return

        if messagebox.askyesno("Delete Note", f"Are you sure you want to delete the note for:\n\nChapter: {chapter}\nSection: {section}?"):
            note_manager.delete_note(chapter, section)
            self.note_text.delete("1.0", "end")
            messagebox.showinfo("Deleted", "The selected note has been deleted.")


    def load_notes_for_section(self):
        """Load notes for the specified chapter and section, or clear the note-taking box if none are found."""
        chapter = self.chapter_entry.get().strip() # Get the chapter title
        section = self.section_entry.get().strip() # Get the section heading

        if not chapter or not section: # Check if both fields are filled out
            self.note_text.delete("1.0", "end") # Clear the note-taking area
            return

        # Try to load notes by chapter and section

        notes = note_manager.load_notes() # Load all notes from the database
        for row in notes: # Iterate through the notes to find the matching chapter and section
            if row["chapter_title"] == chapter and row["section_heading"] == section: # Check if the chapter and section match
                self.note_text.delete("1.0", "end") # Clear the note-taking area
                self.note_text.insert("1.0", row["notes"]) # Insert the loaded notes
                return

        # Clear the note-taking box if no notes are found
        self.note_text.delete("1.0", "end")

    def toggle_prompts(self): # Toggle the visibility of SQ3R prompts
    
        if self.sq3r_enabled.get(): # Check if SQ3R prompts are enabled
            for checkbox in self.sq3r_checkboxes: # Show the checkboxes
                checkbox.pack(anchor="w", padx=10) # Pack them with padding
        else: # If disabled, hide the checkboxes
            for checkbox in self.sq3r_checkboxes: # Hide the checkboxes
                checkbox.pack_forget() # Remove them from the layout
    
    def on_preloaded_pdf_selected(self, event): # Handle selection of preloaded PDFs
        """Load the selected preloaded PDF and display its first page."""
        selected = self.pdf_selector.get()
        self.pdf_selector.selection_clear()
        note_manager.active_pdf = selected

        if selected in self.preloaded_pdfs: # Check if the selected PDF is in the preloaded list
            self.file_path = self.preloaded_pdfs[selected] # Get the file path of the selected PDF
            try: # Open the PDF file using PyMuPDF
                with fitz.open(self.file_path) as pdf: # Open the PDF file
                    self.total_pages = len(pdf) # Get the total number of pages


                self.current_page = 0
                self.display_page(self.current_page)
                #self.load_notes_for_section()


                self.next_button.config(state="normal" if self.total_pages > 1 else "disabled") # Enable next button if there are multiple pages
                self.prev_button.config(state="disabled") # Disable previous button if on the first page
            except Exception as e: # Handle any errors that occur during PDF loading
                messagebox.showerror("Error", f"Failed to load PDF: {e}")
    
    def delete_notes_for_pdf(self, file_path):
        """Delete notes associated with a specific PDF file."""
        query = """
        DELETE FROM note_hierarchy
        WHERE chapter_title = :file_path
        """
        #database_manager.save_data(query, {"file_path": file_path})
        print(f"Notes associated with the file '{file_path}' have been deleted.")

class ServerSetupScreen(ttk.Frame): # Server setup screen for connecting to the database
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Make the ServerSetupScreen frame expand
        label = ttk.Label(self, text="Server Setup Page", style="Header.TLabel")
        label.pack(pady=20)

        self.custom_input = tk.Text(self, height=1, width=40)
        self.custom_input.pack()

        # Placeholder server setup info
        instructions = ttk.Label(self, text="Select a user to connect:")
        instructions.pack(pady=10)

        self.usernames = list(default_creds.keys())
        self.user_selector = ttk.Combobox(self, values=self.usernames, state="readonly", width=30, style="CustomCombobox.TCombobox")
        self.user_selector.set("Choose a User")
        self.user_selector.pack(pady=10)

        connect_btn = ttk.Button(self, text="Connect", command=lambda:self.connection_verification())        
        connect_btn.pack(pady=10)

        #Back to the main menu button
        back_btn = ttk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)

        self.status_label = ttk.Label(self, text="In the textbox above, input the connection string from your database.", justify="center", foreground="white")
        self.status_label.pack()

    def connection_verification(self): # Verify the connection to the database
        user = self.user_selector.get() # Get the selected user from the combobox
        creds = default_creds.get(user) # Get the credentials for the selected user

        test= self.custom_input.get("1.0", "end-1c")
        print(test)


        
        value = database_manager.change_client(test) # Attempt to connect to the database with the selected user and credentials
        
        if value[0] == True: # If the connection is successful
            self.status_label.config(text=f"Successfully connected as {user}", foreground="green")
        else:
            self.status_label.config(text=f"Failed to connect as {user}:\n{value[1]}", justify="center",foreground="orange")


class AboutScreen(ttk.Frame): # About screen for the application
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Page title
        title = ttk.Label(self, text="About ARA", style="Title.TLabel")
        title.pack(pady=20)

        # Section 1: What is ARA?
        section1_text = (
            "ARA (Active Reading Assistant) is a reading and note-taking tool built around the SQ3R method:\n"
            "Survey, Question, Read, Recite, and Review.\n\n"
            "It is designed to help people engage deeply with academic texts, organize their ideas, and\n"
            "retain key information. ARA integrates PDF viewing, guided prompts, and structured note entry\n"
            "into one easy to use interface."
        )
        section1_label = ttk.Label(self, text=section1_text, style="Body.TLabel")
        section1_label.pack(padx=20, pady=10)

        #How it Works 
        section2_title = ttk.Label(self, text="How It Works", style="Header.TLabel", justify="center")
        section2_title.pack(pady=(20, 0))

        section2_text = (
            "1. Load a PDF: Start by uploading a reading or class material.\n"
            "2. Take Notes: Use the note-taking area to capture insights by chapter and section.\n"
            "3. Use Prompts: Enable SQ3R checkboxes to guide your reading and reflection process.\n"
            "4. Save & Review: Your notes are saved locally and can be revisited at any time.\n\n"
            "By combining reading with active reflection, ARA helps you process material more effectively\n"
            "and develop stronger study habits."
        )
        section2_label = ttk.Label(self, text=section2_text, style="Body.TLabel")
        section2_label.pack(padx=20, pady=10)

        # Back button
        back_btn = ttk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=20)

# if __name__ == "__main__":
#     app = ARA()
#     app.mainloop()