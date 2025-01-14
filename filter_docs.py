"""
File: filter_docs.py
Description: This scipt is part of the requirements generation. Filtering the documents 
for the requirements generation.

Contributors:
David Schön
Marcelo Santibáñez
Adrian Hassa

Created: 2024-09-29
Last Modified: 2024-12-10

Project: 3GPP Requirement Tools
URL: https://github.com/Adrian2901/3gpp-requirements-tools

License: MIT License (see LICENSE file for details)
"""

import os
import csv
from docx import Document
import requests
import json
import re
from doc2docx import convert
import sys

# Change the working directory to the directory of the executable
os.chdir(sys._MEIPASS) if getattr(sys, 'frozen', False) else os.chdir(os.path.dirname(os.path.abspath(__file__)))

def ask_llm(paragraph, filter_word, model, llm_ip):
    '''
    Ask the LLM model to determine if the paragraph contains enough information to generate a requirement.
    :param paragraph: The paragraph to be analyzed
    :param filter_word: The word to be used as a filter
    :return: The response from the LLM model; either "NO" or "POSSIBLE"
    '''
    # Replace {parameter} with the desired term (e.g., "latency"), and setup what we need to send the request (url, data, and headers)
    prompt_text = prompts['verify_context'].replace("{parameter}", filter_word) + paragraph
    url = f'http://{llm_ip}/api/generate'
    data = {
        "model": model,
        "prompt": prompt_text,
        "stream": False
        }
    headers = {'Content-Type': 'application/json'}
    
    # Send the request to the LLM model, extract the response from the JSON data and return it
    response = requests.post(url, data=json.dumps(data), headers=headers)
    json_data = json.loads(response.text)
    return json_data['response']

def extract_paragraphs_with_keywords(doc, filename, config):
    '''
    Extract paragraphs from a document that contain any of the keywords and are not in the ignored sections.
    :param doc: The document to be analyzed
    :param keywords: A list of keywords to search for
    :param filename: The name of the file being processed
    :param config: The configuration dictionary
    :return: A list of paragraphs that contain any of the keywords and are not in the ignored sections
    '''
    paragraphs = []
    requirements = []
    # Get the keywords from the config file
    keywords = config['keywords']

    current_section = ""
    selected_units = config.get("checked_units", []) # Builds a list of compiled regexes for selected units
    unit_regexes = [re.compile(config['units'][unit], re.IGNORECASE) for unit in selected_units if unit in config['units']]
    requirement_regex = re.compile(r'^\[\w+[\-\.\d]*\]', re.IGNORECASE)
    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            current_section = paragraph.text
            continue
        # Check if the paragraph contains any of the keywords
        if any(keyword.lower() in paragraph.text.lower() for keyword in keywords):
            # Check if the section is not ignored
            if current_section != "" and not any(ignored_section in current_section for ignored_section in config['ignored_sections']):
                paragraphs.append((filename, current_section, paragraph.text))
        # Check if the paragraph matches any of the selected unit regexes
        elif any(unit_regex.search(paragraph.text) for unit_regex in unit_regexes):
            if requirement_regex.search(paragraph.text): # Check if the paragraph is a requirement (follows the pattern [R-X...])
                requirements.append((filename, current_section, paragraph.text))
            else:
                paragraphs.append((filename, current_section, paragraph.text))
    return paragraphs, requirements

def execute_filtering(config, update):
    ''' 
    Process all .docx files in a folder to extract relevant paragraphs
    :param config: The configuration dictionary
    :param update: The function to call to update the GUI status label and progress bar
    '''

    # Get the configuration values    
    llm_ip = config['llm_address']
    llm = config['model_name']
    folder_path = config['folder_path']
    keywords = config['keywords']
    possible_csv = config["output_folder_path"] + "/possible_paragraphs.csv"
    no_csv = config["output_folder_path"] + "/no_paragraphs.csv"

    # Initialize the list of requirements
    requirements = []

    with open(possible_csv, 'w', newline='', encoding='utf-8') as csvfile_possible, \
         open(no_csv, 'w', newline='', encoding='utf-8') as csvfile_no:
        csvwriter_possible = csv.writer(csvfile_possible, delimiter=';')
        csvwriter_no = csv.writer(csvfile_no, delimiter=';')

        csvwriter_possible.writerow(['File', 'Chapter', 'Paragraph', 'LLM response'])
        csvwriter_no.writerow(['File', 'Chapter', 'Paragraph', 'LLM response'])

        for filename in os.listdir(folder_path):
            if filename.endswith('.doc'):
                convert(os.path.join(folder_path, filename))
                update("Converting " + filename + " to .docx")
                os.remove(os.path.join(folder_path, filename))

        i = 0 # Counter for the progress bar
        for filename in os.listdir(folder_path):
            if filename.endswith('.docx'):
                update("Processing " + filename, i/len(os.listdir(folder_path)))
                file_path = os.path.join(folder_path, filename)
                doc = Document(file_path)
                found_paragraphs, found_requirements = extract_paragraphs_with_keywords(doc, filename, config)
                requirements.extend(found_requirements)
                for filename, section, paragraph in found_paragraphs:
                    llm_response = ask_llm(paragraph, keywords[0], llm, llm_ip)
                    if llm_response == "NO":
                        csvwriter_no.writerow([filename[:-5], section, paragraph, llm_response])
                    if llm_response == "POSSIBLE":
                        csvwriter_possible.writerow([filename[:-5], section, paragraph, llm_response])  
            i += 1                     
    with open(config["output_folder_path"] + "/output.xlsx", 'w', newline='', encoding='utf-8') as csvfile:
        update("Saving output to a file...")
        csvwriter = csv.writer(csvfile, delimiter=';')
        # csvwriter.writerow(['File', 'Chapter', 'Requirement'])
        for filename, section, paragraph in requirements:
            csvwriter.writerow([filename[:-5], section, paragraph])

with open('prompts.json', 'r') as f:
    prompts = json.load(f)

# main function (executed when running this file)
if __name__ == "__main__":
    print("This scipt is part of the requirements generation.\nusage: python gui_requirements.py")