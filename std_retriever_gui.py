import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
import std_retriever
import threading
import sys

# Change the working directory to the directory of the executable for PyInstaller
os.chdir(sys._MEIPASS) if getattr(sys, 'frozen', False) else os.chdir(os.path.dirname(os.path.abspath(__file__)))

class StdRetriever:
    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)
        self.config = config
        self.series_var = tk.StringVar(value=config['series_no'])
        self.search_keyword_var = tk.StringVar(value=config['phrase'])
        self.download_dir_var = tk.StringVar(value=config['download_folder_path'])
        self.tr_var = tk.BooleanVar(value=True)
        self.ts_var = tk.BooleanVar(value=True)

        self.series_label = tk.Label(self.frame, text = 'Series number', font=('arial',10))
        self.series_entry = tk.Entry(self.frame, textvariable = self.series_var, font=('arial',10,'normal'), width=70)

        self.search_keyword_label = tk.Label(self.frame, text = 'Search keyword', font=('arial',10))
        self.search_keyword_entry = tk.Entry(self.frame, textvariable = self.search_keyword_var, font=('arial',10,'normal'), width=70)

        self.type_label = tk.Label(self.frame, text = 'Type', font = ('arial',10,'normal'))
        self.type_frame = tk.Frame(self.frame)

        self.tr_checkbox = tk.Checkbutton(self.type_frame, text='Technical Report', variable=self.tr_var, command=self.update_checked)
        self.ts_checkbox = tk.Checkbutton(self.type_frame, text='Technical Specification', variable=self.ts_var, command=self.update_checked)
        self.tr_checkbox.grid(row=0, column=0, padx=25)
        self.ts_checkbox.grid(row=0, column=1, padx=25)

        self.download_dir_label = tk.Label(self.frame, text = 'Output folder', font=('arial',10))
        self.download_dir_entry = tk.Entry(self.frame, textvariable = self.download_dir_var, font=('arial',10,'normal'), width=70)
        self.download_dir_btn=tk.Button(self.frame,text = '...', command = self.select_download_dir, width=10)

        self.download_btn=tk.Button(self.frame, text = 'Download', command = self.download, width=30)
        self.status_label = tk.Label(self.frame, text = '', font = ('arial',10,'normal'))

        # Place the widgets on the window grid
        self.series_label.grid(row=0,column=0, padx=5)
        self.series_entry.grid(row=0,column=1, pady=10)
        self.search_keyword_label.grid(row=1,column=0, padx=5)
        self.search_keyword_entry.grid(row=1,column=1, pady=10)
        self.type_label.grid(row=2,column=0, padx=5)
        self.type_frame.grid(row=2,column=1, pady=10)
        self.download_dir_label.grid(row=3,column=0, padx=5)
        self.download_dir_entry.grid(row=3,column=1, pady=10)
        self.download_dir_btn.grid(row=3,column=2, pady=10)
        self.download_btn.grid(row=4,column=1)
        self.status_label.grid(row=5,column=1)

    # Function to save the configuration to the JSON file
    def save_config(self):
        self.config['download_folder_path'] = self.download_dir_var.get()
        self.config['phrase'] = self.search_keyword_var.get()
        self.config['series_no'] = self.series_var.get()
        self.config['type'] = self.update_checked()
        with open('config.json', 'w') as f:
            json.dump(self.config, f)
        return self.config

    # Callback function to update the download status
    def update_download_status(self, message):
        self.status_label.config(text=message)

    # Function to start the download on button press
    def download(self):
        self.status_label.config(text="Processing the standards...")
        config = self.save_config()
        threading.Thread(target=std_retriever.download, args=(config, self.download_btn, self.update_download_status)).start()
        
    def update_checked(self):
        checked = []
        if self.tr_var.get():
            checked.append("Technical Report (TR)")
        if self.ts_var.get():
            checked.append("Technical Specification (TS)")
        if len(checked) == 0:
            checked = ["Technical Report (TR)", "Technical Specification (TS)"]
        return checked

    # Directory selection dialog
    def select_download_dir(self):
        dir = filedialog.askdirectory()
        self.download_dir_var.set(dir)
        self.download_dir_entry.delete(0, tk.END)
        self.download_dir_entry.insert(0, dir)

if __name__ == "__main__":
    # File path for the configuration file
    CONFIG_FILE = 'config.json'

    # Function to load the configuration from the JSON file
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Create the main window
    root = tk.Tk()
    root.title(config.get("title", "Download Standards"))
    std_retriever_gui = StdRetriever(root, config)
    std_retriever_gui.frame.pack(expand=True, fill="both")

    root.geometry("700x400")

    # Run the application
    root.mainloop()