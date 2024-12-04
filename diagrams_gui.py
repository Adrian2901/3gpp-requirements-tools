import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
import process_images
import threading
import sys

# Change the working directory to the directory of the executable for PyInstaller
os.chdir(sys._MEIPASS) if getattr(sys, 'frozen', False) else os.chdir(os.path.dirname(os.path.abspath(__file__)))

class DiagramProcessor:
    def __init__(self, parent, config):
        self.frame = ttk.Frame(parent)
        self.config = config
        self.ip_var=tk.StringVar(value=config['llm_address'])
        self.input_var = tk.StringVar(value="test_files/23502-i20_l.docx")
        self.output_var = tk.StringVar(value="diagrams_output")

        # LLM IP address and port input in the GUI
        self.ip_label = tk.Label(self.frame, text = 'LLM address:port', font=('arial',10))
        self.ip_entry = tk.Entry(self.frame, textvariable = self.ip_var, font=('arial',10,'normal'), width=70)

        self.input_label = tk.Label(self.frame, text = 'Input file', font=('arial',10))
        self.input_entry = tk.Entry(self.frame, textvariable = self.input_var, font=('arial',10,'normal'), width=70)
        self.input_btn=tk.Button(self.frame,text = '...', command = self.select_input_file, width=10)

        self.output_dir_label = tk.Label(self.frame, text = 'Output folder', font=('arial',10))
        self.output_dir_entry = tk.Entry(self.frame, textvariable = self.output_var, font=('arial',10,'normal'), width=70)
        self.output_dir_btn=tk.Button(self.frame,text = '...', command = self.select_output_dir, width=10)

        self.run_btn=tk.Button(self.frame, text = 'Download', command = self.run, width=30)
        self.status_label = tk.Label(self.frame, text = '', font = ('arial',10,'normal'))

        self.progressbar = ttk.Progressbar(self.frame, length=500)

        # Place the widgets on the window grid
        self.ip_label.grid(row=0,column=0, padx=5)
        self.ip_entry.grid(row=0,column=1, pady=10)

        self.input_label.grid(row=1,column=0, padx=5)
        self.input_entry.grid(row=1,column=1, pady=10)
        self.input_btn.grid(row=1,column=2, pady=10)

        self.output_dir_label.grid(row=2,column=0, padx=5)
        self.output_dir_entry.grid(row=2,column=1, pady=10)
        self.output_dir_btn.grid(row=2,column=2, pady=10)

        self.run_btn.grid(row=3,column=1)
        self.status_label.grid(row=4,column=1)
        

    # Callback function to update the download status
    def update_status(self, message, progress=None):
        self.status_label.config(text=message)
        if progress is not None:
            self.progressbar.grid(row=5,column=1)
            self.progressbar.config(value=progress*100)
        else:
            self.progressbar.grid_forget()

    # Function to start the download on button press
    def run(self):
        self.update_status("Reading the document...")
        threading.Thread(target=process_images.process_docx, args=(self.input_var.get(), self.output_var.get(), self.ip_var.get(), self.update_status)).start()

    # File selection dialog
    def select_input_file(self):
        file = filedialog.askopenfilename(filetypes=[("Microsoft Word document", ".docx")])
        self.input_var.set(file)
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file)
        
    # Directory selection dialog
    def select_output_dir(self):
        dir = filedialog.askdirectory()
        self.output_var.set(dir)
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, dir)

if __name__ == "__main__":
    # File path for the configuration file
    CONFIG_FILE = 'config.json'

    # Function to load the configuration from the JSON file
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Create the main window
    root = tk.Tk()
    root.title(config.get("title", "Extract Text from Diagrams"))
    diagrams_gui = DiagramProcessor(root, config)
    diagrams_gui.frame.pack(expand=True, fill="both")

    root.geometry("700x400")

    # Run the application
    root.mainloop()