import json
import os
import tkinter as tk
from tkinter import ttk
import filter_docs

# File path for the configuration file
CONFIG_FILE = "config.json"

# Function to load the configuration from the JSON file
def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config


# Load configuration
config = load_config()

# Create the main window
root = tk.Tk()
root.title(config.get("title", "Generate Requirements"))

ip_var=tk.StringVar(value="localhost:11435")
path_var=tk.StringVar(value=config['folder_path'])
output_var=tk.StringVar(value=config['latency_paragraphs'])
keyword_var=tk.StringVar(value=' '.join(config['keywords']).replace(" ", ","))
model_var=config['model_name']

def run():
    status_label.config(text="Running...")
    root.update()
    config = {
        'llm_address': ip_var.get(),
        'folder_path': path_var.get(),
        'latency_paragraphs': output_var.get(),
        'keywords': keyword_var.get().split(","),
        'ignored_sections': ["References", "Appendix", "Definitions", "Abbreviations"],
        'model_name': model_var,
        'verbose': False
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    filter_docs.execute_filtering(config)
    status_label.config(text="Done! Check the output folder for the results.")

def on_model_select(event):
    model_var = combo_box.get()

# Set window size
width = config.get("width", 500)
height = config.get("height", 350)
root.geometry(f"{width}x{height}")

ip_label = tk.Label(root, text = 'LLM address:port', font=('arial',10))
ip_entry = tk.Entry(root,textvariable = ip_var, font=('arial',10,'normal'), width=50)

path_label = tk.Label(root, text = 'Input folder path', font=('arial',10))
path_entry = tk.Entry(root,textvariable = path_var, font=('arial',10,'normal'), width=50)

output_label = tk.Label(root, text = 'Output file path', font = ('arial',10,'normal'))
output_entry=tk.Entry(root, textvariable = output_var, font = ('arial',10,'normal'), width=50)

keyword_label = tk.Label(root, text = 'Keywords', font = ('arial',10,'normal'))
keyword_entry=tk.Entry(root, textvariable = keyword_var, font = ('arial',10,'normal'), width=50)

model_label = tk.Label(root, text = 'Language Model', font = ('arial',10,'normal'))
model_entry=ttk.Combobox(root, values=["llama3.1", "llama3.1:70b", "llama3.1:405b"], width=55)
model_entry.set(model_var)

run_btn=tk.Button(root,text = 'Run', command = run, width=30)

status_label = tk.Label(root, text = '', font = ('arial',10,'normal'))

ip_label.grid(row=0,column=0, padx=5)
ip_entry.grid(row=0,column=1, pady=10)
model_label.grid(row=1,column=0, padx=5)
model_entry.grid(row=1,column=1, pady=10)
path_label.grid(row=2,column=0, padx=5)
path_entry.grid(row=2,column=1, pady=10)
output_label.grid(row=3,column=0, padx=5)
output_entry.grid(row=3,column=1, pady=10)
keyword_label.grid(row=4,column=0, padx=5)
keyword_entry.grid(row=4,column=1, pady=10)

run_btn.grid(row=5,column=1)
status_label.grid(row=6,column=1)

# Run the application
root.mainloop()