"""
File: main.py
Description: This is the main.py script. Opens a gui with all different tools present.

Contributors:
David Schön
Adrian Hassa

Created: 2024-10-16
Last Modified: 2024-12-10

Project: 3GPP Requirement Tools
URL: https://github.com/Adrian2901/3gpp-requirements-tools

License: MIT License (see LICENSE file for details)
"""

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