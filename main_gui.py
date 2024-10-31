import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
import filter_docs
import generate_req

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
if "latency_paragraphs.csv" in config['latency_paragraphs']:
    config['latency_paragraphs'] = config['latency_paragraphs'].replace("/latency_paragraphs.csv", "")
output_var=tk.StringVar(value=config['latency_paragraphs'])
keyword_var=tk.StringVar(value=' '.join(config['keywords']).replace(" ", ","))
model_var=config['model_name']

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Generate Requirements')
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Download Standards')
tabControl.pack(expand=1, fill="both")

def run():
    status_label.config(text="Filtering the documents...")
    root.update()
    config = {
        'llm_address': ip_var.get(),
        'folder_path': path_var.get(),
        'latency_paragraphs': output_var.get() + "/latency_paragraphs.csv",
        'keywords': keyword_var.get().split(","),
        'ignored_sections': ["References", "Appendix", "Definitions", "Abbreviations"],
        'model_name': model_var,
        'verbose': False
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    try:
        filter_docs.execute_filtering(config)
        status_label.config(text="Generating requirements...")
        root.update()
        generate_req.generate_req(config)
        status_label.config(text="Done! Check the output folder for the results.")
    except Exception as e:
        status_label.config(text=f"An error occurred! Please try again.")

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

# Set window size
width = config.get("width", 700)
height = config.get("height", 350)
root.geometry(f"{width}x{height}")

ip_label = tk.Label(tab1, text = 'LLM address:port', font=('arial',10))
ip_entry = tk.Entry(tab1, textvariable = ip_var, font=('arial',10,'normal'), width=70)

path_label = tk.Label(tab1, text = 'Input folder path', font=('arial',10))
path_entry = tk.Entry(tab1, textvariable = path_var, font=('arial',10,'normal'), width=70)
path_btn=tk.Button(tab1,text = '...', command = select_path_dir, width=10)

output_label = tk.Label(tab1, text = 'Output folder path', font = ('arial',10,'normal'))
output_entry=tk.Entry(tab1, textvariable = output_var, font = ('arial',10,'normal'), width=70)
output_btn=tk.Button(tab1,text = '...', command = select_output_dir, width=10)

keyword_label = tk.Label(tab1, text = 'Keywords', font = ('arial',10,'normal'))
keyword_entry=tk.Entry(tab1, textvariable = keyword_var, font = ('arial',10,'normal'), width=70)

model_label = tk.Label(tab1, text = 'Language Model', font = ('arial',10,'normal'))
model_entry=ttk.Combobox(tab1, values=["llama3.1", "llama3.1:70b", "llama3.1:405b"], width=79)
model_entry.set(model_var)

run_btn=tk.Button(tab1,text = 'Run', command = run, width=30)

status_label = tk.Label(tab1, text = '', font = ('arial',10,'normal'))

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

run_btn.grid(row=5,column=1)
status_label.grid(row=6,column=1)

def download():
    status2_label.config(text="Downloading the standards...")
    root.update()
    # TODO: Implement the download function
    status2_label.config(text="Done! Check the output folder for the results.")

def select_download_dir():
    download_dir_var = filedialog.askdirectory()
    download_dir_entry.delete(0, tk.END)
    download_dir_entry.insert(0, download_dir_var)

series_var=tk.StringVar()
search_keyword_var=tk.StringVar()
download_dir_var=tk.StringVar()

series_label = tk.Label(tab2, text = 'Series number', font=('arial',10))
series_entry = tk.Entry(tab2, textvariable = series_var, font=('arial',10,'normal'), width=70)

search_keyword_label = tk.Label(tab2, text = 'Search keyword', font=('arial',10))
search_keyword_entry = tk.Entry(tab2, textvariable = search_keyword_var, font=('arial',10,'normal'), width=70)

download_dir_label = tk.Label(tab2, text = 'Output folder', font=('arial',10))
download_dir_entry = tk.Entry(tab2, textvariable = download_dir_var, font=('arial',10,'normal'), width=70)
download_dir_btn=tk.Button(tab2,text = '...', command = select_download_dir, width=10)

download_btn=tk.Button(tab2, text = 'Download', command = download, width=30)
status2_label = tk.Label(tab2, text = '', font = ('arial',10,'normal'))

series_label.grid(row=0,column=0, padx=5)
series_entry.grid(row=0,column=1, pady=10)
search_keyword_label.grid(row=1,column=0, padx=5)
search_keyword_entry.grid(row=1,column=1, pady=10)
download_dir_label.grid(row=2,column=0, padx=5)
download_dir_entry.grid(row=2,column=1, pady=10)
download_dir_btn.grid(row=2,column=2, pady=10)
download_btn.grid(row=3,column=1)
status2_label.grid(row=4,column=1)

# Run the application
root.mainloop()