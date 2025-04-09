import tkinter as tk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Screen")
        self.root.geometry("300x200")

        # Add content to the main window
        main_label = tk.Label(self.root, text="This is the main screen!", font=("Arial", 14))
        main_label.pack(pady=50)

        switch_button = tk.Button(self.root, text="Switch Screen", command=self.switch_window)
        switch_button.pack()

    def switch_window(self):
        self.root.destroy()  # Close the current window
        self.open_second_window()  # Open the second window

    def open_second_window(self):
        second_window = tk.Tk()
        second_window.title("Second Screen")
        second_window.geometry("300x200")

        # Add content to the second window
        second_label = tk.Label(second_window, text="This is the second screen!", font=("Arial", 14))
        second_label.pack(pady=50)

        back_button = tk.Button(second_window, text="Back", command=lambda: self.back_to_main(second_window))
        back_button.pack()

        second_window.mainloop()

    def back_to_main(self, second_window):
        second_window.destroy()  # Close the second window
        root = tk.Tk()  # Reopen the main window
        MainWindow(root)  # Create a new main window instance
        root.mainloop()

# Create the main window
root = tk.Tk()

# Initialize the app with the root window
app = MainWindow(root)

# Run the application
root.mainloop()
