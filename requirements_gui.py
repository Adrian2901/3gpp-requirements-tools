import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
import filter_docs
import generate_req
import csv2xlsx
import threading


class RequirementsGenerator:
    def __init__(self, root, config):
        self.frame = ttk.Frame(root)
        self.config = config

        # Get the values from the config files
        self.ip_var=tk.StringVar(value="localhost:11435")
        self.path_var=tk.StringVar(value=config['folder_path'])
        self.output_var=tk.StringVar(value=config['output_folder_path'])
        self.keyword_var=tk.StringVar(value=' '.join(config['keywords']).replace(" ", ","))
        self.model_var=config['model_name']

        # LLM IP address and port input in the GUI
        self.ip_label = tk.Label(self.frame, text = 'LLM address:port', font=('arial',10))
        self.ip_entry = tk.Entry(self.frame, textvariable = self.ip_var, font=('arial',10,'normal'), width=70)

        # Input path input in the GUI
        self.path_label = tk.Label(self.frame, text = 'Input folder path', font=('arial',10))
        self.path_entry = tk.Entry(self.frame, textvariable = self.path_var, font=('arial',10,'normal'), width=70)
        self.path_btn=tk.Button(self.frame,text = '...', command = self.select_path_dir, width=10)

        # Output path input in the GUI
        self.output_label = tk.Label(self.frame, text = 'Output folder path', font = ('arial',10,'normal'))
        self.output_entry=tk.Entry(self.frame, textvariable = self.output_var, font = ('arial',10,'normal'), width=70)
        self.output_btn=tk.Button(self.frame,text = '...', command = self.select_output_dir, width=10)

        # Keywords input in the GUI
        self.keyword_label = tk.Label(self.frame, text = 'Keywords', font = ('arial',10,'normal'))
        self.keyword_entry=tk.Entry(self.frame, textvariable = self.keyword_var, font = ('arial',10,'normal'), width=70)

        # Model selection in the GUI
        self.model_label = tk.Label(self.frame, text = 'Language Model', font = ('arial',10,'normal'))
        self.model_entry=ttk.Combobox(self.frame, values=["llama3.1", "llama3.1:70b", "llama3.1:405b"], width=79)
        self.model_entry.set(self.model_var)

        # Unit selection in the GUI
        self.unit_label = tk.Label(self.frame, text = 'Units', font = ('arial',10,'normal'))
        self.unit_frame = tk.Frame(self.frame)

        self.unit_vars = {}  # Dictionary to store BooleanVar for each unit
        # Create a checkbox for each unit type in the config
        col = 0
        for unit_name in config['units']:
            unit_var = tk.BooleanVar(value=unit_name in config.get('checked_units', []))
            self.unit_vars[unit_name] = unit_var
            self.unit_checkbox = tk.Checkbutton(self.unit_frame, text=unit_name, variable=unit_var)
            self.unit_checkbox.grid(row=0, column=col, padx=25)
            col += 1

        self.run_btn=tk.Button(self.frame,text = 'Run', command = self.run, width=30)
        self.status_label = tk.Label(self.frame, text = '', font = ('arial',10,'normal'))
        self.progressbar = ttk.Progressbar(self.frame, length=500)

        # Place the widgets on the window grid
        self.ip_label.grid(row=0,column=0, padx=5)
        self.ip_entry.grid(row=0,column=1, pady=10)
        self.model_label.grid(row=1,column=0, padx=5)
        self.model_entry.grid(row=1,column=1, pady=10)
        self.path_label.grid(row=2,column=0, padx=5)
        self.path_entry.grid(row=2,column=1, pady=10)
        self.path_btn.grid(row=2,column=2, pady=10)
        self.output_label.grid(row=3,column=0, padx=5)
        self.output_entry.grid(row=3,column=1, pady=10)
        self.output_btn.grid(row=3,column=2, pady=10)
        self.keyword_label.grid(row=4,column=0, padx=5)
        self.keyword_entry.grid(row=4,column=1, pady=10)
        self.unit_label.grid(row=5, column=0, padx=5)
        self.unit_frame.grid(row=5, column=1, pady=10)
        self.run_btn.grid(row=6,column=1)
        self.status_label.grid(row=7,column=1)

    # Function to save the configuration to the JSON file
    def save_config(self):
        checked_units = [unit for unit, var in self.unit_vars.items() if var.get()]
        self.config['llm_address'] = self.ip_var.get()
        self.config['folder_path'] = self.path_var.get()
        self.config['output_folder_path'] = self.output_var.get()
        self.config['keywords'] = self.keyword_var.get().split(",")
        self.config['model_name'] = self.model_var
        self.config['checked_units'] = checked_units

        with open('config.json', 'w') as f:
            json.dump(self.config, f)
        return self.config

    # Function to update the status label and progress bar
    def update_status(self, message, progress=None):
        self.status_label.config(text=message)
        if progress is not None:
            self.progressbar.grid(row=8,column=1)
            self.progressbar.config(value=progress*100)
        else:
            self.progressbar.grid_forget()

    # Function to start the filtering on button press
    def run(self):
        self.run_btn.config(state=tk.DISABLED)
        self.update_status("Starting the filtering...")
        self.config = self.save_config()
        try:
            # Function to run on a separate thread
            def run_tasks():
                filter_docs.execute_filtering(self.config, self.update_status)
                generate_req.generate_req(self.config, self.update_status)
                csv2xlsx.csv_to_xlsx(self.config, self.update_status)
                self.run_btn.config(state=tk.NORMAL)
            # Start the thread
            task_thread = threading.Thread(target=run_tasks)
            task_thread.start()
        except Exception as e:
            print(e)
            update_status("An error occurred! Please try again.")

    def on_model_select(self, event):
        self.model_var = self.combo_box.get()

    def select_path_dir(self):
        dir = filedialog.askdirectory()
        self.path_var.set(dir)
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, dir)

    def select_output_dir(self):
        dir = filedialog.askdirectory()
        self.output_var.set(dir)
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, dir)

if __name__ == "__main__":
    # File path for the configuration file
    CONFIG_FILE = "config.json"

    # Load the configuration from the JSON file
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Create the main window
    root = tk.Tk()
    root.title(config.get("title", "Generate Requirements"))
    requirements_gui = RequirementsGenerator(root, config)
    requirements_gui.frame.pack(expand=True, fill="both")

    # Set window size
    root.geometry("700x400")

    # Run the application
    root.mainloop()