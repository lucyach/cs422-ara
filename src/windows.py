import tkinter as tk
from tkinter import ttk

<<<<<<< Updated upstream
class ARA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ARA - Active Reading Assistant")
        self.geometry("1000x700")

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

        

        label = tk.Label(self, text="Welcome to ARA\n Your Active Reading Assistent", font=("Arial", 20))
        label.pack(pady=30)

        notes_btn = tk.Button(self, text="Notes", width=20, command=lambda: controller.show_frame(NotesScreen))
        notes_btn.pack(pady=10)

        server_btn = tk.Button(self, text="Server Setup", width=20, command=lambda: controller.show_frame(ServerSetupScreen))
        server_btn.pack(pady=10)

        about_btn = tk.Button(self, text="About", width=20, command=lambda: controller.show_frame(AboutScreen))
        about_btn.pack(pady=10)


class NotesScreen(tk.Frame):
=======
class ARA(tk.Tk): # main window that creates and stores all of the frames/"pages"
    def __init__(self):
        super().__init__()
        self.title("ARA - Active Reading Assistant")
        self.geometry("1000x1000")

        self.frames = {}

    #using frames keeps everything in one window, which keeps buttons and other components from overlapping

        for F in (MainMenu, Notes, ServerSetup, About): #inisiates each frame "F" in a loop
            frame = F(parent=self, controller=self)
            self.frames[F] = frame   #adds the frames to a dictionary
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)



    def show_frame(self, frame_class): # makes only one frame visible at a time, and is called witn controller
        frame = self.frames[frame_class]
        frame.tkraise()


class MainMenu(tk.Frame):
>>>>>>> Stashed changes
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

<<<<<<< Updated upstream
        # Initialize managers
        #self.database_manager = DatabaseManager()
        #self.pdf_manager = PDFManager()
        #self.note_manager = NoteManager(self.database_manager)

        # Create frames for layout
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.note_frame = tk.Frame(self, bg="lightgray")
        self.note_frame.grid(row=1, column=0, sticky="nsew")

        self.pdf_frame = tk.Frame(self, bg="white")
        self.pdf_frame.grid(row=1, column=1, sticky="nsew")

        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Add buttons to the top frame
        tk.Button(self.button_frame, text="1. Load PDF", command=self.load_pdf, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="2. Highlight Sections", command=self.highlight_sections, width=20).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="3. Create Note Hierarchy", command=self.create_note_hierarchy, width=20).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="4. Save Notes", command=self.save_notes, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="5. Load Notes", command=self.load_notes, width=15).pack(side="left", padx=5, pady=5)
        tk.Button(self.button_frame, text="6. Delete All Notes", command=self.delete_all_notes, width=20).pack(side="left", padx=5, pady=5)

        # Add widgets to the note-taking frame
        tk.Label(self.note_frame, text="Notes", font=("Arial", 14), bg="lightgray").pack(pady=10)
        self.note_text = tk.Text(self.note_frame, wrap="word", height=20)
        self.note_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Add widgets to the PDF display frame
        tk.Label(self.pdf_frame, text="PDF Viewer", font=("Arial", 14), bg="white").pack(pady=10)
        self.pdf_display = tk.Text(self.pdf_frame, wrap="word", height=20, state="disabled", bg="white")
        self.pdf_display.pack(expand=True, fill="both", padx=10, pady=10)

        # Add a Back button to navigate to the MainMenu
        back_btn = tk.Button(self, text="Back to Main Menu", width=20, command=lambda: controller.show_frame(MainMenu))
        back_btn.grid(row=2, column=0, columnspan=2, pady=10)  # Place it below the frames

    # Placeholder methods for button commands
    def load_pdf(self):
        print("Load PDF clicked")

    def highlight_sections(self):
        print("Highlight Sections clicked")

    def create_note_hierarchy(self):
        print("Create Note Hierarchy clicked")

    def save_notes(self):
        print("Save Notes clicked")

    def load_notes(self):
        print("Load Notes clicked")

    def delete_all_notes(self):
        print("Delete All Notes clicked")


class ServerSetupScreen(tk.Frame):
=======
        # Make the parent frame (self) expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a container to hold all widgets
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")  # Center the container, not working

        # Configure the container to center its content (STILL NOT CENTERING)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Add widgets to the container
        label = tk.Label(container, text="Welcome to ARA", font=("Arial", 20))
        label.grid(row=0, column=0, pady=30)

        notes_btn = tk.Button(container, text="Notes", width=20, command=lambda: controller.show_frame(Notes))
        notes_btn.grid(row=1, column=0, pady=10)

        server_btn = tk.Button(container, text="Server Setup", width=20, command=lambda: controller.show_frame(ServerSetup))
        server_btn.grid(row=2, column=0, pady=10)

        about_btn = tk.Button(container, text="About", width=20, command=lambda: controller.show_frame(About))
        about_btn.grid(row=3, column=0, pady=10)

        # Ensure the container itself is centered within the parent frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Notes(tk.Frame):   #need to create a colum for taking notes, and then column for the PDF
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Notes Page", font=("Arial", 16))
        label.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)

        # Box for note entry for now, but will have to be changed later 
        note_entry = tk.Text(self, height=15, width=80)
        note_entry.pack(pady=20)


class ServerSetup(tk.Frame):
>>>>>>> Stashed changes
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Server Setup Page", font=("Arial", 16))
        label.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)

<<<<<<< Updated upstream
        # Placeholder server setup info
=======
        # Placeholder server setup info, will input later
>>>>>>> Stashed changes
        instructions = tk.Label(self, text="Instructions or fields for setting up the server will go here.")
        instructions.pack(pady=10)


<<<<<<< Updated upstream
class AboutScreen(tk.Frame):
=======
class About(tk.Frame):
>>>>>>> Stashed changes
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="About ARA", font=("Arial", 16))
        label.pack(pady=20)

        description = tk.Label(
            self,
<<<<<<< Updated upstream
            text="ARA helps students actively read using the SQ3R method.\nSurvey, Question, Read, Recite, Review.\n How it works",
=======
            text="ARA helps students actively read using the SQ3R method.\nSurvey, Question, Read, Recite, Review.",
>>>>>>> Stashed changes
            justify="center"
        )
        description.pack(pady=10)

        back_btn = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)


# Run the application
if __name__ == "__main__":
    app = ARA()
    app.mainloop()
