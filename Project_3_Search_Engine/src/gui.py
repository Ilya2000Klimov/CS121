import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import from Pillow
import pyprojroot
root = pyprojroot.here()
root = root/'Project_3_Search_Engine'
src = root/'src'
Test = root/'test'

from src.query import MongoDBSearch
from pymongo import MongoClient

class SearchEngineGUI:
    def __init__(self, root):
        self.search = MongoDBSearch()
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["searchEngine"]
        self.collection = self.db["DisplayDocuments"]
        self.ranked_docs = []
        
        
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
        self.main_frame.rowconfigure(2, weight=1)
        self.results_area.config(state=tk.DISABLED, bg='white')
        
        # Ensure that the main frame itself can expand within the root window
        self.root.rowconfigure(0, weight=1)  # This makes the first row of the root, which contains main_frame, expandable
        self.root.columnconfigure(0, weight=1)  # Make sure the column in the root window is also expandable

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
        ranked_docs = self.search.search(query)
        # Fetch additional information for each document from MongoDB
        ranked_results = []
        for doc in ranked_docs[:20]:
            #print(f"Found document {doc}")
            doc_id = doc[0]
            document = self.collection.find_one({"_id": doc_id})  # Assuming '_id' is used as the document ID in MongoDB
            if document:
                ranked_results.append(document)
        #print(ranked_results)
        self.display_results(ranked_results)

    def display_results(self, ranked_results):
        self.results_area.config(state=tk.NORMAL)
        self.results_area.delete(1.0, tk.END)

        # Define tag configurations for different parts of the result
        self.results_area.tag_configure('doc_id', foreground='grey')
        self.results_area.tag_configure('url', foreground='grey')
        self.results_area.tag_configure('title', foreground='blue', font=('Helvetica', 12, 'bold'))
        self.results_area.tag_configure('summary', wrap=tk.WORD)
        
        self.results_area.insert(tk.END, f"{len(self.ranked_docs)} results found\nSearch Results\n", 'title')
        
        # Display only the top 20 results
        for result in ranked_results[:20]:
            doc_id = result.get('doc_id', '')
            url = result.get('url', '')
            title = result.get('title', 'No Title')
            summary = result.get('summary', 'No Summary')

            # Insert each part of the result with its respective tag for styling
            self.results_area.insert(tk.END, f'{doc_id}\n', 'doc_id')
            self.results_area.insert(tk.END, f'{url}\n', 'url')
            self.results_area.insert(tk.END, f'{title}\n', 'title')
            self.results_area.insert(tk.END, f'{summary}\n\n', 'summary')

        self.results_area.config(state=tk.DISABLED)