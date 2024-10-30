# import the necessary libraries
# we should probably change this 
import os
import csv
from docx import Document
import requests
import json
import re

global llm_ip
llm_ip = "localhost:11435"

def ask_llm(paragraph):
    url = f'http://{llm_ip}/api/generate'
    data = {
        "model": "llama3.1:70b",
        "prompt": prompts['verify_context'] + paragraph,
        "stream": False
        }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    json_data = json.loads(response.text)
    return json_data['response']

def extract_paragraphs_with_keywords(doc, keywords, filename, config):
    paragraphs = []
    requirements = []
    current_section = ""
    unit_regex = re.compile(rf'\b\d+\s*{re.escape("ms")}\b\.?', re.IGNORECASE)
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
        # Check if the paragraph contains a ms unit
        elif unit_regex.search(paragraph.text):
            # Check if the paragraph is a requirement (follows the pattern [R-X...])
            if requirement_regex.search(paragraph.text):
                requirements.append((filename, current_section, paragraph.text))
            else:
                paragraphs.append((filename, current_section, paragraph.text))
    return paragraphs, requirements


def process_docx_files_in_folder(folder_path, search_word, output_csv, config):
    requirements = []
    with open(output_csv[0], 'w', newline='', encoding='utf-8') as csvfile_possible, \
         open(output_csv[1], 'w', newline='', encoding='utf-8') as csvfile_no:
        csvwriter_possible = csv.writer(csvfile_possible, delimiter=';')
        csvwriter_no = csv.writer(csvfile_no, delimiter=';')

        csvwriter_possible.writerow(['File', 'Chapter', 'Paragraph', 'LLM response'])
        csvwriter_no.writerow(['File', 'Chapter', 'Paragraph', 'LLM response'])

        for filename in os.listdir(folder_path):
            if filename.endswith('.docx'):
                file_path = os.path.join(folder_path, filename)
                print(f"Processing file: {file_path}")
                doc = Document(file_path)
                found_paragraphs, found_requirements = extract_paragraphs_with_keywords(doc, search_word, filename, config)
                requirements.extend(found_requirements)
                for filename, section, paragraph in found_paragraphs:
                    llm_response = ask_llm(paragraph)
                    if llm_response == "NO":
                        csvwriter_no.writerow([filename[:-5], section, paragraph, llm_response])
                    if llm_response == "POSSIBLE":
                        csvwriter_possible.writerow([filename[:-5], section, paragraph, llm_response])                       
    with open("outputs/requirements.csv", 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(['File', 'Chapter', 'Requirement'])
        for filename, section, paragraph in requirements:
            csvwriter.writerow([filename[:-5], section, paragraph])

with open('prompts.json', 'r') as f:
    prompts = json.load(f)


def execute_filtering(config):
    llm_ip = config['llm_address']
    folder_path = config['folder_path']
    keywords = config['keywords']
    output_csv = config['latency_paragraphs']
    process_docx_files_in_folder(folder_path, keywords, output_csv, config)

########################################################################
# main function (executed when running this file)

if __name__ == "__main__":
    print("skibidi")