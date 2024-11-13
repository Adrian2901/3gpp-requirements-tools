import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
import std_retriever
import threading

class StdRetriever:
    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)
        self.config = config
        series_var=tk.StringVar(value=config['series_no'])
        search_keyword_var=tk.StringVar(value=config['phrase'])
        download_dir_var=tk.StringVar(value=config['download_folder_path'])

        series_label = tk.Label(self.frame, text = 'Series number', font=('arial',10))
        series_entry = tk.Entry(self.frame, textvariable = series_var, font=('arial',10,'normal'), width=70)

        search_keyword_label = tk.Label(self.frame, text = 'Search keyword', font=('arial',10))
        search_keyword_entry = tk.Entry(self.frame, textvariable = search_keyword_var, font=('arial',10,'normal'), width=70)

        download_dir_label = tk.Label(self.frame, text = 'Output folder', font=('arial',10))
        download_dir_entry = tk.Entry(self.frame, textvariable = download_dir_var, font=('arial',10,'normal'), width=70)
        download_dir_btn=tk.Button(self.frame,text = '...', command = self.select_download_dir, width=10)

        download_btn=tk.Button(self.frame, text = 'Download', command = self.download, width=30)
        status_label = tk.Label(self.frame, text = '', font = ('arial',10,'normal'))

        # Place the widgets on the window grid
        series_label.grid(row=0,column=0, padx=5)
        series_entry.grid(row=0,column=1, pady=10)
        search_keyword_label.grid(row=1,column=0, padx=5)
        search_keyword_entry.grid(row=1,column=1, pady=10)
        download_dir_label.grid(row=2,column=0, padx=5)
        download_dir_entry.grid(row=2,column=1, pady=10)
        download_dir_btn.grid(row=2,column=2, pady=10)
        download_btn.grid(row=3,column=1)
        status_label.grid(row=4,column=1)

    # Function to save the configuration to the JSON file
    def save_config():
        config['download_folder_path'] = download_dir_var.get()
        config['phrase'] = search_keyword_var.get()
        config['series_no'] = series_var.get()
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return config

    # Callback function to update the download status
    def update_download_status(message):
        status_label.config(text=message)
        root.update()

    # Function to start the download on button press
    def download():
        status_label.config(text="Processing the standards...")
        root.update()
        config = save_config()
        threading.Thread(target=std_retriever.download, args=(config, download_btn, update_download_status)).start()
        
    # Directory selection dialog
    def select_download_dir():
        download_dir_var = filedialog.askdirectory()
        download_dir_entry.delete(0, tk.END)
        download_dir_entry.insert(0, download_dir_var)

if __name__ == "__main__":
    # File path for the configuration file
    CONFIG_FILE = "config.json"

    # Function to load the configuration from the JSON file
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Create the main window
    root = tk.Tk()
    root.title(config.get("title", "Download Standards"))
    std_retriever = StdRetriever(root, config)
    std_retriever.frame.pack(expand=True, fill="both")

    root.geometry("700x400")

    # Run the application
    root.mainloop()