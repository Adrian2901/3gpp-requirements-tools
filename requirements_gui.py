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
        ip_var=tk.StringVar(value="localhost:11435")
        path_var=tk.StringVar(value=config['folder_path'])
        output_var=tk.StringVar(value=config['output_folder_path'])
        keyword_var=tk.StringVar(value=' '.join(config['keywords']).replace(" ", ","))
        model_var=config['model_name']

        # LLM IP address and port input in the GUI
        ip_label = tk.Label(self.frame, text = 'LLM address:port', font=('arial',10))
        ip_entry = tk.Entry(self.frame, textvariable = ip_var, font=('arial',10,'normal'), width=70)

        # Input path input in the GUI
        path_label = tk.Label(self.frame, text = 'Input folder path', font=('arial',10))
        path_entry = tk.Entry(self.frame, textvariable = path_var, font=('arial',10,'normal'), width=70)
        path_btn=tk.Button(self.frame,text = '...', command = self.select_path_dir, width=10)

        # Output path input in the GUI
        output_label = tk.Label(self.frame, text = 'Output folder path', font = ('arial',10,'normal'))
        output_entry=tk.Entry(self.frame, textvariable = output_var, font = ('arial',10,'normal'), width=70)
        output_btn=tk.Button(self.frame,text = '...', command = self.select_output_dir, width=10)

        # Keywords input in the GUI
        keyword_label = tk.Label(self.frame, text = 'Keywords', font = ('arial',10,'normal'))
        keyword_entry=tk.Entry(self.frame, textvariable = keyword_var, font = ('arial',10,'normal'), width=70)

        # Model selection in the GUI
        model_label = tk.Label(self.frame, text = 'Language Model', font = ('arial',10,'normal'))
        model_entry=ttk.Combobox(self.frame, values=["llama3.1", "llama3.1:70b", "llama3.1:405b"], width=79)
        model_entry.set(model_var)

        # Unit selection in the GUI
        unit_label = tk.Label(self.frame, text = 'Units', font = ('arial',10,'normal'))
        unit_frame = tk.Frame(self.frame)

        unit_vars = {}  # Dictionary to store BooleanVar for each unit
        # Create a checkbox for each unit type in the config
        col = 0
        for unit_name in config['units']:
            unit_var = tk.BooleanVar(value=unit_name in config.get('checked_units', []))
            unit_vars[unit_name] = unit_var
            unit_checkbox = tk.Checkbutton(unit_frame, text=unit_name, variable=unit_var)
            unit_checkbox.grid(row=0, column=col, padx=25)
            col += 1

        run_btn=tk.Button(self.frame,text = 'Run', command = self.run, width=30)
        status_label = tk.Label(self.frame, text = '', font = ('arial',10,'normal'))
        progressbar = ttk.Progressbar(self.frame, length=500)

        # Place the widgets on the window grid
        ip_label.grid(row=0,column=0, padx=5)
        ip_entry.grid(row=0,column=1, pady=10)
        model_label.grid(row=1,column=0, padx=5)
        model_entry.grid(row=1,column=1, pady=10)
        path_label.grid(row=2,column=0, padx=5)
        path_entry.grid(row=2,column=1, pady=10)
        path_btn.grid(row=2,column=2, pady=10)
        output_label.grid(row=3,column=0, padx=5)
        output_entry.grid(row=3,column=1, pady=10)
        output_btn.grid(row=3,column=2, pady=10)
        keyword_label.grid(row=4,column=0, padx=5)
        keyword_entry.grid(row=4,column=1, pady=10)
        unit_label.grid(row=5, column=0, padx=5)
        unit_frame.grid(row=5, column=1, pady=10)
        run_btn.grid(row=6,column=1)
        status_label.grid(row=7,column=1)

    # Function to save the configuration to the JSON file
    def save_config():
        checked_units = [unit for unit, var in unit_vars.items() if var.get()]
        config = {
            'llm_address': ip_var.get(),
            'folder_path': path_var.get(),
            'output_folder_path': output_var.get(),
            'keywords': keyword_var.get().split(","),
            'ignored_sections': ["References", "Appendix", "Definitions", "Abbreviations"],
            'model_name': model_var,
            'verbose': False,
            'download_folder_path': download_dir_var.get(),
            'phrase': search_keyword_var.get(),
            'series_no': series_var.get(),
            'units': {
                "ms": "\\b\\d+\\s*ms\\b\\.?",
                "percent": "\\b\\d+\\s*%\\b\\.?",
                "kbps": "\\b\\d+\\s*kbps\\b\\.?"
            },
            'checked_units': checked_units
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return config

    # Function to update the status label and progress bar
    def update_status(message, progress=None):
        status_label.config(text=message)
        if progress is not None:
            progressbar.grid(row=8,column=1)
            progressbar.config(value=progress*100)
        else:
            progressbar.grid_forget()
        root.update()

    # Function to start the filtering on button press
    def run():
        run_btn.config(state=tk.DISABLED)
        update_status("Starting the filtering...")
        config = save_config()
        try:
            # Function to run on a separate thread
            def run_tasks():
                filter_docs.execute_filtering(config, update_status)
                generate_req.generate_req(config, update_status)
                csv2xlsx.csv_to_xlsx(config, update_status)
                run_btn.config(state=tk.NORMAL)
            # Start the thread
            task_thread = threading.Thread(target=run_tasks)
            task_thread.start()
        except Exception as e:
            print(e)
            update_status("An error occurred! Please try again.")

    def on_model_select(event):
        model_var = combo_box.get()

    def select_path_dir():
        path_var = filedialog.askdirectory()
        path_entry.delete(0, tk.END)
        path_entry.insert(0, path_var)

    def select_output_dir():
        output_var = filedialog.askdirectory()
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_var)

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