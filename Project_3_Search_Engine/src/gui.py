import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import from Pillow
import pyprojroot
root = pyprojroot.here()
root = root/'Project_3_Search_Engine'
src = root/'src'
Test = root/'test'

class SearchEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UCI Search Engine")
        self.root.geometry("1280x720")  # Set initial size to HD 1280x720
        self.root.configure(background='white')
        self.root.update()  # Ensure the window size is updated

        self.main_frame = ttk.Frame(root, padding="10", style='My.TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)  # Make the main frame expandable

        # Load and display an image above the search bar
        self.load_and_display_image()

        # Inner frame to hold the search bar and button, centered in the main frame
        self.search_frame = ttk.Frame(self.main_frame, style='My.TFrame')
        self.search_frame.grid(row=1, column=0, pady=10)  # Center the frame in the main frame
        self.search_frame.columnconfigure(0, weight=1)  # Make the main frame expandable

        style = ttk.Style()
        style.configure('My.TFrame', background='white')
        style.configure('TEntry', borderwidth=2, relief="sunken", background="white")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, width=50, textvariable=self.search_var, style='TEntry')
        self.search_entry.grid(row=0, column=0, padx=5)  # Place the search bar in the search frame
        self.search_entry.focus()
        
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

        style.configure('TButton', background='white', foreground='black')
        style.map('Hover.TButton', foreground=[('active', 'blue')])

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.perform_search, style='TButton')
        self.search_button.grid(row=0, column=1, padx=5)  # Place the button next to the search bar in the search frame

        self.results_area = tk.Text(self.main_frame, height=15, width=60, wrap=tk.WORD, borderwidth=0, relief="flat")
        self.results_area.grid(row=2, column=0, pady=10, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))  # Make the results area expand with the window
        self.main_frame.columnconfigure(0, weight=1)  # Allow the column containing the results area to expand
        self.results_area.config(state=tk.DISABLED, bg='white')

    def load_and_display_image(self):
        # Open the image using Pillow
        image_path = src / "AntEater.png"  # Ensure this is the correct path to your transparent image
        original_image = Image.open(image_path)

        # Calculate the target width as 30% of the window's width
        target_width = int(self.root.winfo_width() * 0.3)
        # Calculate the target height to maintain the aspect ratio
        aspect_ratio = original_image.height / original_image.width
        target_height = int(target_width * aspect_ratio)

        # Resize the image to the target size while maintaining aspect ratio
        resized_image = original_image.resize((target_width, target_height), Image.Resampling.LANCZOS)


        # Convert the resized image to a format that Tkinter can use (Preserve transparency)
        photo = ImageTk.PhotoImage(resized_image)

        # Create a label to display the image and place it above the search bar
        image_label = ttk.Label(self.main_frame, image=photo, background='white')
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))  # Ensure proper padding to separate from the search bar


    def perform_search(self):
        query = self.search_var.get()
        self.display_results(f"Results for '{query}' would be displayed here.")

    def display_results(self, results_text):
        self.results_area.config(state=tk.NORMAL)
        self.results_area.delete(1.0, tk.END)
        self.results_area.insert(tk.END, results_text)
        self.results_area.config(state=tk.DISABLED)