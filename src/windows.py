import tkinter as tk
from tkinter import ttk

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

        label = tk.Label(self, text="Welcome to ARA", font=("Arial", 20))
        label.pack(pady=30)

        notes_btn = tk.Button(self, text="Notes", width=20, command=lambda: controller.show_frame(NotesScreen))
        notes_btn.pack(pady=10)

        server_btn = tk.Button(self, text="Server Setup", width=20, command=lambda: controller.show_frame(ServerSetupScreen))
        server_btn.pack(pady=10)

        about_btn = tk.Button(self, text="About", width=20, command=lambda: controller.show_frame(AboutScreen))
        about_btn.pack(pady=10)


class NotesScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Notes Page", font=("Arial", 16))
        label.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)

        # Placeholder note entry
        note_entry = tk.Text(self, height=15, width=80)
        note_entry.pack(pady=20)


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
            text="ARA helps students actively read using the SQ3R method.\nSurvey, Question, Read, Recite, Review.",
            justify="center"
        )
        description.pack(pady=10)

        back_btn = tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MainMenu))
        back_btn.pack(pady=10)


# Run the application
if __name__ == "__main__":
    app = ARA()
    app.mainloop()
