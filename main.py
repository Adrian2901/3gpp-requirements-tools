import json
import tkinter as tk
from tkinter import ttk
from requirements_gui import RequirementsGenerator
from std_retriever_gui import StdRetriever

if __name__ == "__main__":
    # File path for the configuration file
    CONFIG_FILE = "config.json"

    # Load the configuration from the JSON file
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Create the main window
    root = tk.Tk()
    root.title(config.get("title", "Generate Requirements"))

    root.geometry("700x400")

    # Create a tabbed interface
    tabControl = ttk.Notebook(root)
    tab1 = RequirementsGenerator(root, config).frame
    tabControl.add(tab1, text='Generate Requirements')
    tab2 = StdRetriever(root, config).frame
    tabControl.add(tab2, text='Download Standards')
    tabControl.pack(expand=1, fill="both")

    # Run the application
    root.mainloop()